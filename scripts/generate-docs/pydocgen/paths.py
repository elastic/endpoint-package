import pathlib

ENDPOINT_PACKAGE_DIR = pathlib.Path(__file__).resolve().parents[3]

CUSTOM_DOCUMENTATION_DIR = (
    ENDPOINT_PACKAGE_DIR / "custom_documentation" / "src" / "endpoint" / "data_stream"
)
PACKAGES_DIR = ENDPOINT_PACKAGE_DIR / "package" / "endpoint" / "data_stream"

DOCUMENTATION_OVERRIDE_PATH = (
    ENDPOINT_PACKAGE_DIR
    / "custom_documentation"
    / "src"
    / "documentation_overrides.yaml"
)
