// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"text/template"

	"github.com/pkg/errors"
)

const (
	readmeFilename = "README.md"
)

func gatherStreams(options generateOptions, packageName string) ([]string, error) {
	templatePath := filepath.Join(options.docTemplatesDir, fmt.Sprintf("%s/docs", packageName), readmeFilename)

	_, err := os.Stat(templatePath)
	if os.IsNotExist(err) {
		log.Printf(`Notice: the template file "%s" does not exist. The README.md file will not be rendered.`, templatePath)
		return nil, nil
	} else if err != nil {
		return nil, errors.Wrapf(err, "stat file failed (path: %s)", templatePath)
	}

	var dataStreams []string
	t := template.New(readmeFilename)
	t, err = t.Funcs(template.FuncMap{
		"event": func(dataStreamName string) (string, error) {
			return "event thing", nil
		},
		"fields": func(dataStreamName string) (string, error) {
			dataStreams = append(dataStreams, dataStreamName)
			return "fields thing", nil
		},
	}).ParseFiles(templatePath)
	if err != nil {
		return nil, errors.Wrapf(err, "parsing README template failed (path: %s)", templatePath)
	}

	var tpl bytes.Buffer
	err = t.Execute(&tpl, nil)
	return dataStreams, nil
}

func renderReadme(options generateOptions, packageName string, existing map[string][]string) error {
	templatePath := filepath.Join(options.docTemplatesDir, fmt.Sprintf("%s/docs", packageName), readmeFilename)

	_, err := os.Stat(templatePath)
	if os.IsNotExist(err) {
		log.Printf(`Notice: the template file "%s" does not exist. The README.md file will not be rendered.`, templatePath)
		return nil
	} else if err != nil {
		return errors.Wrapf(err, "stat file failed (path: %s)", templatePath)
	}

	t := template.New(readmeFilename)
	t, err = t.Funcs(template.FuncMap{
		"event": func(dataStreamName string) (string, error) {
			return renderSampleEvent(options, packageName, dataStreamName)
		},
		"fields": func(dataStreamName string) (string, error) {
			return renderExportedFields(options, packageName, dataStreamName, existing)
		},
	}).ParseFiles(templatePath)
	if err != nil {
		return errors.Wrapf(err, "parsing README template failed (path: %s)", templatePath)
	}

	outputPath := filepath.Join(options.packagesSourceDir, packageName, "docs", readmeFilename)
	f, err := os.OpenFile(outputPath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return errors.Wrapf(err, "opening README file for writing failed (path: %s)", outputPath)
	}
	defer f.Close()

	err = t.Execute(f, nil)
	if err != nil {
		return errors.Wrapf(err, "rendering README file failed (path: %s)", templatePath)
	}
	return nil
}

func renderReadmePlatform(options generateOptions, packageName, dataStream, os_ string) (bool, error) {

	var result = false
	output, err := renderFilteredFields(options, packageName, dataStream, os_)

	if err != nil {
		return false, errors.Wrapf(err, "failed to render fields for %s/%s/%s", packageName, dataStream, os_)
	}

	if len(output) > 0 {
		result = true
		outputDir := filepath.Join(options.packagesSourceDir, packageName, "docs", dataStream)
		if _,err := os.Stat(outputDir); errors.Is(err, os.ErrNotExist) {
			err := os.MkdirAll(outputDir, os.ModePerm)

			if err != nil {
				return result, errors.Wrapf(err, fmt.Sprintf("failed to make directory %s", outputDir))
			}
		}

		outputPath := filepath.Join(outputDir, fmt.Sprintf("%s.md", os_))
		f, err := os.OpenFile(outputPath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0644)
		if err != nil {
			return result, errors.Wrapf(err, "opening README file for writing failed (path: %s)", outputPath)
		}
		defer f.Close()

		f.WriteString(output)
		if err != nil {
			return result, errors.Wrapf(err, "rendering README file failed (path: %s)", outputPath)
		}
	}
	return result, nil
}
