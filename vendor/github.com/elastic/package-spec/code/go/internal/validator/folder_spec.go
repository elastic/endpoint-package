package validator

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"path"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/pkg/errors"
	"gopkg.in/yaml.v3"
)

const (
	itemTypeFile   = "file"
	itemTypeFolder = "folder"

	visibilityTypePublic  = "public"
	visibilityTypePrivate = "private"
)

type folderSpec struct {
	fs       http.FileSystem
	specPath string
	commonSpec
}

func newFolderSpec(fs http.FileSystem, specPath string) (*folderSpec, error) {
	specFile, err := fs.Open(specPath)
	if err != nil {
		return nil, errors.Wrap(err, "could not open folder specification file")
	}
	defer specFile.Close()

	data, err := ioutil.ReadAll(specFile)
	if err != nil {
		return nil, errors.Wrap(err, "could not read folder specification file")
	}

	var wrapper struct {
		Spec commonSpec `yaml:"spec"`
	}

	if err := yaml.Unmarshal(data, &wrapper); err != nil {
		return nil, errors.Wrap(err, "could not parse folder specification file")
	}

	spec := folderSpec{
		fs:         fs,
		specPath:   specPath,
		commonSpec: wrapper.Spec,
	}

	err = setDefaultValues(&spec.commonSpec)
	if err != nil {
		return nil, errors.Wrap(err, "could not set default values")
	}
	return &spec, nil
}

func (s *folderSpec) validate(packageName string, folderPath string) ValidationErrors {
	var errs ValidationErrors
	files, err := ioutil.ReadDir(folderPath)
	if err != nil {
		errs = append(errs, errors.Wrapf(err, "could not read folder [%s]", folderPath))
		return errs
	}

	for _, file := range files {
		fileName := file.Name()
		itemSpec, err := s.findItemSpec(packageName, fileName)
		if err != nil {
			errs = append(errs, err)
			continue
		}

		if itemSpec == nil && s.AdditionalContents {
			// No spec found for current folder item but we do allow additional contents in folder.
			continue
		}

		if itemSpec == nil && !s.AdditionalContents {
			// No spec found for current folder item and we do not allow additional contents in folder.
			errs = append(errs, fmt.Errorf("item [%s] is not allowed in folder [%s]", fileName, folderPath))
			continue
		}

		if itemSpec != nil && itemSpec.Visibility != visibilityTypePrivate && itemSpec.Visibility != visibilityTypePublic {
			errs = append(errs, fmt.Errorf("item [%s] visibility is expected to be private or public, not [%s]", fileName, itemSpec.Visibility))
			continue
		}

		if file.IsDir() {
			if !itemSpec.isSameType(file) {
				errs = append(errs, fmt.Errorf("[%s] is a folder but is expected to be a file", fileName))
				continue
			}

			if itemSpec.Ref == "" && itemSpec.Contents == nil {
				// No recursive validation needed
				continue
			}

			var subFolderSpec *folderSpec
			if itemSpec.Ref != "" {
				subFolderSpecPath := path.Join(filepath.Dir(s.specPath), itemSpec.Ref)
				subFolderSpec, err = newFolderSpec(s.fs, subFolderSpecPath)
				if err != nil {
					errs = append(errs, err)
					continue
				}
			} else if itemSpec.Contents != nil {
				subFolderSpec = &folderSpec{
					fs:       s.fs,
					specPath: s.specPath,
					commonSpec: commonSpec{
						AdditionalContents: itemSpec.AdditionalContents,
						Contents:           itemSpec.Contents,
					},
				}
			}

			subFolderPath := path.Join(folderPath, fileName)
			subErrs := subFolderSpec.validate(packageName, subFolderPath)
			if len(subErrs) > 0 {
				errs = append(errs, subErrs...)
			}

		} else {
			if !itemSpec.isSameType(file) {
				errs = append(errs, fmt.Errorf("[%s] is a file but is expected to be a folder", fileName))
				continue
			}

			itemPath := filepath.Join(folderPath, file.Name())
			itemValidationErrs := itemSpec.validate(s.fs, s.specPath, itemPath)
			if itemValidationErrs != nil {
				for _, ive := range itemValidationErrs {
					errs = append(errs, errors.Wrapf(ive, "file \"%s\" is invalid", itemPath))
				}
			}
		}
	}

	// validate that required items in spec are all accounted for
	for _, itemSpec := range s.Contents {
		if !itemSpec.Required {
			continue
		}

		fileFound, err := itemSpec.matchingFileExists(files)
		if err != nil {
			errs = append(errs, err)
			continue
		}

		if !fileFound {
			var err error
			if itemSpec.Name != "" {
				err = fmt.Errorf("expecting to find [%s] %s in folder [%s]", itemSpec.Name, itemSpec.ItemType, folderPath)
			} else if itemSpec.Pattern != "" {
				err = fmt.Errorf("expecting to find %s matching pattern [%s] in folder [%s]", itemSpec.ItemType, itemSpec.Pattern, folderPath)
			}
			errs = append(errs, err)
		}
	}
	return errs
}

func (s *folderSpec) findItemSpec(packageName string, folderItemName string) (*folderItemSpec, error) {
	for _, itemSpec := range s.Contents {
		if itemSpec.Name != "" && itemSpec.Name == folderItemName {
			return &itemSpec, nil
		}
		if itemSpec.Pattern != "" {
			isMatch, err := regexp.MatchString(strings.ReplaceAll(itemSpec.Pattern, "{PACKAGE_NAME}", packageName), folderItemName)
			if err != nil {
				return nil, errors.Wrap(err, "invalid folder item spec pattern")
			}
			if isMatch {
				return &itemSpec, nil
			}
		}
	}

	// No item spec found
	return nil, nil
}