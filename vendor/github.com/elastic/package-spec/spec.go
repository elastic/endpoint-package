// Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
// or more contributor license agreements. Licensed under the Elastic License;
// you may not use this file except in compliance with the Elastic License.

package spec

import (
	"embed"
	"io/fs"
)

//go:embed versions/1 versions/1/_dev versions/1/data_stream/_dev
var content embed.FS

// FS returns an io/fs.FS for accessing the "package-spec/version" contents.
//
// All contents are rooted within the "versions" folder, and are addressed first by
// version, e.g. "1/spec.yml".
func FS() fs.FS {
	fs, err := fs.Sub(content, "versions")
	if err != nil {
		panic(err)
	}
	return fs
}
