import csv
import hashlib
import logging
import os
import pathlib
from typing import List, TextIO

from sqlmodel import Session, select

from .models.custom_documentation import OsNameList
from .database import OverrideQueryResult, PackageField, getDatabase
from .models import CustomDocumentationList, Filter


def quote_markdown_string(s: str) -> str:
    """
    quote_markdown_string prepends each line of a string with a '>' character
    Args:
        s: string to quote

    Returns:
        quoted string
    """
    return "\n".join(f"> {line}" for line in s.splitlines())


def generate_random_sha256() -> str:
    """
    generate_random_sha256 generates a random SHA256 hash for use in example fields

    Returns:
        random SHA256 hash
    """
    return hashlib.sha256(os.urandom(32)).hexdigest()


class FieldMetadata:
    """
    FieldMetadata contains all the information necessary to generate markdown for a field
    it queries the package field database for ECS metadata and the overrides database
    for endpoint-specific metadata. It also generates a random SHA256 hash if the field is a
    SHA256 hash and no example is provided.f
    """

    def __init__(
        self, field: str, session: Session, event_name: str, os_names: OsNameList
    ) -> None:
        """
        __init__ queries the database for ECS metadata and endpoint-specific metadata.  Also
        generates a random SHA256 hash if the field is a SHA256 hash and no example is provided.

        Args:
            field: field name
            session: active sqlmodel session for querying the database
            event_name: name of the event
            os_name: os name (e.g., "windows", "linux", "macos")
        """
        self.field = field
        self.event_name = event_name
        self.os_names = os_names

        self.endpoint_description: str | None = None
        self.endpoint_example: str | None = None
        self.endpoint_type: str | None = None
        self.ecs_description: str | None = None
        self.ecs_example: str | None = None
        self.ecs_type: str | None = None

        self._populate_ecs_metadata(session)
        self._populate_endpoint_metadata(session)

        if not self.ecs_example and self.field.endswith(".sha256"):
            # If the field is a SHA256 hash, generate a random example if none is provided
            self.ecs_example = generate_random_sha256()

    def _populate_ecs_metadata(self, session: Session) -> None:
        """
        _populate_ecs_metadata populates the ECS metadata for a field
        based on the package field database

        Args:
            session: SQLAlchemy session
        """
        package_field: PackageField | None = session.exec(
            select(PackageField).where(PackageField.name == self.field)
        ).first()
        if package_field:
            #
            # The package field description may contain newlines, so we replace them with spaces
            #
            self.ecs_description = package_field.description
            self.ecs_example = package_field.example
            self.ecs_type = package_field.type

    def _populate_endpoint_metadata(self, session: Session) -> None:
        """
        _populate_endpoint_metadata populates the endpoint metadata for a field
        based on the overrides database

        Args:
            session: SQLAlchemy session
            field: field name
            event_name: event name
            os_name: OS name
        """
        result = OverrideQueryResult(
            session, self.field, self.event_name, self.os_names
        )
        if result.description:
            self.endpoint_description = result.description
        if result.example:
            self.endpoint_example = result.example
        if result.type:
            self.endpoint_type = result.type

    def has_data(self) -> bool:
        """
        has_data checks if the metadata has any data populated

        Returns:
            True if any metadata is populated, False otherwise
        """
        return any(
            [
                self.ecs_description,
                self.ecs_example,
                self.ecs_type,
                self.endpoint_description,
                self.endpoint_example,
                self.endpoint_type,
            ]
        )

    def missing_data(self) -> bool:
        """
        missing_data checks if the metadata is missing any data

        Returns:
            True if any metadata is missing, False otherwise
        """
        return not all(
            [
                self.ecs_description,
                self.ecs_example,
                self.ecs_type,
                self.endpoint_description,
                self.endpoint_example,
                self.endpoint_type,
            ]
        )

    def write_markdown(self, f: TextIO) -> None:
        """
        write_markdown writes the field metadata to a markdown file
        Args:
            f: file object to write to
        """
        f.write(f"### `{self.field}`\n\n")
        if not self.has_data():
            f.write("No description or example found\n\n")
            f.write("<br>\n\n")
            return

        if self.ecs_description:
            f.write("**ECS Description**\n\n")
            f.write(f"{quote_markdown_string(self.ecs_description)}\n\n")
        if self.endpoint_description:
            f.write("**Extended Description**\n\n")
            f.write(f"{quote_markdown_string(self.endpoint_description)}\n\n")
        if self.endpoint_example:
            f.write("**Example**\n\n")
            f.write(f"{quote_markdown_string(self.endpoint_example)}\n\n")
        elif self.ecs_example:
            f.write("**Example**\n\n")
            f.write(f"{quote_markdown_string(self.ecs_example)}\n\n")
        if self.endpoint_type:
            f.write("**Type**\n\n")
            f.write(f"{quote_markdown_string(self.endpoint_type)}\n\n")
        elif self.ecs_type:
            f.write("**Type**\n\n")
            f.write(f"{quote_markdown_string(self.ecs_type)}\n\n")
        f.write("<br>\n\n")


class MetadataCsvWriter:
    """
    This class will write a CSV file that contains fields
    that are missing either a description or an example. This
    can be imported into a spreadsheet to track missing documentation
    """

    FIELD_NAME = "Field Name"
    FIELD_EVENT_NAME = "Event Name"
    FIELD_HAS_ECS_DESCRIPTION = "Has ECS Description"
    FIELD_HAS_ECS_EXAMPLE = "Has ECS Example"
    FIELD_HAS_ECS_TYPE = "Has ECS Type"
    FIELD_HAS_ENDPOINT_DESCRIPTION = "Has Endpoint Description"
    FIELD_HAS_ENDPOINT_EXAMPLE = "Has Endpoint Example"

    def __init__(self, csv_path: pathlib.Path):

        self.csv_path = csv_path
        self.fields = [
            self.FIELD_NAME,
            self.FIELD_EVENT_NAME,
            self.FIELD_HAS_ECS_DESCRIPTION,
            self.FIELD_HAS_ECS_EXAMPLE,
            self.FIELD_HAS_ECS_TYPE,
            self.FIELD_HAS_ENDPOINT_DESCRIPTION,
            self.FIELD_HAS_ENDPOINT_EXAMPLE,
        ]
        self.rows = []

    def add_row(self, field: FieldMetadata):
        """
        add_row adds a row to the CSV output

        Args:
            field: FieldMetadata object containing the field information
        """
        self.rows.append(
            {
                self.FIELD_NAME: field.field,
                self.FIELD_EVENT_NAME: field.event_name,
                self.FIELD_HAS_ECS_DESCRIPTION: bool(field.ecs_description),
                self.FIELD_HAS_ECS_EXAMPLE: bool(field.ecs_example),
                self.FIELD_HAS_ECS_TYPE: bool(field.ecs_type),
                self.FIELD_HAS_ENDPOINT_DESCRIPTION: bool(field.endpoint_description),
                self.FIELD_HAS_ENDPOINT_EXAMPLE: bool(field.endpoint_example),
            }
        )

    def write_csv(self):
        """
        write_csv writes the collected rows to a CSV file
        """
        logging.debug(f"Generating CSV output at {self.csv_path}")
        with self.csv_path.open("w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)


def generate_custom_documentation_markdown(
    db_path: pathlib.Path,
    output_dir: pathlib.Path,
    csv_path: pathlib.Path | None = None,
):
    """
    Generate markdown files for custom documentation
    """

    def get_output_filepath(src_path: pathlib.Path) -> pathlib.Path:
        """
        get_output_filepath determines the output filename for writing markdown, based
        on the source path of the package

        Args:
            src_path: yaml file path

        Returns:
            output filepath
        """
        parts = src_path.parts
        index = parts.index("data_stream")
        output_filename = output_dir
        for part in parts[index + 1 : -1]:
            output_filename = output_filename / part
        return output_filename / parts[-1].replace(".yaml", ".md")

    def get_formatted_os_name(os: str) -> str:
        """
        get_formatted_os_name os names in the defintions are always lowercase, this function will
        return the correct case for the os name

        Args:
            os: os name

        Returns:
            _description_
        """
        match os:
            case "windows":
                return "Windows"
            case "linux":
                return "Linux"
            case "macos":
                return "macOS"
            case _:
                raise ValueError(
                    f"Unknown OS name: {os}. Please add it to the get_formatted_os_name function."
                )

    def get_formatted_os_string(os_list: OsNameList) -> str:
        """
        get_formatted_os_string some documents have multiple os's, this function will format them
        correctly for the markdown output

        Args:
            os_list: list of os names

        Returns:
            formatted os string
        """
        return ", ".join(get_formatted_os_name(os) for os in os_list)

    def get_kql_query_string(filter: Filter) -> str:
        """
        get_kql_query_string generates a KQL query string from a Filter object

        Args:
            filter: Filter object from the custom documentation

        Returns:
            KQL query string
        """
        queries = []
        for field, metadata in Filter.model_fields.items():
            field_name = metadata.alias if metadata.alias else field
            if field in filter.dict():
                field_value = filter.dict()[field]
                if not field_value:
                    continue
                if isinstance(field_value, list):
                    if len(field_value) == 1:
                        field_value = f"{field_value[0]}"
                    else:
                        field_value = '" or "'.join(field_value)
                queries.append(f'{field_name} : "{field_value}"')
        return " and ".join(queries)

    #
    # Function Begin
    #

    # Create or get the populated database
    engine = getDatabase(db_path)

    # Get the custom documentation
    custom_docs = CustomDocumentationList.from_files()

    csv_writer: MetadataCsvWriter | None = None
    if csv_path:
        csv_writer = MetadataCsvWriter(csv_path)

    # Generate markdown for each custom document
    with Session(engine) as session:
        for custom_doc in custom_docs:

            # Get the output filename and create the parent directories
            output_filename = get_output_filepath(custom_doc.filepath)
            output_filename.parent.mkdir(parents=True, exist_ok=True)

            # Write the markdown file
            with output_filename.open("w") as f:
                f.write(f"# {custom_doc.overview.name}\n\n")

                f.write(f"## Description\n\n")
                f.write(f"{custom_doc.overview.description}\n\n")

                f.write("## Overview\n\n")
                f.write("<table>\n")
                f.write("<tr>\n")
                f.write("<td><strong>OS</strong></td>\n")
                f.write(
                    f"<td>{get_formatted_os_string(custom_doc.identification.os)}</td>\n"
                )
                f.write("</tr>\n")
                f.write("<tr>\n")
                f.write(f"<td><strong>Data Stream</strong></td>\n")
                f.write(f"<td>{custom_doc.identification.data_stream}</td>\n")
                f.write("</tr>\n")
                f.write("<tr>\n")
                f.write(f"<td><strong>KQL Query</strong></td>\n")
                f.write(
                    f"<td><code>{get_kql_query_string(custom_doc.identification.filter)}</code></td>\n"
                )
                f.write("</tr>\n")
                f.write("</table>\n\n")
                f.write(f"## Fields\n\n")

                #
                # Write markdown for the individual Fields
                #
                for field in custom_doc.fields.endpoint:
                    field_metadata = FieldMetadata(
                        field=field,
                        session=session,
                        event_name=custom_doc.filepath.stem,
                        os_names=custom_doc.identification.os,
                    )

                    if csv_writer:
                        if not all(
                            [field_metadata.ecs_description, field_metadata.ecs_example]
                        ):
                            csv_writer.add_row(field_metadata)

                    # Check if the field we are writing is a wildcard or special field
                    # If it is, we skip it unless it has a specific description or example
                    # Wildcard fields are those that end with "._" or ".*"
                    if any(["._" in field, ".*" in field]):
                        if (
                            custom_doc.fields.details
                            and field in custom_doc.fields.details
                        ):
                            field_metadata.ecs_description = custom_doc.fields.details[
                                field
                            ].description
                        else:
                            logging.info(
                                f"Skipping field {field} because it is a wildcard or special field that does not have a specific description or example"
                            )
                            continue
                    field_metadata.write_markdown(f)
            logging.debug(f"wrote markdown to {output_filename}")

    # If we have a CSV writer, write the CSV file
    if csv_writer:
        csv_writer.write_csv()
