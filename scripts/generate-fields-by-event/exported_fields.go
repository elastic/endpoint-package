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

type fieldOsFilter struct {
	Name        string               `yaml:"name"`
	Os          []string             `yaml:"os,omitempty"`
}

type fieldFilter struct {
	Ecs         string               `yaml:"ecs,omitempty"`
	Filter      []fieldOsFilter      `yaml:"found_in_event,omitempty"`
}

type fieldFilterArray []*fieldFilter

type def struct {
	Name        string               `yaml:"name"`
	Value       string               `yaml:"value"`
}

type eventDefinition struct {
	Name        string               `yaml:"name"`
	Values      []def                `yaml:"values"`
}

type allTheThings struct {
	Definitions []eventDefinition    `yaml:"definitions"`
	Fields      fieldFilterArray     `yaml:"fields"`
}

func renderExportedFields(options generateOptions, packageName, dataStreamName string) (string, error) {
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

	// gather filter files
	filterFiles := gatherFilterFiles(options, fieldFiles)

	// loop over all the definitions
	// for each definition, print out the make-up of the ECS fields
	// print out each of the filtered fields

	var builder strings.Builder
	builder.WriteString("#### Exported fields\n\n")

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
