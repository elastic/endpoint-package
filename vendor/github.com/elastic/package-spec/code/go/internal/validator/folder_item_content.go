// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package validator

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"mime"

	"github.com/pkg/errors"
	"gopkg.in/yaml.v3"
)

func loadItemContent(itemPath, mediaType string) ([]byte, error) {
	itemData, err := ioutil.ReadFile(itemPath)
	if err != nil {
		return nil, errors.Wrap(err, "reading item file failed")
	}

	// There might be a situation in which we'd like to keep a directory without any file content under version control.
	// Usually it can be solved by adding the .empty file. There is no media type defined for this file.
	// It's expected of the file with media type defined not to be empty - the file can be marked as non-required.
	if len(itemData) == 0 && mediaType != "" {
		return nil, errors.New("file is empty, but media type is defined")
	}

	if mediaType == "" {
		return itemData, nil // no item's schema defined
	}

	basicMediaType, params, err := mime.ParseMediaType(mediaType)
	if err != nil {
		return nil, errors.Wrapf(err, "invalid media type (%s)", mediaType)
	}

	switch basicMediaType {
	case "application/x-yaml":
		// TODO Determine if special handling of `---` is required (issue: https://github.com/elastic/package-spec/pull/54)
		if v, _ := params["require-document-dashes"]; v == "true" && !bytes.HasPrefix(itemData, []byte("---\n")) {
			return nil, errors.New("document dashes are required (start the document with '---')")
		}

		var c interface{}
		err = yaml.Unmarshal(itemData, &c)
		if err != nil {
			return nil, errors.Wrapf(err, "unmarshalling YAML file failed (path: %s)", itemPath)
		}
		c = expandItemKey(c)

		itemData, err = json.Marshal(&c)
		if err != nil {
			return nil, errors.Wrapf(err, "converting YAML file to JSON failed (path: %s)", itemPath)
		}
	case "application/json": // no need to convert the item content
	case "text/markdown": // text/markdown can't be transformed into JSON format
	case "text/plain": // text/plain should be left as-is
	default:
		return nil, fmt.Errorf("unsupported media type (%s)", mediaType)
	}
	return itemData, nil
}

func expandItemKey(c interface{}) interface{} {
	if c == nil {
		return c
	}

	// c is an array
	if cArr, isArray := c.([]interface{}); isArray {
		var arr []interface{}
		for _, ca := range cArr {
			arr = append(arr, expandItemKey(ca))
		}
		return arr
	}

	// c is map[string]interface{}
	if cMap, isMapString := c.(map[string]interface{}); isMapString {
		expanded := MapStr{}
		for k, v := range cMap {
			ex := expandItemKey(v)
			_, err := expanded.Put(k, ex)
			if err != nil {
				panic(errors.Wrapf(err, "unexpected error while setting key value (key: %s)", k))
			}
		}
		return expanded
	}
	return c // c is something else, e.g. string, int, etc.
}
