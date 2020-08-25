package validator

import (
	"errors"

	"github.com/elastic/package-spec/code/go/internal/validator"
)

// ValidateFromPath validates a package located at the given path against the
// appropriate specification and returns any errors.
func ValidateFromPath(packageRootPath string) error {
	pkg, err := validator.NewPackage(packageRootPath)
	if err != nil {
		return err
	}

	if pkg.SpecVersion == nil {
		return errors.New("could not determine specification version for package")
	}

	spec, err := validator.NewSpec(*pkg.SpecVersion)
	if err != nil {
		return err
	}

	if errs := spec.ValidatePackage(*pkg); errs != nil && len(errs) > 0 {
		return errs
	}

	return nil
}
