package validator

import (
	"encoding/json"
	"fmt"
	"github.com/elastic/package-spec/code/go/internal/yamlschema"
	"github.com/xeipuuv/gojsonschema"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"regexp"

	"github.com/pkg/errors"
	"gopkg.in/yaml.v3"
)

type folderItemSpec struct {
	Description      string `yaml:"description"`
	ItemType         string `yaml:"type"`
	ContentMediaType string `yaml:"contentMediaType"`
	Name             string `yaml:"name"`
	Pattern          string `yaml:"pattern"`
	Required         bool   `yaml:"required"`
	Ref              string `yaml:"$ref"`
	Visibility       string `yaml:"visibility" default:"public"`
	commonSpec       `yaml:",inline"`
}

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
	var schemaLoader gojsonschema.JSONLoader
	if s.Ref != "" {
		schemaPath := filepath.Join(filepath.Dir(folderSpecPath), s.Ref)
		schemaLoader = yamlschema.NewReferenceLoaderFileSystem("file://"+schemaPath, fs)
	} else if s.Content != nil {
		schemaLoader = yamlschema.NewRawLoaderFileSystem(s.Content, fs)
	} else {
		return nil // item's schema is not defined
	}

	// loading item content
	itemData, err := loadItemContent(itemPath, s.ContentMediaType)
	if err != nil {
		return ValidationErrors{errors.Wrapf(err, "loading item content failed (path %s)", itemPath)}
	}

	// validation with schema
	documentLoader := gojsonschema.NewBytesLoader(itemData)
	result, err := gojsonschema.Validate(schemaLoader, documentLoader)
	if err != nil {
		return ValidationErrors{err}
	}

	if result.Valid() {
		return nil // item content is valid according to the loaded schema
	}

	var errs ValidationErrors
	for _, re := range result.Errors() {
		errs = append(errs, fmt.Errorf("field %s: %s", re.Field(), re.Description()))
	}
	return errs
}

func loadItemContent(itemPath, mediaType string) ([]byte, error) {
	itemData, err := ioutil.ReadFile(itemPath)
	if err != nil {
		return nil, errors.Wrap(err, "reading item file failed")
	}

	if len(itemData) == 0 {
		return nil, errors.New("file is empty")
	}

	switch mediaType {
	case "application/x-yaml":
		var c interface{}
		err = yaml.Unmarshal(itemData, &c)
		if err != nil {
			return nil, errors.Wrapf(err, "unmarshalling YAML file failed (path: %s)", itemPath)
		}

		itemData, err = json.Marshal(&c)
		if err != nil {
			return nil, errors.Wrapf(err, "converting YAML file to JSON failed (path: %s)", itemPath)
		}
	case "application/json": // no need to convert the item content
	default:
		return nil, fmt.Errorf("unsupported media type (%s)", mediaType)
	}
	return itemData, nil
}
