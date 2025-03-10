import pathlib
from .models import Package, PackageList
import json


def generate_package_markdown(package: Package):
    """
    Generate markdown for a package

    Args:
        package: the package to generate markdown for

    Returns:
        markdown string
    """
    markdown = f"# {package.name}\n\n"
    for field in package.fields:
        markdown += f"### {field.name}\n\n"
        markdown += f"#### Description\n"
        markdown += f"{field.description}\n"
        markdown += f"#### Example\n\n"
        markdown += f"```json\n"
        if not field.example:
            markdown += "Needs example\n"
        else:
            markdown += json.dumps(field.example, indent=4)
        markdown += "\n```\n<hr>\n\n"
    return markdown


def generate_package_list_markdown(package_list: PackageList, output_directory: pathlib.Path):
    """
    Generate markdown for a list of packages

    Args:
        package_list: the package list to generate markdown for

    Returns:
        markdown string
    """
    if not output_directory.exists():
        output_directory.mkdir(parents=True)
    if not output_directory.is_dir():
        raise ValueError(f"output_directory {output_directory} is not a directory")

    for package in package_list.packages:
        path = output_directory / f"{package.name}.md"
        with path.open("w") as f:
            f.write(generate_package_markdown(package))

    readme_path = output_directory / "README.md"
    with readme_path.open("w") as f:
        f.write("# Packages\n\n")
        for package in package_list.packages:
            f.write(f"- [{package.name}]({package.name}.md)\n")
    return f"Generated {len(package_list.packages)} packages to {output_directory}"
