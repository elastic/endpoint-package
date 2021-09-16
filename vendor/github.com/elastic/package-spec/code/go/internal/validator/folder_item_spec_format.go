// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package validator

import (
	"os"
	"path/filepath"
)

// RelativePathChecker is responsible for checking presence of the file path
type RelativePathChecker struct {
	currentPath string
}

// IsFormat method checks if the path exists.
func (r RelativePathChecker) IsFormat(input interface{}) bool {
	asString, ok := input.(string)
	if !ok {
		return false
	}

	path := filepath.Join(r.currentPath, asString)
	_, err := os.Stat(path)
	if err != nil {
		return false
	}
	return true
}