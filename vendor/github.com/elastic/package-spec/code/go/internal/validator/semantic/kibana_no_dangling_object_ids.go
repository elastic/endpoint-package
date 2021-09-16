// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package semantic

import "github.com/elastic/package-spec/code/go/internal/errors"

// ValidateKibanaNoDanglingObjectIDs returns validation errors if there are any
// dangling references to Kibana objects in any Kibana object files. That is, it
// returns validation errors if a Kibana object file in the package references another
// Kibana object with ID i, but no Kibana object file for object ID i is found in the
// package.
func ValidateKibanaNoDanglingObjectIDs(pkgRoot string) errors.ValidationErrors {
	// TODO: will be implemented in follow up PR
	return nil
}
