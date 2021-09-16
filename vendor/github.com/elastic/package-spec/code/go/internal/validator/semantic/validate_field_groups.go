// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package semantic

import (
	"fmt"
	"gopkg.in/yaml.v3"
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/pkg/errors"

	ve "github.com/elastic/package-spec/code/go/internal/errors"
)

type fields []field

type field struct {
	Name       string `yaml:"name"`
	Type       string `yaml:"type"`
	Unit       string `yaml:"unit"`
	MetricType string `yaml:"metric_type"`

	Fields fields `yaml:"fields"`
}

// ValidateFieldGroups verifies if field groups don't have units and metric types defined.
func ValidateFieldGroups(pkgRoot string) ve.ValidationErrors {
	fieldsFiles, err := listFieldsFiles(pkgRoot)
	if err != nil {
		return ve.ValidationErrors{errors.Wrapf(err, "can't list fields files")}
	}

	var vErrs ve.ValidationErrors
	for _, fieldsFile := range fieldsFiles {
		unmarshaled, err := unmarshalFields(fieldsFile)
		if err != nil {
			vErrs = append(vErrs, errors.Wrap(err, "can't unmarshal fields"))
		}

		for _, u := range unmarshaled {
			errs := validateFieldUnit(u)
			if len(errs) > 0 {
				vErrs = append(vErrs, errs...)
			}
		}
	}
	return vErrs
}

func listFieldsFiles(pkgRoot string) ([]string, error) {
	var fieldsFiles []string

	dataStreamDir := filepath.Join(pkgRoot, "data_stream")
	dataStreams, err := ioutil.ReadDir(dataStreamDir)
	if errors.Is(err, os.ErrNotExist) {
		return fieldsFiles, nil
	}
	if err != nil {
		return nil, errors.Wrap(err, "can't list data streams directory")
	}

	for _, dataStream := range dataStreams {
		fieldsDir := filepath.Join(dataStreamDir, dataStream.Name(), "fields")
		fs, err := ioutil.ReadDir(fieldsDir)
		if errors.Is(err, os.ErrNotExist) {
			continue
		}
		if err != nil {
			return nil, errors.Wrapf(err, "can't list fields directory (path: %s)", fieldsDir)
		}

		for _, f := range fs {
			fieldsFiles = append(fieldsFiles, filepath.Join(fieldsDir, f.Name()))
		}
	}

	return fieldsFiles, nil
}

func unmarshalFields(fieldsPath string) (fields, error) {
	content, err := ioutil.ReadFile(fieldsPath)
	if err != nil {
		return nil, errors.Wrapf(err, "can't read file (path: %s)", fieldsPath)
	}

	var f fields
	err = yaml.Unmarshal(content, &f)
	if err != nil {
		return nil, errors.Wrapf(err, "yaml.Unmarshal failed (path: %s)", fieldsPath)
	}
	return f, nil
}

func validateFieldUnit(f field) ve.ValidationErrors {
	if f.Type == "group" && f.Unit != "" {
		return ve.ValidationErrors{fmt.Errorf(`field "%s" can't have unit property'`, f.Name)}
	}

	if f.Type == "group" && f.MetricType != "" {
		return ve.ValidationErrors{fmt.Errorf(`field "%s" can't have metric type property'`, f.Name)}
	}

	var vErrs ve.ValidationErrors
	for _, aField := range f.Fields {
		errs := validateFieldUnit(aField)
		if len(errs) > 0 {
			vErrs = append(vErrs, errs...)
		}
	}
	return vErrs
}
