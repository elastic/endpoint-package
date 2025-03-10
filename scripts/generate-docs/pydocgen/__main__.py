import argparse
import pathlib
import traceback
import sys
from .models import PackageList
from .markdown import generate_package_list_markdown

def resolve_packages_dir() -> pathlib.Path:
    """
    resolve_packages_dir returns the directory where the packages are stored relative to this file
    """
    this_file = pathlib.Path(__file__).resolve()
    root_dir = this_file.parents[3]
    return root_dir / "package" / "endpoint" / "data_stream"

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

    #
    # Validate the output directory
    #
    if args.output.exists():
        raise FileExistsError(
            f"output directory {args.output} already exists, please remove it or specify a different directory"
        )
    args.output.mkdir(parents=True)

    #
    # Create the PackageList object and dump it to a file
    #
    package_list = PackageList.from_packages_dir(args.packages_dir)
    json_path = args.output / "packages.json"
    with json_path.open("w") as f:
        # Dump to json with indentation and exclude None values
        f.write(package_list.model_dump_json(indent=4, exclude_none=True))

    #
    # Generate markdown files
    #
    generate_package_list_markdown(package_list, args.output)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
