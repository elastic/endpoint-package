import json
import pathlib
import yaml
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict


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
        with yaml_path.open("r") as f:
            data = yaml.safe_load(f)
            return cls(**data, filepath=yaml_path)


class CustomDocList(BaseModel):
    """
    List of custom documentation for a package
    """
    map: Dict[str, CustomDocumentation]

    @classmethod
    def from_yaml(cls, yaml_dir: pathlib.Path) -> "CustomDocList":
        yaml_files = list(yaml_dir.rglob("*.yaml"))
        temp_map = {}
        for yaml_path in yaml_dir.rglob("*.yaml"):
            custom_doc = CustomDocumentation.from_yaml(yaml_path)
            temp_map[custom_doc.filepath.stem] = custom_doc

        return cls(map=temp_map)
