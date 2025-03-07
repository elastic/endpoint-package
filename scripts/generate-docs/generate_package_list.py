import argparse
import json
import pathlib
import yaml
from pydantic import BaseModel
from typing import List, Optional, Any, Dict

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
        return cls(name=package_dir.name, fields=fields, sample_event=sample_event)

class PackageList(BaseModel):
    """
    PackageList is a list of packages
    """
    packages: List[Package] = []

    @classmethod
    def from_packages_dir(cls, packages_dir: pathlib.Path):
        """
        from_packages_dir creates a PackageList from a directory of packages

        Args:
            packages_dir: top level directory holding the packages
        """
        package_paths = list(packages_dir.glob("*"))
        packages = [Package.from_package_dir(package_path) for package_path in package_paths]
        return cls(packages=packages)


def resolve_packages_dir() -> pathlib.Path:
    """
    resolve_packages_dir returns the directory where the packages are stored relative to this file
    """
    this_file = pathlib.Path(__file__).resolve()
    root_dir = this_file.parents[2]
    return root_dir / "package" / "endpoint" / "data_stream"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump packages as JSON")
    parser.add_argument(
        "--packages-dir",
        default=resolve_packages_dir(),
        type=pathlib.Path,
        help="directory holding the packages",
    )
    parser.add_argument(
        "--output",
        default=pathlib.Path("packages.json"),
        type=pathlib.Path,
        help="output file",
    )
    args = parser.parse_args()

    #
    # Create the PackageList object and dump it to a file
    #
    package_list = PackageList.from_packages_dir(args.packages_dir)
    with open(args.output, "w") as f:
        #
        # Dump to json with indentation and exclude None values
        #
        f.write(package_list.model_dump_json(indent=4, exclude_none=True))
