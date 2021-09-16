// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package pkgpath

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"

	"github.com/PaesslerAG/jsonpath"
	"github.com/joeshaw/multierror"
	"github.com/pkg/errors"
	"gopkg.in/yaml.v3"
)

// File represents a file in the package.
type File struct {
	path string
	os.FileInfo
}

// Files finds files for the given glob
func Files(glob string) ([]File, error) {
	paths, err := filepath.Glob(glob)
	if err != nil {
		return nil, err
	}

	var errs multierror.Errors
	var files = make([]File, 0)
	for _, path := range paths {
		info, err := os.Stat(path)
		if err != nil {
			errs = append(errs, err)
			continue
		}

		file := File{path, info}
		files = append(files, file)
	}

	return files, errs.Err()
}

// Values returns values within the file matching the given path. Paths
// should be expressed using JSONPath syntax. This method is only supported
// for YAML and JSON files.
func (f File) Values(path string) (interface{}, error) {
	fileName := f.Name()
	fileExt := strings.TrimLeft(filepath.Ext(fileName), ".")

	if fileExt != "json" && fileExt != "yaml" && fileExt != "yml" {
		return nil, fmt.Errorf("cannot extract values from file type = %s", fileExt)
	}

	contents, err := ioutil.ReadFile(f.path)
	if err != nil {
		return nil, errors.Wrap(err, "reading file content failed")
	}

	var v interface{}
	if fileExt == "yaml" || fileExt == "yml" {
		if err := yaml.Unmarshal(contents, &v); err != nil {
			return nil, errors.Wrapf(err, "unmarshalling YAML file failed (path: %s)", fileName)
		}
	} else if fileExt == "json" {
		if err := json.Unmarshal(contents, &v); err != nil {
			return nil, errors.Wrapf(err, "unmarshalling JSON file failed (path: %s)", fileName)
		}
	}

	return jsonpath.Get(path, v)
}

// Path returns the complete path to the file.
func (f File) Path() string {
	return f.path
}
