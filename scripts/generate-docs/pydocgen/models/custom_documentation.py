import logging
import pathlib
import yaml
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Iterator, Dict

from ..paths import CUSTOM_DOCUMENTATION_DIR, DOCUMENTATION_OVERRIDE_PATH

class Overview(BaseModel):
    """
    Overview of the package
    """
    name: str
    description: str

class Filter(BaseModel):
    """
    Filter for the package
    """
    event_dataset: str = Field(..., alias="event.dataset")
    event_module: str = Field(..., alias="event.module")
    event_provider: Optional[str] = Field(None, alias="event.provider")
    host_os_type: Optional[str] = Field(None, alias="host.os.type")
    event_code: Optional[str] = Field(None, alias="event.code")
    event_action: Optional[List[str]] = Field(None, alias="event.action")

    @field_validator("event_action", mode="before")
    @classmethod
    def validate_tags(cls, value):
        if isinstance(value, str):
            # If input is a string, convert to a list with one item
            return [value]
        return value

    class Config:
        populate_by_name = True


class Identification(BaseModel):
    """
    Identification of the package
    """
    filter: Filter
    os: List[str]
    data_stream: str


class Fields(BaseModel):
    """
    Fields for the package
    """
    endpoint: List[str]


class CustomDocumentation(BaseModel):
    """
    Custom documentation for a package
    """
    overview: Overview
    identification: Identification
    fields: Fields
    filepath: pathlib.Path

    @classmethod
    def from_yaml(cls, yaml_path: pathlib.Path) -> "CustomDocumentation":
        logging.debug(f"Reading custom documentation from {yaml_path}")
        with yaml_path.open("r") as f:
            data = yaml.safe_load(f)
            return cls(**data, filepath=yaml_path)


class CustomDocumentationMap(BaseModel):
    """
    Map of custom documentation for a package
    """
    root: dict = {}

    def __getitem__(self, key) -> CustomDocumentation:
        return self.root[key]

    def __iter__(self) -> Iterator[CustomDocumentation]:
        return iter(self.root.values())

    def __len__(self) -> int:
        return len(self.root)

    def append(self, package: CustomDocumentation) -> None:
        self.root[package.overview.name] = package

    @classmethod
    def from_yaml(cls, yaml_dir: pathlib.Path) -> "CustomDocumentationMap":
        custom_docs = cls()
        for yaml_path in yaml_dir.rglob("*.yaml"):
            custom_doc = CustomDocumentation.from_yaml(yaml_path)
            custom_docs.append(custom_doc)

        return custom_docs


class CustomDocumentationList(BaseModel):
    """
    List of custom documentation for a package
    """
    root: List[CustomDocumentation] = []

    def __iter__(self) -> Iterator[CustomDocumentation]:
        return iter(self.root)

    def __getitem__(self, index) -> List[CustomDocumentation]:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)

    def append(self, package: CustomDocumentation) -> None:
        self.root.append(package)

    @classmethod
    def from_files(
        cls, yaml_dir: pathlib.Path = CUSTOM_DOCUMENTATION_DIR
    ) -> "CustomDocumentationList":
        custom_docs = []
        for yaml_path in yaml_dir.rglob("*.yaml"):
            custom_docs.append(CustomDocumentation.from_yaml(yaml_path))

        return cls(root=custom_docs)


#
# These models reprensent the data from custom_documentation/src/documentation_overrides.yaml
#
class OverrideBase(BaseModel):
    """
    Override for a field
    """
    description: Optional[str] = None
    example: Optional[str] = None
    type: Optional[str] = None

class OverrideMapping(BaseModel):
    """
    Map of overrides for a field
    """
    default: Optional[OverrideBase] = None
    os: Optional[Dict[str, OverrideBase]] = None
    event: Optional[Dict[str, OverrideBase]] = None

class DocumentationOverrideMap(BaseModel):
    """
    Map of documentation overrides for a field
    """
    root: dict = {}

    def __getitem__(self, key) -> OverrideMapping:
        return self.root[key]

    def __iter__(self) -> Iterator[OverrideMapping]:
        return iter(self.root.values())

    def __len__(self) -> int:
        return len(self.root)

    def items(self):
        return self.root.items()

    def append(self, name: str, om: OverrideMapping) -> None:
        self.root[name] = om

    @classmethod
    def from_yaml(
        cls, yaml_path: pathlib.Path = DOCUMENTATION_OVERRIDE_PATH
    ) -> "DocumentationOverrideMap":
        logging.debug(f"Reading documentation overrides from {yaml_path}")
        doc_overrides = cls()
        with yaml_path.open("r") as f:
            data = yaml.safe_load(f)
            for item in data:
                doc_overrides.append(item["name"], OverrideMapping(**item["overrides"]))
        return doc_overrides
