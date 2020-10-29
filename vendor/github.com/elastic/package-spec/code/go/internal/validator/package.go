package validator

import (
	"fmt"
	"io/ioutil"
	"os"
	"path"

	"github.com/Masterminds/semver/v3"
	"github.com/pkg/errors"
	"gopkg.in/yaml.v3"
)

// Package represents an Elastic Package Registry package
type Package struct {
	Name        string
	SpecVersion *semver.Version
	RootPath    string
}

// NewPackage creates a new Package from a path to the package's root folder
func NewPackage(pkgRootPath string) (*Package, error) {
	info, err := os.Stat(pkgRootPath)
	if os.IsNotExist(err) {
		return nil, errors.Wrapf(err, "no package found at path [%v]", pkgRootPath)
	}

	if !info.IsDir() {
		return nil, fmt.Errorf("no package folder found at path [%v]", pkgRootPath)
	}

	pkgManifestPath := path.Join(pkgRootPath, "manifest.yml")
	info, err = os.Stat(pkgManifestPath)
	if os.IsNotExist(err) {
		return nil, errors.Wrapf(err, "no package manifest file found at path [%v]", pkgManifestPath)
	}

	data, err := ioutil.ReadFile(pkgManifestPath)
	if err != nil {
		return nil, fmt.Errorf("could not read package manifest file [%v]", pkgManifestPath)
	}

	var manifest struct {
		Name        string `yaml:"name"`
		SpecVersion string `yaml:"format_version"`
	}
	if err := yaml.Unmarshal(data, &manifest); err != nil {
		return nil, errors.Wrapf(err, "could not parse package manifest file [%v]", pkgManifestPath)
	}

	specVersion, err := semver.NewVersion(manifest.SpecVersion)
	if err != nil {
		return nil, errors.Wrapf(err, "could not read specification version from package manifest file [%v]", pkgManifestPath)
	}

	// Instantiate Package object and return it
	p := Package{
		Name:        manifest.Name,
		RootPath:    pkgRootPath,
		SpecVersion: specVersion,
	}

	return &p, nil
}
