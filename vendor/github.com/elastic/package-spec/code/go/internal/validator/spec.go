package validator

import (
	"net/http"
	"path"
	"strconv"

	"github.com/Masterminds/semver/v3"
	"github.com/pkg/errors"
	"github.com/rakyll/statik/fs"

	// Loads package specs as an in-memory filesystem
	_ "github.com/elastic/package-spec/code/go/internal/spec"
)

// Spec represents a package specification
type Spec struct {
	version  semver.Version
	fs       http.FileSystem
	specPath string
}

// NewSpec creates a new Spec for the given version
func NewSpec(version semver.Version) (*Spec, error) {
	majorVersion := strconv.FormatUint(version.Major(), 10)

	bundle, err := fs.New()
	if err != nil {
		return nil, errors.Wrap(err, "could not load specifications")
	}

	specPath := "/" + majorVersion
	if _, err := bundle.Open(specPath); err != nil {
		return nil, errors.Wrapf(err, "could not load specification for version [%s]", version.String())
	}

	s := Spec{
		version,
		bundle,
		specPath,
	}

	return &s, nil
}

// ValidatePackage validates the given Package against the Spec
func (s Spec) ValidatePackage(pkg Package) ValidationErrors {
	var errs ValidationErrors

	rootSpecPath := path.Join(s.specPath, "spec.yml")
	rootSpec, err := newFolderSpec(s.fs, rootSpecPath)
	if err != nil {
		errs = append(errs, errors.Wrap(err, "could not read root folder spec file"))
		return errs
	}

	return rootSpec.validate(pkg.Name, pkg.RootPath)
}
