import argparse
import logging
from logging import config
import pathlib
import traceback
import sys
import tempfile

from .markdown import generate_custom_documentation_markdown

from .models.custom_documentation import DocumentationOverrideMap

from typing import Literal


def configure_logging(
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
    verbose: bool
) -> None:
    """Configures the logging system with specified level and verbosity.

    Args:
        log_level: String representation of logging level (DEBUG, INFO, etc.)
        verbose: Boolean flag to force maximum verbosity
    """
    level = getattr(logging, log_level)

    # If verbose is specified, override to DEBUG level
    if verbose:
        level = logging.DEBUG

    # Basic config with both handlers
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Create markdown documentation for the fields defined in custom_documentation",
        epilog="Example usage: python -m pydocgen --output-dir /path/to/output",
    )

    parser.add_argument(
        "--database",
        default=pathlib.Path(tempfile.gettempdir()) / "generate-docs.sqlite",
        type=pathlib.Path,
        help="path to the database",
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="do not use cached database if it exists, always regenerate the database",
    )

    parser.add_argument(
        "--output-dir",
        default=pathlib.Path.cwd().resolve() / "output",
        type=pathlib.Path,
        help="output directory for markdown documentation",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Force maximum verbosity (DEBUG level + detailed output)",
    )

    parser.add_argument(
        "-l",
        "--log-level",
        type=str.upper,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging verbosity level",
    )

    args = parser.parse_args()

    configure_logging(args.log_level, args.verbose)

    if args.no_cache and args.database.exists():
        logging.info(f"Removing existing database {args.database} since --no-cache was specified")
        args.database.unlink()

    generate_custom_documentation_markdown(args.database, args.output_dir)
    logging.info(f"Generated markdown documentation to {args.output_dir}")

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
# package_list = PackageList.from_packages_dir(args.packages_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
