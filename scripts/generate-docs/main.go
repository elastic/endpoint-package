// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package main

import (
	"flag"
	"log"
	"os"
	"strings"

	"github.com/pkg/errors"
)

type generateOptions struct {
	docTemplatesDir   string
	packages          string
	packagesSourceDir string
	customDocDir      string
}

func (o *generateOptions) validate() error {
	_, err := os.Stat(o.packagesSourceDir)
	if err != nil {
		return errors.Wrapf(err, "stat file failed for packages directory (path: %s)", o.packagesSourceDir)
	}

	_, err = os.Stat(o.docTemplatesDir)
	if err != nil {
		return errors.Wrapf(err, "stat file failed for doc templates (path: %s)", o.docTemplatesDir)
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

func main() {
	var options generateOptions
	flag.StringVar(&options.docTemplatesDir, "templates", "./doc_templates", "Path to the README templates directory")
	flag.StringVar(&options.packages, "packages", "endpoint", "Packages selected for generating docs")
	flag.StringVar(&options.packagesSourceDir, "sourceDir", "./package", "Path to the packages directory")
	flag.StringVar(&options.customDocDir, "customDocDir", "./custom_documentation", "Path to the custom_documentation directory (default: ./custom_documentation)")
	flag.Parse()

	err := options.validate()
	if err != nil {
		log.Fatal(errors.Wrap(err, "command options validation failed"))
	}

	err = generateDocs(options)
	if err != nil {
		log.Fatal(errors.Wrap(err, "generating docs failed"))
	}
}

func generateDocs(options generateOptions) error {
	packages, err := listPackages(options)
	if err != nil {
		return errors.Wrap(err, "listing packages failed")
	}

	for _, packageName := range packages {
		err = renderCustomDocumentation(options, packageName)
		if err != nil {
			return errors.Wrapf(err, "rendering custom documentation failed (packageName: %s)", packageName)
		}

		err = renderReadme(options, packageName)
		if err != nil {
			return errors.Wrapf(err, "rendering README file failed (packageName: %s)", packageName)
		}
	}
	return nil
}
