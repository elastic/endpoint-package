// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package main

import (
	"flag"
	"log"
	"os"
	"io/ioutil"
	"strings"
	"fmt"
	"path/filepath"
	// "sort"
	// "reflect"

	"github.com/pkg/errors"
	"gopkg.in/yaml.v2"
)

type generateOptions struct {
	filteringDir      string
	packages          string
	packagesSourceDir string
	doGenerate        bool
}

func (o *generateOptions) validate() error {
	_, err := os.Stat(o.packagesSourceDir)
	if err != nil {
		return errors.Wrapf(err, "stat file failed for packages directory (path: %s)", o.packagesSourceDir)
	}

	_, err = os.Stat(o.filteringDir)
	if err != nil {
		return errors.Wrapf(err, "stat file failed for filtering docs (path: %s)", o.filteringDir)
	}

	return nil
}

func (o *generateOptions) selectedPackages() []string {
	var selected []string
	p := strings.TrimSpace(o.packages)
	if len(p) > 0 {
		selected = strings.Split(p, ",")
	}
	return selected
}


func showField(fda fieldDefinitionArray) {
	for _, b := range fda {
		fmt.Printf("name: %s\n", b.Name)
		for _, field := range b.Fields {
			fmt.Printf("field: %s\n", field.Name)
		}
	}
}

func generateDocs() error {
	return nil
}

func generateFields(fromDir string, toDir string) error {
	//
	// gather all the fields files in the package
	fromFiles, err := gatherFieldsFiles(fromDir)
	if err != nil {
		log.Fatal(errors.Wrapf(err, "could not find any files in [%s]", fromDir))
	}

	// loop through each file and gather all the fields
	for _, f := range fromFiles {
		var filter allTheThings

		// gather all the fields
		fda, err := getAllFields(filepath.Join(fromDir, f))
		if err != nil {
			continue
		}

		filter.Fields = captureSortedFields(fda)

		// if the filtering file does not exist, dump the current list to the filtering file
		// does the file exist?
		filterFile := filepath.Join(toDir, f)

		if _, err := os.Stat(filterFile); err == nil {
			// read in the existing file
			existing,_ := readInFilterFile(filterFile)

			// copy over the definitions
			filter.Definitions = existing.Definitions

			// copy over new fields into the existing map
			filter.Fields = join(existing.Fields, filter.Fields)

		} else {
			fmt.Printf("File [%s] does not exist\n", filterFile)
			// make sure the directory exists
			dir := filepath.Dir(filterFile)
			if _, err := os.Stat(dir); errors.Is(err, os.ErrNotExist) {
				err := os.MkdirAll(dir, os.ModePerm)

				if err != nil {
					log.Println(err)
				}
			}

		}

		blob, _ := yaml.Marshal(&filter)
		ioutil.WriteFile(filterFile, blob, 0777)

	}

	return nil
}

func main() {
	var options generateOptions
	flag.StringVar(&options.filteringDir, "filtering", "./custom_documentation", "Path to the directory holding the field filters")
	flag.StringVar(&options.packages, "packages", "endpoint", "Packages selected for generating docs")
	flag.StringVar(&options.packagesSourceDir, "sourceDir", "./package", "Path to the packages directory")
	flag.BoolVar(&options.doGenerate, "generate", false, "Should we generate fields and docs?")
	flag.Parse()

	err := options.validate()
	if err != nil {
		log.Fatal(errors.Wrap(err, "command options validation failed"))
	}

	if options.doGenerate {
		fmt.Printf("we are generating!\n")
		// generate the fields that differ from what we have
		err = generateFields(options.packagesSourceDir, options.filteringDir)

		// generate the docs from the fields, etc
	}

}

