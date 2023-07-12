// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package main

import (
	// "fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	// "text/template"

	"gopkg.in/yaml.v2"

	"github.com/pkg/errors"
)

type eventOverview struct {
	Name        string `yaml:"name"`
	Description string `yaml:"description"`
}

type eventIdentification struct {
	Filter map[string]string `yaml:"filter"`
}

type eventFields struct {
	Endpoint []string `yaml:"endpoint"`
}

type eventDoc struct {
	Overview       eventOverview       `yaml:"overview"`
	Identification eventIdentification `yaml:"identification"`
	Fields         eventFields         `yaml:"fields"`
}

func findCustomDocFiles(root string) ([]string, error) {
	// Return all the custom doc files under root
	var customFiles []string

	err := filepath.WalkDir(root, func(path string, info os.DirEntry, err error) error {
		if !info.IsDir() {
			customFiles = append(customFiles, path)
		}
		return nil
	})
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

func renderCustomDocumentation(options generateOptions, packageName string) error {
	customDocPackageDir := filepath.Join(options.customDocDir, packageName)
	customFiles, err := findCustomDocFiles(customDocPackageDir)

	if err != nil {
		return errors.Wrapf(err, "failed to find custom documentation (path: %s", customDocPackageDir)
	}

	for _, path := range customFiles {
		log.Printf("CUSTOM DOC %s", path)

		customYaml, err := loadCustomDocFile(path)
		if err != nil {
			return err
		}

		log.Printf("CUSTOM YAML %s", path)
		log.Printf(" - Overview.Name: %s", customYaml.Overview.Name)
		log.Printf(" - Overview.Description: %s", customYaml.Overview.Description)
		log.Printf(" - Identification.Filter: %s", customYaml.Identification.Filter)
		log.Printf(" - len(Fields): %d", len(customYaml.Fields.Endpoint))
	}
	return nil
}
