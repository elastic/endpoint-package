// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"text/template"

	"gopkg.in/yaml.v2"

	"github.com/pkg/errors"
)

type customDocEvent struct {
	filePath    string
	dataStream  string
	fileSubPath string
	doc         eventDoc
}

type eventOverview struct {
	Name        string `yaml:"name"`
	Description string `yaml:"description"`
}

type eventIdentification struct {
	Os         []string          `yaml:"os"`
	DataStream string            `yaml:"data_stream"`
	Filter     map[string]string `yaml:"filter"`
}

type eventFields struct {
	Endpoint []string `yaml:"endpoint"`
}

type eventDoc struct {
	Overview       eventOverview       `yaml:"overview"`
	Identification eventIdentification `yaml:"identification"`
	Fields         eventFields         `yaml:"fields"`
}

func findCustomDocFiles(root string) ([]customDocEvent, error) {
	// Return all the custom doc files under root. Intelligently understand the directory structure
	// and interpret the data_stream name from it for each file.
	var customFiles []customDocEvent

	dataStreamRoot := filepath.Clean(filepath.Join(root, "data_stream"))
	dataStreamNames, err := os.ReadDir(dataStreamRoot)
	if err != nil {
		return nil, errors.Wrapf(err, "Failed to list directory %s", dataStreamRoot)
	}
	for _, dataStreamName := range dataStreamNames {
		dataStreamNameRoot := filepath.Join(dataStreamRoot, dataStreamName.Name())
		err := filepath.WalkDir(dataStreamNameRoot, func(path string, info os.DirEntry, err error) error {

			if !info.IsDir() {
				cleanPath := filepath.Clean(path)
				event := customDocEvent{filePath: path, dataStream: dataStreamName.Name(), fileSubPath: cleanPath[len(dataStreamRoot):]}
				customFiles = append(customFiles, event)
			}
			return nil
		})
		if err != nil {
			return nil, errors.Wrapf(err, "failed to load data_stream directory %s", dataStreamName.Name())
		}
	}
	return customFiles, err
}

func loadCustomDocFile(path string) (eventDoc, error) {
	var result eventDoc

	body, err := ioutil.ReadFile(path)
	if err != nil {
		return result, errors.Wrapf(err, "reading file failed (path: %s)", path)
	}

	err = yaml.UnmarshalStrict(body, &result)
	if err != nil {
		return result, errors.Wrapf(err, "parsing yaml failed (path: %s)", path)
	}

	return result, nil
}

func loadDataStreamFields(options generateOptions, packageName string, dataStreamName string) ([]fieldsTableRecord, error) {
	dataStreamPath := filepath.Join(options.packagesSourceDir, packageName, "data_stream", dataStreamName)
	fieldFiles, err := listFieldFields(dataStreamPath)
	if err != nil {
		return nil, errors.Wrapf(err, "listing field files failed (dataStreamPath: %s)", dataStreamPath)
	}

	fields, err := loadFields(fieldFiles)
	if err != nil {
		return nil, errors.Wrap(err, "loading fields files failed")
	}

	collected, err := collectFieldsFromDefinitions(fields)
	if err != nil {
		return nil, errors.Wrap(err, "collecting fields files failed")
	}

	return collected, nil
}

type fieldsTableMap map[string]fieldsTableRecord

func renderCustomDocumentationEvent(options generateOptions, packageName string, event customDocEvent, fields fieldsTableMap) error {
	templatePath := filepath.Join(options.docTemplatesDir, fmt.Sprintf("%s/docs", packageName), "CustomDocumentation.md")

	_, err := os.Stat(templatePath)
	if err != nil {
		return errors.Wrapf(err, "failed to find or stat template file %s", templatePath)
	}

	t := template.New("CustomDocumentation.md")
	t, err = t.Funcs(template.FuncMap{
		"overview_name": func() (string, error) {
			return event.doc.Overview.Name, nil
		},
		"overview_description": func() (string, error) {
			return event.doc.Overview.Description, nil
		},
		"identification_os": func() (string, error) {
			sort.Strings(event.doc.Identification.Os)
			return strings.Join(event.doc.Identification.Os, ", "), nil
		},
		"identification_data_stream": func() (string, error) {
			return event.doc.Identification.DataStream, nil
		},
		"identification_kql": func() (string, error) {
			return "FILL ME IN", nil
		},
	}).ParseFiles(templatePath)
	if err != nil {
		return errors.Wrapf(err, "parsing CustomDocumentation template failed (path: %s)", templatePath)
	}

	subPath := event.fileSubPath
	if strings.HasSuffix(subPath, "yaml") {
		subPath = subPath[:len(subPath)-4] + "md"
	} else if strings.HasSuffix(subPath, "yml") {
		subPath = subPath[:len(subPath)-3] + "md"
	} else {
		subPath = subPath + ".md"
	}

	outputPath := filepath.Join(options.packagesSourceDir, packageName, "docs", "custom_documentation", subPath)
	f, err := os.OpenFile(outputPath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return errors.Wrapf(err, "opening %s for writing failed", outputPath)
	}
	defer f.Close()

	err = t.Execute(f, nil)
	if err != nil {
		return errors.Wrapf(err, "rendering custom documentation failed (path: %s)", templatePath)
	}
	return nil
}

func renderCustomDocumentation(options generateOptions, packageName string) error {
	customDocPackageDir := filepath.Join(options.customDocDir, packageName)
	customFiles, err := findCustomDocFiles(customDocPackageDir)

	if err != nil {
		return errors.Wrapf(err, "failed to find custom documentation (path: %s", customDocPackageDir)
	}

	for _, event := range customFiles {
		doc, err := loadCustomDocFile(event.filePath)
		if err != nil {
			return err
		}

		event.doc = doc

		log.Printf("CUSTOM YAML %s", event.filePath)
		log.Printf(" - Data Stream Name: %s", event.dataStream)
		log.Printf(" - Overview.Name: %s", event.doc.Overview.Name)
		log.Printf(" - Overview.Description: %s", event.doc.Overview.Description)
		log.Printf(" - Identification.Filter: %s", event.doc.Identification.Filter)

		// TODO enforce good data in event.doc

		fields, err := loadDataStreamFields(options, packageName, event.dataStream)
		if err != nil {
			return errors.Wrapf(err, "failed to load data stream fields for %s", event.dataStream)
		}

		haveFields := make(fieldsTableMap)
		for _, field := range fields {
			haveFields[field.name] = field
		}

		for _, wantFieldName := range event.doc.Fields.Endpoint {
			haveField, ok := haveFields[wantFieldName]
			if !ok {
				err := fmt.Errorf("field %s in %s is not in data_steam %s definition",
					wantFieldName, event.filePath, event.dataStream)
				// TODO return error don't just print it. this requires documentation updates first.
				log.Printf("ERROR FIXME: %s", err)
			}

			log.Printf(" - HAVE %s %s", wantFieldName, haveField.name)

			err := renderCustomDocumentationEvent(options, packageName, event, haveFields)
			if err != nil {
				return errors.Wrapf(err, "failed to render %s", event.filePath)
			}
		}
	}
	return nil
}
