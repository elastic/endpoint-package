package main

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/Masterminds/semver/v3"
	"gopkg.in/yaml.v3"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "argument required: version to add changelog entries under")
		os.Exit(1)
	}

	lastV := lastPublishedRelease()
	response := commitList(lastV)

	// if commit message ends like  (#444)  then it is probably a PR reference
	prPattern := regexp.MustCompile(`\s*\(\#(\d+)\)$`)

	for _, c := range response.Commits {
		firstLine := strings.Split(strings.ReplaceAll(c.Commit.Message, "\r\n", "\n"), "\n")[0]
		matches := prPattern.FindStringSubmatch(firstLine)
		if matches == nil {
			// no PR to reference!
			fmt.Printf("Commit %s did not contain a PR number in its commit message in the expected place. Please add it manually. The commit message was:\n%s\n", c.SHA, c.Commit.Message)
			continue
		}
		prNo, _ := strconv.Atoi(matches[1])

		message := strings.TrimSuffix(firstLine, matches[0]) // trim PR number from changelog entry line

		cmd := exec.Command(
			"../../scripts/go-tools/bin/elastic-package",
			"changelog", "add",
			"--description", message,
			"--link", fmt.Sprintf("https://github.com/elastic/endpoint-package/pull/%d", prNo),
			"--type", "enhancement",
			"--version", os.Args[1])
		cmd.Dir = "./package/endpoint"
		_, err := cmd.CombinedOutput()
		if err != nil {
			panic(err)
		}

		//fmt.Printf("elastic-package changelog add --description \"%s\" --link https://github.com/elastic/endpoint-package/pull/%d --type enhancement --version \n", message, prNo)

	}

	fmt.Println("entries added, please review the changes in the changelog file and edit as needed.")

}

func makeClient(t time.Duration) *http.Client {
	return &http.Client{
		Timeout: t,
		Transport: &http.Transport{
			Dial: (&net.Dialer{
				Timeout: t,
			}).Dial,
		},
	}
}

// get last changelog version (without prerelease suffixes like -next)
func lastPublishedRelease() string {
	f, err := os.OpenFile("package/endpoint/changelog.yml", os.O_RDONLY, 0644)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	entries := make([]map[string]interface{}, 0, 50)
	if err := yaml.NewDecoder(f).Decode(&entries); err != nil {
		panic(err)
	}

	if len(entries) == 0 {
		fmt.Fprintln(os.Stderr, "previous changelog version not found")
		os.Exit(1)
	}

	for _, e := range entries {
		if v, ok := e["version"].(string); ok {
			semv, err := semver.NewVersion(v)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Unable to parse changelog version '%s': %v\n", v, err)
				continue
			}
			if semv.Prerelease() != "" {
				//fmt.Fprintf(os.Stderr, "%s is a Prerelease version. Skipping\n", v)
				continue
			}
			return v
		}

	}

	fmt.Fprintln(os.Stderr, "previous changelog version not found")
	os.Exit(1)
	return ""
}

type ghCompareResponse struct {
	Commits []struct {
		SHA    string `json:"sha"`
		Commit struct {
			Message string `json:"message"`
		} `json:"commit"`
		HTMLurl string `json:"html_url"`
	} `json:"commits"`
}

func commitList(since string) ghCompareResponse {
	client := makeClient(30 * time.Second)

	req, err := http.NewRequest(http.MethodGet, fmt.Sprintf("https://api.github.com/repos/elastic/endpoint-package/compare/v%s...main", since), nil)
	if err != nil {
		panic(err)
	}

	req.Header.Set("Accept", "application/vnd.github+json")
	req.Header.Set("X-Github-Api-Version", "2022-11-28")
	resp, err := client.Do(req)

	if err != nil {
		panic(err)
	}
	if resp.StatusCode != http.StatusOK {
		panic(fmt.Errorf("%d status code when retrieving changelog commits", resp.StatusCode))
	}

	var r ghCompareResponse
	defer resp.Body.Close()
	if err := json.NewDecoder(resp.Body).Decode(&r); err != nil {
		panic(err)
	}
	return r
}
