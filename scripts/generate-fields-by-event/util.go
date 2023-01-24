
package main

import (
	"strings"
	"os"
	"path/filepath"
	"log"
	"sort"
	"io/ioutil"
	"github.com/pkg/errors"
	"gopkg.in/yaml.v2"
)

// Remove the common path, and strip the "/" prefix from the result
func parePath(input string, common string) string {
	result := strings.TrimPrefix(input, common)

	return strings.TrimPrefix(result, "/")
}

func gatherFilterFiles(options generateOptions, fieldFiles []string) []string {
	var files []string

	for _, f := range fieldFiles {
		halfPath := parePath(f, options.packagesSourceDir)

		filterPath := filepath.Join(options.filteringDir, halfPath)

		// make sure this file exists
		if _,err := os.Stat(filterPath); err == nil {
			files = append(files, filterPath)
		}
	}

	return files
}

func gatherFieldsFiles(topDir string) ([]string, error) {
	var folders []string
	err := filepath.Walk(topDir,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if strings.HasSuffix(path, "fields.yml") || strings.HasSuffix(path, "fields.yaml") {
				pathy := parePath(path, topDir)
				folders = append(folders, pathy)
			}
			return nil
		})
	if err != nil {
		log.Println(err)
		return nil, err
	}
	sort.Slice(folders, func(i, j int) bool {
		return folders[i] < folders[j]
	})
	return folders, nil
}

func getAllFields(path string) (fieldDefinitionArray, error) {
	var fda fieldDefinitionArray

	body, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, errors.Wrapf(err, "reading fields from file failed (path: %s)",
			path)
	}

	err = yaml.Unmarshal(body, &fda)
	if err != nil {
		return nil, errors.Wrapf(err, "failed to unmarshal file (path: %s)",
			path)
	}

	return fda, nil
}

func captureFields(ecs string, fda fieldDefinitionArray) *set {
	s := NewSet()

	for _, b := range fda {
		path := b.Name
		if len(ecs) > 0 {
			path = ecs + "." + b.Name
		}

		if b.Fields != nil && len(b.Fields) > 0 {
			res := captureFields(path, b.Fields)
			for k, _ := range res.m {
				s.Add(k)
			}
		} else {
			s.Add(path)
		}
	}
	return s
}

func captureSortedFields(fda fieldDefinitionArray) fieldFilterArray {
	var result fieldFilterArray
	s := captureFields("", fda)

	for n,_ := range s.m {
		var path fieldFilter
		path.Ecs = n
		result = append(result, &path)
	}

	sort.Slice(result, func(i, j int) bool {
		return result[i].Ecs < result[j].Ecs
	})

	return result
}

func readInFilterFile(path string) (*allTheThings, error) {
	result := new(allTheThings)

	body, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, errors.Wrapf(err, "reading fields from file failed (path: %s)",
			path)
	}

	err = yaml.Unmarshal(body, &result)
	if err != nil {
		return nil, errors.Wrapf(err, "failed to unmarshal file (path: %s)",
			path)
	}

	return result, nil
}

func join(left, right fieldFilterArray) fieldFilterArray {
	var result fieldFilterArray
	var intersection fieldFilterArray

	var leftExclusive []string
	var rightExclusive []string

	var leftMax int = len(left)
	var rightMax int = len(right)

	var i int = 0
	var j int = 0

	for i < leftMax && j < rightMax {
		// copy over the left
		if left[i].Ecs < right[j].Ecs {
			result = append(result, left[i])
			leftExclusive = append(leftExclusive, left[i].Ecs)
			i++
		} else if right[j].Ecs < left[i].Ecs {
			result = append(result, right[j])
			rightExclusive = append(rightExclusive, right[j].Ecs)
			j++
		} else {
			result = append(result, left[i])
			intersection = append(intersection, left[i])
			i++
			j++
		}
	}

	for i < leftMax {
		result = append(result, left[i])
		leftExclusive = append(leftExclusive, left[i].Ecs)
		i++
	}
	for j < rightMax {
		result = append(result, right[j])
		rightExclusive = append(rightExclusive, right[j].Ecs)
		j++
	}

	// print the left-exclusive fields!
	for _,l := range leftExclusive {
		log.Printf("found left-exclusive field: %s\n", l)
	}

	// print the right-exclusive fields!
	for _,l := range rightExclusive {
		log.Printf("found right-exclusive field: %s\n", l)
	}

	return result
}
