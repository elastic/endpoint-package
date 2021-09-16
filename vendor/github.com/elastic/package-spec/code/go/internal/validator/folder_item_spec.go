// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package validator

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"sync"

	"github.com/pkg/errors"
	"github.com/xeipuuv/gojsonschema"

	ve "github.com/elastic/package-spec/code/go/internal/errors"
	"github.com/elastic/package-spec/code/go/internal/validator/semantic"
	"github.com/elastic/package-spec/code/go/internal/yamlschema"
)

type folderItemSpec struct {
	Description       string   `yaml:"description"`
	ItemType          string   `yaml:"type"`
	ContentMediaType  string   `yaml:"contentMediaType"`
	ForbiddenPatterns []string `yaml:"forbiddenPatterns"`
	Name              string   `yaml:"name"`
	Pattern           string   `yaml:"pattern"`
	Required          bool     `yaml:"required"`
	Ref               string   `yaml:"$ref"`
	Visibility        string   `yaml:"visibility" default:"public"`
	commonSpec        `yaml:",inline"`
}

var formatCheckersMutex sync.Mutex

func (s *folderItemSpec) matchingFileExists(files []os.FileInfo) (bool, error) {
	if s.Name != "" {
		for _, file := range files {
			if file.Name() == s.Name {
				return s.isSameType(file), nil
			}
		}
	} else if s.Pattern != "" {
		for _, file := range files {
			isMatch, err := regexp.MatchString(s.Pattern, file.Name())
			if err != nil {
				return false, errors.Wrap(err, "invalid folder item spec pattern")
			}
			if isMatch {
				return s.isSameType(file), nil
			}
		}
	}

	return false, nil
}

func (s *folderItemSpec) isSameType(file os.FileInfo) bool {
	switch s.ItemType {
	case itemTypeFile:
		return !file.IsDir()
	case itemTypeFolder:
		return file.IsDir()
	}

	return false
}

func (s *folderItemSpec) validate(fs fs.FS, folderSpecPath string, itemPath string) ve.ValidationErrors {
	// loading item content
	itemData, err := loadItemContent(itemPath, s.ContentMediaType)
	if err != nil {
		return ve.ValidationErrors{err}
	}

	var schemaLoader gojsonschema.JSONLoader
	if s.Ref != "" {
		schemaPath := filepath.Join(filepath.Dir(folderSpecPath), s.Ref)
		schemaLoader = yamlschema.NewReferenceLoaderFileSystem("file:///"+schemaPath, fs)
	} else if s.Content != nil {
		schemaLoader = yamlschema.NewRawLoaderFileSystem(s.Content, fs)
	} else {
		return nil // item's schema is not defined
	}

	// validation with schema
	documentLoader := gojsonschema.NewBytesLoader(itemData)

	formatCheckersMutex.Lock()
	defer func() {
		semantic.UnloadRelativePathFormatChecker()
		semantic.UnloadDataStreamNameFormatChecker()
		formatCheckersMutex.Unlock()
	}()

	semantic.LoadRelativePathFormatChecker(filepath.Dir(itemPath))
	semantic.LoadDataStreamNameFormatChecker(filepath.Dir(itemPath))
	result, err := gojsonschema.Validate(schemaLoader, documentLoader)
	if err != nil {
		return ve.ValidationErrors{err}
	}

	if result.Valid() {
		return nil // item content is valid according to the loaded schema
	}

	var errs ve.ValidationErrors
	for _, re := range result.Errors() {
		errs = append(errs, fmt.Errorf("field %s: %s", re.Field(), adjustErrorDescription(re.Description())))
	}
	return errs
}
