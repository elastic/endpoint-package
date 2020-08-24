// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

// +build tools

/**
 * This file is a dummy file that will never be compiled. It just indicates that we're using
 * the elastic-package tool. This is necessary so we can vendor it. If additional external go tools
 * are needed they can be added in the import here.
 *
 * For more information see: https://github.com/go-modules-by-example/index/blob/master/010_tools/README.md
 */
package tools

import (
	_ "github.com/elastic/elastic-package"
)
