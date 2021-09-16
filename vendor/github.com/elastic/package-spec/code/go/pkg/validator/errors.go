// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package validator

import (
	"github.com/elastic/package-spec/code/go/internal/errors"
)

// ValidationErrors is an Error that contains a iterable collection of validation error messages.
type ValidationErrors errors.ValidationErrors
