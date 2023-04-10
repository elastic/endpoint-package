// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
	"sort"
	"strings"

	"os"

	"github.com/pkg/errors"
	"gopkg.in/yaml.v2"
)

type fieldDefinition struct {
	Name        string               `yaml:"name,omitempty"`
	Type        string               `yaml:"type,omitempty"`
	Description string               `yaml:"description,omitempty"`
	Fields      fieldDefinitionArray `yaml:"fields,omitempty"`
	Enabled     *bool                `yaml:"enabled,omitempty"`
}

type fieldDefinitionArray []*fieldDefinition

func (s fieldDefinitionArray) Len() int           { return len(s) }
func (s fieldDefinitionArray) Swap(i, j int)      { s[i], s[j] = s[j], s[i] }
func (s fieldDefinitionArray) Less(i, j int) bool { return s[i].Name < s[j].Name }

type fieldsTableRecord struct {
	name        string
	description string
	aType       string
}

func updateFilterFile(options generateOptions, fieldFiles []string, collected []fieldsTableRecord) error {
	// if we are not doing this, just bail
	if !options.updateFilters {
		return nil
	}

	// gather the filter files (assert there is only one)
	filterFiles := gatherFilterFiles(options, fieldFiles)
	var filter allTheThings
	var filterFile string

	if len(filterFiles) > 1 {
		panic(fmt.Sprintf("There are too many files (%d) in the path %s\n", len(filterFiles),
			filterFiles[0]))
		return errors.New(fmt.Sprintf("Too many files (%d) in path %s",
			len(filterFiles), fieldFiles[0]))
	}

	if len(fieldFiles) == 0 {
		return errors.New("Not enough files (0)!")
	}

	// below here, len(fieldFiles) is guaranteed to be 1
	filterFile = filepath.Join(options.filteringDir, parePath(fieldFiles[0], options.packagesSourceDir))

	for _, c := range collected {
		filter.Fields = append(filter.Fields, fieldFilter{Ecs: c.name})
	}

	sort.Slice(filter.Fields, func(i, j int) bool {
		return filter.Fields[i].Ecs < filter.Fields[j].Ecs
	})

	if len(filterFiles) == 0 {
		// There are no filter files right now, so create them
		fmt.Printf("No filter file found, so just dumping what we have to %s\n",
			filterFile)
		dir := filepath.Dir(filterFile)
		if _, err := os.Stat(dir); errors.Is(err, os.ErrNotExist) {
			err := os.MkdirAll(dir, os.ModePerm)

			if err != nil {
				return errors.Wrap(err, fmt.Sprintf("making directory path %s failed", dir))
			}
		}
	} else {
		// we have some filters, so join the ecs stuff with the existing filter
		existing, _ := readInFilterFile(filterFile)
		filter.Definitions = existing.Definitions
		for i := range filter.Definitions {
			if filter.Definitions[i].Kind == "" {
				filter.Definitions[i].Kind = "event"
			}
			if len(filter.Definitions[i].Type) == 0 {
				filter.Definitions[i].Type = append(filter.Definitions[i].Type, "info")
			}
		}
		filter.Os = existing.Os
		filter.Fields = join(existing.Fields, filter.Fields)
	}

	// update the things
	blob, _ := yaml.Marshal(&filter)
	err := ioutil.WriteFile(filterFile, blob, 0777)
	if err != nil {
		return errors.Wrapf(err, "Failed to write file %s", filterFile)
	}

	return nil
}

func getFilteredFields(filter allTheThings, name, os string, collected []fieldsTableRecord) []fieldsTableRecord {
	var result []fieldsTableRecord

	// create a map from the filter that is limited by event and os
	var mapping map[string]int = make(map[string]int)

	var found bool = false
	for i := range filter.Os {
		if filter.Os[i] == os {
			found = true
			break
		}
	}

	// if this event isn't supported on this os at all, don't output anything
	if !found {
		return result
	}

	// for each ecs path in the filter
	for _,f := range filter.Fields {
		if f.isEmpty() || f.findPath(name, os) {
			mapping[f.Ecs] = 1
		}
	}

	// loop over the collected fields
	for _,f := range collected {
		if v,ok := mapping[f.name]; ok && v == 1 {
			result = append(result, f)
		}
	}

	return result
}

func renderExportedFields(options generateOptions, packageName, dataStreamName string, osMap map[string][]string) (string, error) {
	dataStreamPath := filepath.Join(options.packagesSourceDir, packageName, "data_stream", dataStreamName)
	fieldFiles, err := listFieldFields(dataStreamPath)
	if err != nil {
		return "", errors.Wrapf(err, "listing field files failed (dataStreamPath: %s)", dataStreamPath)
	}

	fields, err := loadFields(fieldFiles)
	if err != nil {
		return "", errors.Wrap(err, "loading fields files failed")
	}

	collected, err := collectFieldsFromDefinitions(fields)
	if err != nil {
		return "", errors.Wrap(err, "collecting fields files failed")
	}

	var builder strings.Builder
	builder.WriteString("#### Exported fields -- placeholder\n\n")

	/*
	var needNewParagraph = false
	for _,os_ := range osMap[dataStreamName] {
		needNewParagraph = true
		builder.WriteString(fmt.Sprintf("* [link to %s-specific fields](%s)\n", os_, filepath.Join(".", dataStreamName, fmt.Sprintf("%s.md", os_))))
	}

	if needNewParagraph {
		builder.WriteString("\n\n")
	}
	*/

	if len(collected) == 0 {
		builder.WriteString("(no fields available)\n")
		return builder.String(), nil
	}
	builder.WriteString("| Field | Description | Type |\n")
	builder.WriteString("|---|---|---|\n")
	for _, c := range collected {
		description := strings.TrimSpace(strings.ReplaceAll(c.description, "\n", " "))
		builder.WriteString(fmt.Sprintf("| %s | %s | %s |\n", c.name, description, c.aType))
	}
	return builder.String(), nil
}

func findNeedleInHaystack(needle string, haystack []string) bool {
	for i := range haystack {
		if needle == haystack[i] {
			return true
		}
	}
	return false
}

func renderFilteredFields(options generateOptions, packageName, dataStreamName, os_ string) (string, error) {
	dataStreamPath := filepath.Join(options.packagesSourceDir, packageName, "data_stream", dataStreamName)
	fieldFiles, err := listFieldFields(dataStreamPath)
	if err != nil {
		return "", errors.Wrapf(err, "listing field files failed (dataStreamPath: %s)", dataStreamPath)
	}

	fields, err := loadFields(fieldFiles)
	if err != nil {
		return "", errors.Wrap(err, "loading fields files failed")
	}

	collected, err := collectFieldsFromDefinitions(fields)
	if err != nil {
		return "", errors.Wrap(err, "collecting fields files failed")
	}

	// update the filters (bail early if we don't need to update)
	err = updateFilterFile(options, fieldFiles, collected)
	if err != nil {
		return "", errors.Wrap(err, "updating filters failed")
	}

	var builder strings.Builder

	// From here, we need to gather the filtered things
	// If we are supposed to update the filters, do that, too
	// There should really only be one file, but loop here, anyway
	filterFiles := gatherFilterFiles(options, fieldFiles)
	for _, f := range filterFiles {
		// load the filter
		var filter, err = readInFilterFile(f)
		if err != nil {
			return "", errors.Wrapf(err, "failed to load filter file %s", f)
		}

		// if this dataStream isn't supported on this os, just bail
		if !findNeedleInHaystack(os_, filter.Os) {
			continue
		}

		// output the definitions
		if len(filter.Definitions) > 0 {
			builder.WriteString(fmt.Sprintf("\n*Definitions for %s*\n", dataStreamName))
			for _, def := range filter.Definitions {
				def.dumpDefinition(&builder, os_)

			}
		}

		// loop over the definitions
		for _, def := range filter.Definitions {
			// if this event type isn't supported on this os, don't output anything
			if !def.matchesOs(os_) {
				continue
			}

			filteredCollected := getFilteredFields(filter, def.Name, os_, collected)

			builder.WriteString(fmt.Sprintf("Event type: %s\n", def.Name))
			if len(filteredCollected) == 0 {
				builder.WriteString("(no fields available)\n\n")
				continue
			}

			builder.WriteString("#### Exported fields\n\n")
			builder.WriteString("| Field | Description | Type |\n")
			builder.WriteString("|---|---|---|\n")
			for _, c := range filteredCollected {
				description := strings.TrimSpace(strings.ReplaceAll(
					c.description, "\n", " "))
				builder.WriteString(fmt.Sprintf("| %s | %s | %s |\n",
					c.name, description, c.aType))
			}
			builder.WriteString("\n")

		}

	}
	return builder.String(), nil
}

func listFieldFields(dataStreamPath string) ([]string, error) {
	fieldsPath := filepath.Join(dataStreamPath, "fields")

	var files []string
	fileInfos, err := ioutil.ReadDir(fieldsPath)
	if err != nil {
		return nil, errors.Wrapf(err, "reading dataStream fields dir failed (path: %s)", fieldsPath)
	}

	for _, fileInfo := range fileInfos {
		if !fileInfo.IsDir() {
			files = append(files, filepath.Join(fieldsPath, fileInfo.Name()))
		}
	}
	return files, nil
}

func loadFields(files []string) (fieldDefinitionArray, error) {
	var fdas fieldDefinitionArray

	for _, f := range files {
		var fda fieldDefinitionArray

		body, err := ioutil.ReadFile(f)
		if err != nil {
			return nil, errors.Wrapf(err, "reading fields file failed (path: %s)", f)
		}

		err = yaml.Unmarshal(body, &fda)
		if err != nil {
			return nil, errors.Wrapf(err, "unmarshaling fields file failed (path: %s)", f)
		}
		fdas = append(fdas, fda...)
	}
	return fdas, nil
}

func collectFieldsFromDefinitions(fieldDefinitions fieldDefinitionArray) ([]fieldsTableRecord, error) {
	var records []fieldsTableRecord

	var err error
	var disabledField string
	sort.Sort(fieldDefinitions)
	for _, f := range fieldDefinitions {
		records, err = visitFields("", f, records, &disabledField)
		if err != nil {
			return nil, errors.Wrapf(err, "visiting fields failed")
		}
	}

	sort.Slice(records, func(i, j int) bool {
		return sort.StringsAreSorted([]string{records[i].name, records[j].name})
	})
	return uniqueTableRecords(records), nil
}

func visitFields(namePrefix string, f *fieldDefinition, records []fieldsTableRecord, disabledField *string) ([]fieldsTableRecord, error) {
	var name = namePrefix
	if namePrefix != "" {
		name += "."
	}
	name += f.Name
	if disabledField != nil && *disabledField != "" && strings.HasPrefix(name, *disabledField) {
		// skipping the field because a top level field was disabled
		return records, nil
	}

	if f.Enabled != nil && *f.Enabled == false {
		// found a new disabled field so use that one from now on
		// this works because all the fields are sorted so the top level fields are encountered first
		*disabledField = name
		return records, nil
	}

	if len(f.Fields) == 0 && f.Type != "group" {
		records = append(records, fieldsTableRecord{
			name:        name,
			description: f.Description,
			aType:       f.Type,
		})
		return records, nil
	}

	var err error
	sort.Sort(f.Fields)
	for _, fieldEntry := range f.Fields {
		records, err = visitFields(name, fieldEntry, records, disabledField)
		if err != nil {
			return nil, errors.Wrapf(err, "recursive visiting fields failed (namePrefix: %s)", namePrefix)
		}
	}
	return records, nil
}

func uniqueTableRecords(records []fieldsTableRecord) []fieldsTableRecord {
	fieldNames := make(map[string]bool)
	var unique []fieldsTableRecord
	for _, r := range records {
		if _, ok := fieldNames[r.name]; !ok {
			fieldNames[r.name] = true
			unique = append(unique, r)
		}
	}
	return unique
}
