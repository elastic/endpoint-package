import logging
import pathlib
from .models import Package, PackageList, CustomDocumentationList, Filter
from .database import getDatabase, PackageField

from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from sqlalchemy import Engine, Column, JSON

from typing import List

# def ensure_valid_output_directory(output_directory: pathlib.Path):
#     """
#     Ensure that the output directory is valid
#     """
#     if not output_directory.exists():
#         output_directory.mkdir(parents=True)
#     if not output_directory.is_dir():
#         raise FileExistsError(f"output_directory {output_directory} is not a directory")

# def generate_package_markdown(package: Package):
#     """
#     Generate markdown for a package

#     Args:
#         package: the package to generate markdown for

#     Returns:
#         markdown string
#     """
#     markdown = f"[Back to index](README.md)\n\n"
#     for field in package.fields:
#         markdown += f"## `{field.name}`\n\n"
#         markdown += f"### Description\n"
#         markdown += f"{field.description}\n"
#         if field.fields:
#             markdown += f"### Sub-fields\n"
#             markdown += "| Field | Description | Example |\n"
#             markdown += "| --- | --- | --- |\n"
#             for sub_field in field.fields:
#                 markdown += f"| `{sub_field.name}` | {sub_field.description} | {sub_field.example} |\n"
#         markdown += f"### Example\n\n"
#         markdown += f"```json\n"
#         if not field.example:
#             markdown += "Needs example\n"
#         else:
#             markdown += json.dumps(field.example, indent=4)
#         markdown += "\n```\n<hr>\n\n"
#     return markdown

# def generate_readme_markdown(package_list: PackageList, output_directory: pathlib.Path):
#     """
#     Generates the top level readme markdown file
#     """
#     ensure_valid_output_directory(output_directory)
#     readme_path = output_directory / "README.md"

#     #
#     # This file will list each package, its top level fields, and a link to the package's markdown file
#     # if the package has a sample event, it will be included in a details tag
#     #
#     with readme_path.open("w") as f:
#         for package in package_list.packages:
#             f.write(f"# {package.name}\n")
#             if package.sample_event:
#                 f.write("### Sample Event\n")
#                 f.write("<details>\n")
#                 f.write("<summary>\nClick to expand\n</summary>\n\n")
#                 f.write("```json\n")
#                 f.write(json.dumps(package.sample_event, indent=4))
#                 f.write("\n```\n")
#                 f.write("</details>\n\n")
#             f.write(f"### [Fields]({package.name}.md)\n")
#             for field in package.fields:
#                 f.write(f"- [{field.name}]({package.name}.md#{field.name})\n")

# def generate_package_list_markdown(package_list: PackageList, output_directory: pathlib.Path) -> None:
#     """
#     Generate markdown files for a list of packages
#     """
#     ensure_valid_output_directory(output_directory)

#     #
#     # Create a top level Readme.md file
#     #
#     generate_readme_markdown(package_list, output_directory)

#     #
#     # Walk the list of packages and create a markdown file for each
#     #
#     for package in package_list.packages:
#         path = output_directory / f"{package.name}.md"
#         with path.open("w") as f:
#             f.write(generate_package_markdown(package))

#     return f"Generated {len(package_list.packages)} packages to {output_directory}"


def generate_custom_documentation_markdown(db_path: pathlib.Path, output_dir: pathlib.Path):
    """
    Generate markdown files for custom documentation
    """

    def get_output_filename(src_path: pathlib.Path) -> pathlib.Path:
        parts = src_path.parts
        index = parts.index("data_stream")
        output_filename = output_dir
        for part in parts[index + 1 : -1]:
            output_filename = output_filename / part
        return output_filename / parts[-1].replace(".yaml", ".md")

    def get_formatted_os_name(os: str) -> str:
        if os == "windows":
            return "Windows"
        if os == "linux":
            return "Linux"
        if os == "macos":
            return "macOS"
        return os

    def get_formatted_os_string(os_list: List[str]) -> str:
        return ", ".join(get_formatted_os_name(os) for os in os_list)

    def get_kql_query_string(filter: Filter) -> str:
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
                queries.append(f"{field_name} : \"{field_value}\"")
        return " and ".join(queries)

    engine = getDatabase(db_path)
    custom_docs = CustomDocumentationList.from_files()
    with Session(engine) as session:
        for custom_doc in custom_docs:
            output_filename = get_output_filename(custom_doc.filepath)
            output_filename.parent.mkdir(parents=True, exist_ok=True)
            with output_filename.open("w") as f:
                f.write(f"# {custom_doc.overview.name}\n\n")

                f.write(f"## Description\n\n")
                f.write(f"{custom_doc.overview.description}\n\n")

                f.write("## Overview\n\n")
                f.write("<table>\n")
                f.write("<tr>\n")
                f.write("<td><strong>OS</strong></td>\n")
                f.write(f"<td>{get_formatted_os_string(custom_doc.identification.os)}</td>\n")
                f.write("</tr>\n")
                f.write("<tr>\n")
                f.write(f"<td><strong>Data Stream</strong></td>\n")
                f.write(f"<td>{custom_doc.identification.data_stream}</td>\n")
                f.write("</tr>\n")
                f.write("<tr>\n")
                f.write(f"<td><strong>KQL Query</strong></td>\n")
                f.write(f"<td><code>{get_kql_query_string(custom_doc.identification.filter)}</code></td>\n")
                f.write("</tr>\n")
                f.write("</table>\n\n")

                f.write(f"## Fields\n\n")
                f.write("<table>\n")
                #f.write("<tr><th>Field</th><th>Description</th></tr>\n")
                for field in custom_doc.fields.endpoint:
                    package_field = session.exec(select(PackageField).where(PackageField.name == field)).first()

                    description = None
                    if package_field:
                        description = package_field.description.replace("\n", "  ").replace("\r", "  ")
                    f.write(f"<tr><td><code>{field}<code></td><td>{description if description else 'No description found'}</td></tr>\n")
                f.write("</table>\n")

            logging.debug(f"wrote markdown to {output_filename}")
