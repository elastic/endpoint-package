import argparse
import pathlib
import traceback
import sys
from unittest import result
from .models import PackageList
from .custom_documentation import CustomDocList
from .markdown import generate_package_list_markdown
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

def resolve_packages_dir() -> pathlib.Path:
    """
    resolve_packages_dir returns the directory where the packages are stored relative to this file
    """
    this_file = pathlib.Path(__file__).resolve()
    root_dir = this_file.parents[3]
    return root_dir / "package" / "endpoint" / "data_stream"

def resolve_custom_documentation_dir() -> pathlib.Path:
    """
    resolve_custom_documentation_dir returns the directory where the custom documentation is stored relative to this file
    """
    this_file = pathlib.Path(__file__).resolve()
    root_dir = this_file.parents[3]
    return root_dir / "custom_documentation" / "src" / "endpoint" / "data_stream"

def main():
    parser = argparse.ArgumentParser(description="Dump packages as JSON")
    parser.add_argument(
        "--packages-dir",
        default=resolve_packages_dir(),
        type=pathlib.Path,
        help="directory holding the packages",
    )
    parser.add_argument(
        "--output",
        default=pathlib.Path().resolve() / "output",
        type=pathlib.Path,
        help="output directory",
    )
    args = parser.parse_args()

    # #
    # # Validate the output directory
    # #
    # if args.output.exists():
    #     raise FileExistsError(
    #         f"output directory {args.output} already exists, please remove it or specify a different directory"
    #     )
    # args.output.mkdir(parents=True)

    #
    # Create the PackageList object and dump it to a file
    #
    package_list = PackageList.from_packages_dir(args.packages_dir)

    fields = {}

    class DocumentField(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(sa_column_kwargs={"unique": True})
        description: str

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    def add_to_db(field: DocumentField, session: Session):
        existing_field = session.exec(select(DocumentField).where(DocumentField.name == field.name)).first()
        if existing_field:
            if existing_field.description != field.description:
                raise ValueError(
                    f"Field {field.name} already exists with different description"
                )
        else:
            session.add(field)
            session.commit()

    with Session(engine) as session:
        for package in package_list:
            for field in package.fields:
                if field.fields:
                    for sub_field in field.fields:
                        name = f"{field.name}.{sub_field.name}"
                        add_to_db(DocumentField(name=name, description=sub_field.description), session)
                else:
                    add_to_db(DocumentField(name=field.name, description=field.description), session)

    statement = select(DocumentField).where(
        DocumentField.name
        == "Endpoint.metrics.system_impact.threat_intelligence_events.week_ms"
    )
    results = session.exec(statement)
    for result in results:
        print(result)

    # json_path = args.output / "packages.json"
    # with json_path.open("w") as f:
    #     # Dump to json with indentation and exclude None values
    #     f.write(package_list.model_dump_json(indent=4, exclude_none=True))

    # #
    # # Generate markdown files
    # #
    # generate_package_list_markdown(package_list, args.output)

    # custom_doc_list = CustomDocList.from_yaml(resolve_custom_documentation_dir())
    # import pdb; pdb.set_trace()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
