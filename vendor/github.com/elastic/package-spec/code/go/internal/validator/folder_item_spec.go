package validator

import (
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"sync"

	"github.com/pkg/errors"
	"github.com/xeipuuv/gojsonschema"

	"github.com/elastic/package-spec/code/go/internal/yamlschema"
)

const relativePathFormat = "relative-path"

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

func (s *folderItemSpec) validate(fs http.FileSystem, folderSpecPath string, itemPath string) ValidationErrors {
	// loading item content
	itemData, err := loadItemContent(itemPath, s.ContentMediaType)
	if err != nil {
		return ValidationErrors{err}
	}

	var schemaLoader gojsonschema.JSONLoader
	if s.Ref != "" {
		schemaPath := filepath.Join(filepath.Dir(folderSpecPath), s.Ref)
		schemaLoader = yamlschema.NewReferenceLoaderFileSystem("file://"+schemaPath, fs)
	} else if s.Content != nil {
		schemaLoader = yamlschema.NewRawLoaderFileSystem(s.Content, fs)
	} else {
		return nil // item's schema is not defined
	}

	// validation with schema
	documentLoader := gojsonschema.NewBytesLoader(itemData)

	formatCheckersMutex.Lock()
	defer func() {
		unloadRelativePathFormatChecker()
		formatCheckersMutex.Unlock()
	}()

	loadRelativePathFormatChecker(filepath.Dir(itemPath))
	result, err := gojsonschema.Validate(schemaLoader, documentLoader)
	if err != nil {
		return ValidationErrors{err}
	}

	if result.Valid() {
		return nil // item content is valid according to the loaded schema
	}

	var errs ValidationErrors
	for _, re := range result.Errors() {
		errs = append(errs, fmt.Errorf("field %s: %s", re.Field(), adjustErrorDescription(re.Description())))
	}
	return errs
}

func loadRelativePathFormatChecker(currentPath string) {
	gojsonschema.FormatCheckers.Add(relativePathFormat, RelativePathChecker{
		currentPath: currentPath,
	})
}

func unloadRelativePathFormatChecker() {
	gojsonschema.FormatCheckers.Remove(relativePathFormat)
}
