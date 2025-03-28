import logging
import json
import pathlib
import yaml
from pydantic import BaseModel, RootModel
from typing import List, Optional, Any, Dict, Iterator

from ..paths import PACKAGES_DIR


#
# See any of the files at package/endpoint/data_stream/*/fields/fields.yaml for examples
# of the data these models parse
#

class MultiField(BaseModel):
    """
    fields can have a number of multi_fields
    """

    name: str
    type: str
    norms: Optional[bool] = None
    normalizer: Optional[str] = None
    ignore_above: Optional[int] = None
    default_field: Optional[bool] = None

    class Config:
        """
        this config setting ensures that the model will raise an error if any extra fields are present
        """

        extra = "forbid"


class Field(BaseModel):
    """
    Field field as defined in fields.yml
    """

    name: str
    title: Optional[str] = None
    default_field: Optional[bool] = None
    level: Optional[str] = None
    type: Optional[str] = None
    ignore_above: Optional[int] = None
    description: Optional[str] = None
    fields: Optional[List["Field"]] = None
    required: Optional[bool] = None
    group: Optional[int] = None
    multi_fields: Optional[List[MultiField]] = None
    example: Optional[Any] = None
    format: Optional[str] = None
    enabled: Optional[bool] = None
    doc_values: Optional[bool] = None
    index: Optional[bool] = None
    footnote: Optional[str] = None
    pattern: Optional[str] = None
    path: Optional[str] = None

    class Config:
        """
        this config setting ensures that the model will raise an error if any extra fields are present
        """

        extra = "forbid"


class Package(BaseModel):
    """
    A package consists of a name, a list of fields and an optional sample event
    """

    name: str
    fields: List[Field]
    sample_event: Optional[Dict[Any, Any]] = None
    filepath: Optional[pathlib.Path] = None

    @classmethod
    def from_package_dir(cls, package_dir: pathlib.Path):
        """
        takes a directory and returns a Package object
        - name is the name of the directory (package)
        - fields are read from fields/fields.yml
        - sample_event is read from sample_event.json if it exists

        Args:
            package_dir: directory holding the package data
        """
        logging.debug(f"Reading package from {package_dir}")
        if not package_dir.exists():
            raise ValueError(f"package directory {package_dir} does not exist")
        if not package_dir.is_dir():
            raise ValueError(f"package directory {package_dir} is not a directory")

        #
        # read fields from fields.yml and create Field objects
        #
        fields_path = package_dir / "fields" / "fields.yml"
        fields_data = yaml.safe_load(fields_path.read_text())
        fields = [Field(**field) for field in fields_data]

        #
        # read sample event if it exists
        #
        sample_event = None
        sample_event_path = package_dir / "sample_event.json"
        if sample_event_path.exists():
            sample_event = json.loads(sample_event_path.read_text())

        #
        # return the Package object
        #
        return cls(
            name=package_dir.name,
            fields=fields,
            sample_event=sample_event,
            filepath=fields_path,
        )


class PackageList(RootModel):
    """
    PackageList is a list of packages
    """

    root: List[Package] = []

    def __iter__(self) -> Iterator[Package]:
        return iter(self.root)

    def __getitem__(self, index) -> List[Package]:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

    def append(self, package: Package) -> None:
        self.root.append(package)

    @classmethod
    def from_files(cls, packages_dir: pathlib.Path = PACKAGES_DIR):
        """
        from_packages_dir creates a PackageList from a directory of packages

        Args:
            packages_dir: top level directory holding the packages
        """
        package_paths = list(packages_dir.glob("*"))
        packages = [
            Package.from_package_dir(package_path) for package_path in package_paths
        ]
        return cls(root=packages)
