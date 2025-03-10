import pathlib
from .models import Package, PackageList
import json

def ensure_valid_output_directory(output_directory: pathlib.Path):
    """
    Ensure that the output directory is valid
    """
    if not output_directory.exists():
        output_directory.mkdir(parents=True)
    if not output_directory.is_dir():
        raise FileExistsError(f"output_directory {output_directory} is not a directory")

def generate_package_markdown(package: Package):
    """
    Generate markdown for a package

    Args:
        package: the package to generate markdown for

    Returns:
        markdown string
    """
    markdown = f"[Back to index](README.md)\n\n"
    for field in package.fields:
        markdown += f"## `{field.name}`\n\n"
        markdown += f"### Description\n"
        markdown += f"{field.description}\n"
        if field.fields:
            markdown += f"### Sub-fields\n"
            markdown += "| Field | Description | Example |\n"
            markdown += "| --- | --- | --- |\n"
            for sub_field in field.fields:
                markdown += f"| `{sub_field.name}` | {sub_field.description} | {sub_field.example} |\n"
        markdown += f"### Example\n\n"
        markdown += f"```json\n"
        if not field.example:
            markdown += "Needs example\n"
        else:
            markdown += json.dumps(field.example, indent=4)
        markdown += "\n```\n<hr>\n\n"
    return markdown

def generate_readme_markdown(package_list: PackageList, output_directory: pathlib.Path):
    """
    Generates the top level readme markdown file
    """
    ensure_valid_output_directory(output_directory)
    readme_path = output_directory / "README.md"

    #
    # This file will list each package, its top level fields, and a link to the package's markdown file
    # if the package has a sample event, it will be included in a details tag
    #
    with readme_path.open("w") as f:
        for package in package_list.packages:
            f.write(f"# {package.name}\n")
            if package.sample_event:
                f.write("### Sample Event\n")
                f.write("<details>\n")
                f.write("<summary>\nClick to expand\n</summary>\n\n")
                f.write("```json\n")
                f.write(json.dumps(package.sample_event, indent=4))
                f.write("\n```\n")
                f.write("</details>\n\n")
            f.write(f"### [Fields]({package.name}.md)\n")
            for field in package.fields:
                f.write(f"- [{field.name}]({package.name}.md#{field.name})\n")

def generate_package_list_markdown(package_list: PackageList, output_directory: pathlib.Path) -> None:
    """
    Generate markdown files for a list of packages
    """
    ensure_valid_output_directory(output_directory)

    #
    # Create a top level Readme.md file
    #
    generate_readme_markdown(package_list, output_directory)

    #
    # Walk the list of packages and create a markdown file for each
    #
    for package in package_list.packages:
        path = output_directory / f"{package.name}.md"
        with path.open("w") as f:
            f.write(generate_package_markdown(package))

    return f"Generated {len(package_list.packages)} packages to {output_directory}"
