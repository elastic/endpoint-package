import logging
import pathlib
from .models import CustomDocumentationList, Filter
from .database import getDatabase, PackageField, OverrideRelationship

from sqlmodel import (
    Session,
    select,
    or_,
    and_,
    case,
)

from typing import List


def generate_custom_documentation_markdown(
    db_path: pathlib.Path, output_dir: pathlib.Path
):
    """
    Generate markdown files for custom documentation
    """

    def get_output_filepath(src_path: pathlib.Path) -> pathlib.Path:
        """
        get_output_filepath determines the output filename for a given source path

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
        if os == "windows":
            return "Windows"
        if os == "linux":
            return "Linux"
        if os == "macos":
            return "macOS"
        return os

    def get_formatted_os_string(os_list: List[str]) -> str:
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
                # f.write("<table>\n")
                # f.write("<tr><th>Name</th><th>Description</th><th>Example</th></tr>\n")
                for field in custom_doc.fields.endpoint:
                    description = "No Description Found"
                    example = ""
                    event_name = custom_doc.filepath.stem

                    #
                    # This query will look for an override for the field in the following order:
                    # 1. Event name
                    # 2. OS
                    # 3. Default
                    #
                    # If no override is found, the package field description will be used
                    #
                    override = session.exec(
                        select(OverrideRelationship)
                        .where(
                            and_(
                                # field must match
                                OverrideRelationship.name == field,
                                # one of the following must match
                                or_(
                                    (OverrideRelationship.event == event_name),
                                    (
                                        OverrideRelationship.os
                                        == custom_doc.identification.os[0]
                                    ),
                                    (OverrideRelationship.default == True),
                                ),
                            )
                        )
                        .order_by(
                            # The order of precedence is event, os, default, so we order by that
                            case(
                                (OverrideRelationship.event == event_name, 1),
                                (
                                    OverrideRelationship.os
                                    == custom_doc.identification.os[0],
                                    2,
                                ),
                                (OverrideRelationship.default == True, 3),
                                else_=4,
                            )
                        )
                    ).first()

                    if override:
                        description = override.override.description
                        if override.override.example:
                            example = override.override.example
                        logging.debug(
                            f"Found override for field {field} in {event_name}"
                        )
                    else:
                        #
                        # If no override is found, use the package field description
                        #
                        package_field = session.exec(
                            select(PackageField).where(PackageField.name == field)
                        ).first()
                        if package_field:
                            #
                            # The package field description may contain newlines, so we replace them with spaces
                            #
                            description = package_field.description.replace(
                                "\n", "  "
                            ).replace("\r", "  ")
                            if package_field.example:
                                example = package_field.example

                    f.write(f"#### `{field}`\n\n")
                    f.write("<div style='margin-left: 20px;'>\n")
                    f.write("<table>\n")
                    f.write(f"<tr><td>Description</td><td>{description}</td></tr>\n")
                    if example:
                        f.write(f"<tr><td>Example</td><td><code>{example}</code></td></tr>\n")
                    f.write("</table>\n\n<br>\n\n")
                    f.write("</div>\n\n")
                #     f.write("<tr>\n")
                #     f.write(f"<td><code>{field}</code></td>\n")
                #     f.write(f"<td>{description}</td>\n")
                #     if example:
                #         f.write(f"<td><code>{example}</code></td>\n")
                #     else:
                #         f.write("<td></td>\n")
                #     f.write("</tr>\n")

                # f.write("</table>\n")

            logging.debug(f"wrote markdown to {output_filename}")
