package main

import (
	"github.com/pkg/errors"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

type eventDefinition struct {
	Name   string `yaml:"name"`
	Values []struct {
		Name  string `yaml:"name"`
		Value string `yaml:"value"`
	} `yaml:"values,omitempty"`
	Kind     string      `yaml:"event.kind"`
	Category []string    `yaml:"event.category"`
	Type     []string    `yaml:"event.type"`
	Outcome  string      `yaml:"event.outcome,omitempty"`
	Action   string      `yaml:"event.action,omitempty"`
	Protocol string      `yaml:"network.protocol,omitempty"`

	Os       []string    `yaml:"os,omitempty"`

	// print out the definition
	// dumpDef(builder strings.Builder)
}

type fieldFilter struct {
	Ecs    string `yaml:"ecs"`
	All     []string  `yaml:"all,omitempty"`
	Windows []string  `yaml:"windows,omitempty"`
	Macos   []string  `yaml:"macos,omitempty"`
	Linux   []string  `yaml:"linux,omitempty"`

	// methods:
	//  see if the given ecs path is supported for this os in this event type/subtype
	// findPath(ecs, os string) -> bool
	//  does this event type/subtype have anything at all configured
	// isEmpty() -> bool
}

type allTheThings struct {
	Definitions []eventDefinition  `yaml:"definitions"`
	Os          []string           `yaml:"os"`
	Fields      []fieldFilter      `yaml:"fields"`
}

func isInArrayAllowAll(needle string, haystack []string) bool {
	for i:= range haystack {
		// if one of the items in haystack is "all", we treat that like '*'
		if haystack[i] == "all" {
			return true
		}
		if needle == haystack[i] {
			return true
		}
	}
	return false
}

func (f fieldFilter) findPath(ecs, os_ string) bool {
	// first, look through "all"
	if isInArrayAllowAll(ecs, f.All) {
		return true
	}

	// then go through the specific os filters
	if os_ == "windows" {
		return isInArrayAllowAll(ecs, f.Windows)
	} else if os_ == "linux" {
		return isInArrayAllowAll(ecs, f.Linux)
	} else if os_ == "macos" {
		return isInArrayAllowAll(ecs, f.Macos)
	}

	return false
}

// if nothing has been configured, then this is an allow-all
func (f fieldFilter) isEmpty() bool {
	if len(f.All) > 0 {
		return false
	} else if len(f.Windows) > 0 {
		return false
	} else if len(f.Linux) > 0 {
		return false
	} else if len(f.Macos) > 0 {
		return false
	}

	return true
}

func (d eventDefinition) matchesOs(os_ string) bool {
	if len(d.Os) > 0 {
		// if the passed-in os doesn't match anything, bail
		for _, o := range d.Os {
			if o == "all" || o == os_ {
				return true
			}
		}

		// if we got here, there was no match
		return false
	}

	// if there is no os defined in the definition, it matches everything
	return true
}

//
func (d eventDefinition) dumpDefinition(builder *strings.Builder, os_ string) {

	// is this definition supported for this os?
	if ! d.matchesOs(os_) {
		return
	}

	// do the header
	builder.WriteString(fmt.Sprintf("\nECS fields for %s\n", d.Name))

	// event.kind
	if d.Kind != "" {
		builder.WriteString(fmt.Sprintf(" - event.kind :: %s\n", d.Kind))
	}

	// event.category
	if len(d.Category) > 1 {
		builder.WriteString(" - event.category (array)\n")
		for i := range d.Category {
			builder.WriteString(fmt.Sprintf("   * %s\n", d.Category[i]))
		}
	} else if len(d.Category) > 0 {
		builder.WriteString(fmt.Sprintf(" - event.category :: %s\n", d.Category[0]))
	}

	// event.type
	if len(d.Type) > 1 {
		builder.WriteString(" - event.type (array)\n")
		for i := range d.Type {
			builder.WriteString(fmt.Sprintf("   * %s\n", d.Type[i]))
		}
	} else if len(d.Type) > 0 {
		builder.WriteString(fmt.Sprintf(" - event.type :: %s\n", d.Type[0]))
	}

	// event.action
	if d.Action != "" {
		builder.WriteString(fmt.Sprintf(" - event.action :: %s\n", d.Action))
	}

	// event.outcome
	if d.Outcome != "" {
		builder.WriteString(fmt.Sprintf(" - event.outcome :: %s\n", d.Outcome))
	}

	// network.protocol (optional)
	if d.Protocol != "" {
		builder.WriteString(fmt.Sprintf(" - network.protocol :: %s\n", d.Protocol))
	}


	// extra things
	for i := range d.Values {
		builder.WriteString(fmt.Sprintf(" - %s :: %s\n", d.Values[i].Name,
			d.Values[i].Value))
	}

	builder.WriteString("\n")
}

// Remove the common path, and strip the "/" prefix from the result
func parePath(input string, common string) string {
	result := strings.TrimPrefix(input, common)

	return strings.TrimPrefix(result, "/")
}

// this just copies the field file paths from "packages" to "custom_documentation" (if they exist)
func gatherFilterFiles(options generateOptions, fieldFiles []string) []string {
	var files []string

	for _, f := range fieldFiles {
		halfPath := parePath(f, options.packagesSourceDir)

		filterPath := filepath.Join(options.filteringDir, halfPath)

		// make sure this file exists
		if _, err := os.Stat(filterPath); err == nil {
			files = append(files, filterPath)
		}
	}

	return files
}

func readInFilterFile(path string) (allTheThings, error) {
	var result allTheThings

	body, err := ioutil.ReadFile(path)
	if err != nil {
		return result, errors.Wrapf(err, "reading fields from file failed (path: %s)",
			path)
	}

	err = yaml.UnmarshalStrict(body, &result)
	if err != nil {
		return result, errors.Wrapf(err, "failed to unmarshal file (path: %s)",
			path)
	}

	return result, nil
}

func join(left, right []fieldFilter) []fieldFilter {
	var holdingSet map[string]int = make(map[string]int)

	var result []fieldFilter

	for i := range left {
		holdingSet[left[i].Ecs] = 1
		result = append(result, left[i])
	}

	for i := range right {
		// if this is already in the set, move along
		if v,ok := holdingSet[right[i].Ecs]; ok && v == 1 {
			holdingSet[right[i].Ecs] = 2
			continue
		}

		// if this is not already in the set, add it to the result
		holdingSet[right[i].Ecs] = 3
		result = append(result, right[i])
	}


	// sort the output before returning
	sort.Slice(result, func (i, j int) bool {
		return result[i].Ecs < result[j].Ecs
	})

	// print left- and right-exclusive
	for _, l := range result {
		res := holdingSet[l.Ecs]
		if res == 1 {
			log.Printf("found left-exclusive field: %s\n", l.Ecs)
		} else if res == 3 {
			log.Printf("found right-exclusive field: %s\n", l.Ecs)
		}
	}

	return result
}
