import pathlib
import logging

from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship, and_
from sqlalchemy import Engine, Column, JSON

from .models.custom_documentation import DocumentationOverrideMap
from .models.packages import Package, PackageList

from typing import Optional, Literal, TypeAlias

OsNameList: TypeAlias = list[Literal["windows", "linux", "macos"]]


#
# These models represent the database tables for mapped fields
#
class PackageReference(SQLModel, table=True):
    __tablename__ = "package_references"
    id: Optional[int] = Field(default=None, primary_key=True)
    package_data: Optional[str] = Field(default=None, sa_column=Column(JSON))


class PackageField(SQLModel, table=True):
    """
    PackageField represents a specific field as defined in package/endpoint/datastream/{type}/fields/fields.yml
    each in fields.yml has a name and description, this class holds the name, description, and reference to the parent package.
    These fields will be used to provide descriptions for the fields in the custom documentation.

    Note: this is the database table definition for the Package class defined in models/packages.py

    Args:
        SQLModel: this is a SQLModel class (database table)
        table: Defaults to True.

    Raises:
        ValueError: _description_

    Returns:
        _description_
    """

    __tablename__ = "package_fields"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    example: Optional[str] = None
    type: Optional[str] = None
    package_reference_id: Optional[int] = Field(foreign_key="package_references.id")
    package_reference: Optional[PackageReference] = Relationship()

    @property
    def package(self) -> Package:
        if not self.package_reference:
            raise ValueError(f"PackageReference is not set for PackageField {self}")
        return Package.model_validate_json(self.package_reference.package_data)


#
# These models reprensent the database tables for overrides
#
class OverrideField(SQLModel, table=True):
    __tablename__ = "overrides"
    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = None
    example: Optional[str] = None
    type: Optional[str] = None


class OverrideRelationship(SQLModel, table=True):
    __tablename__ = "override_relationships"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    event: Optional[str] = None
    os: Optional[str] = None
    default: bool = False
    override_id: int = Field(foreign_key="overrides.id")
    override: OverrideField = Relationship(sa_relationship_kwargs={"lazy": "joined"})


def populate_overrides(session: Session):
    dom = DocumentationOverrideMap.from_yaml()
    for name, mapping in dom.items():
        if mapping.os:
            for os, override in mapping.os.items():
                record = OverrideField(
                    description=override.description,
                    example=override.example,
                    type=override.type,
                )
                session.add(record)
                session.flush()

                related_record = OverrideRelationship(
                    name=name, os=os, override_id=record.id
                )
                session.add(related_record)

        if mapping.event:
            for event, override in mapping.event.items():

                record = OverrideField(
                    description=override.description,
                    example=override.example,
                    type=override.type,
                )
                session.add(record)
                session.flush()

                related_record = OverrideRelationship(
                    name=name, event=event, override_id=record.id
                )
                session.add(related_record)

        if mapping.default:
            record = OverrideField(
                description=mapping.default.description,
                example=mapping.default.example,
                type=mapping.default.type,
            )
            session.add(record)
            session.flush()

            related_record = OverrideRelationship(
                name=name, default=True, override_id=record.id
            )
            session.add(related_record)

    session.commit()


def populate_packages_fields(session: Session):
    """
    populate_packages_fields populates the package fields in the database

    Args:
        session: database session
    """

    def add_to_db(field: PackageField, session: Session):
        existing_field = session.exec(
            select(PackageField).where(PackageField.name == field.name)
        ).first()
        if existing_field:
            if existing_field.description != field.description:
                raise ValueError(
                    f"Field {field.name} already exists with different description"
                )
        else:
            logging.debug(f"  Adding field {field.name}")
            session.add(field)

    package_list = PackageList.from_files()
    for package in package_list:
        logging.debug(f"Adding package fields for {package.filepath}")
        package_ref = PackageReference(package_data=package.model_dump_json())
        session.add(package_ref)
        session.flush()
        for field in package.fields:
            if field.fields:
                for sub_field in field.fields:
                    name = f"{field.name}.{sub_field.name}"
                    add_to_db(
                        PackageField(
                            name=name,
                            description=sub_field.description,
                            package_reference_id=package_ref.id,
                            example=sub_field.example,
                            type=sub_field.type,
                        ),
                        session,
                    )
            else:
                add_to_db(
                    PackageField(
                        name=field.name,
                        description=field.description,
                        package_reference_id=package_ref.id,
                        example=field.example,
                        type=field.type,
                    ),
                    session,
                )
    session.commit()


class OverrideQueryResult:
    """
    Represents the result of querying for field overrides, prioritized by event, OS, and default.

    This class retrieves and stores a prioritized list of field overrides for a given field name,
    event name, and OS name from the database. The priority order is: event-specific override (highest),
    then OS-specific override, and finally the default override (lowest).

    Properties such as `description`, `example`, and `type` return the value from the highest-priority
    override that provides a non-empty value, or None if none are found.

    Args:
        session: SQLModel session used to query the database.
        field_name: Name of the field to retrieve overrides for.
        event_name: Name of the event to prioritize event-specific overrides.
        os_name: Name of the OS to prioritize OS-specific overrides.
    """

    def __init__(
        self, session: Session, field_name: str, event_name: str, os_names: OsNameList
    ):
        """
        Initialize OverrideQueryResult.

        Args:
            session: SQLModel session.
            field_name: Name of the field.
            event_name: Name of the event.
            os_name: Name of the OS.
        """
        self.overrides: list[OverrideField] = []

        overrides = session.exec(
            select(OverrideRelationship).where(OverrideRelationship.name == field_name)
        ).all()

        #
        # These functions resolve the overrides for event, os, and default respectively.
        #
        def event_override() -> OverrideField | None:
            """
            Returns the event override if it exists, otherwise None.
            """
            return next((o.override for o in overrides if o.event == event_name), None)

        def os_override() -> OverrideField | None:
            """
            Returns the OS Override if it exists.  There can be multiple os overrides, so the relevant
            ones for this document are saved in markdown table format.
            """
            description = None
            example = None
            type = None
            for o in overrides:
                if o.os:
                    if o.os in os_names:
                        if o.override.description:
                            if not description:
                                description = f"|OS|Description|\n|---|---|\n"
                            description += f"|{o.os}|{o.override.description}|\n"
                        if o.override.example:
                            if not example:
                                example = f"|OS|Example|\n|---|---|\n"
                            example += f"|{o.os}|{o.override.example}|\n"
                        if o.override.type:
                            if not type:
                                type = f"|OS|Type|\n|---|---|\n"
                            type += f"|{o.os}|{o.override.type}|\n"

            return (
                OverrideField(
                    description=description,
                    example=example,
                    type=type,
                )
                if any([description, example, type])
                else None
            )

        def default_override() -> OverrideField | None:
            """
            Returns the default override if it exists, otherwise None.
            """
            return next((o.override for o in overrides if o.default), None)

        # We save the overrides in order of priority, so that we can return the highest-priority override
        self.overrides = [event_override(), os_override(), default_override()]

    @property
    def description(self) -> str | None:
        """
        Returns the description from the highest-priority override that provides a non-empty value, or None.
        """
        for override in self.overrides:
            if override and override.description:
                return override.description
        return None

    @property
    def example(self) -> str | None:
        """
        Returns the example from the highest-priority override that provides a non-empty value, or None.
        """
        for override in self.overrides:
            if override and override.example:
                return override.example
        return None

    @property
    def type(self) -> str | None:
        """
        Returns the type from the highest-priority override that provides a non-empty value, or None.
        """
        for override in self.overrides:
            if override and override.type:
                return override.type
        return None


def getDatabase(db_path: pathlib.Path) -> Engine:
    """
    getDatabase creates a database if it does not exist, otherwise it uses the existing database

    This stores the documentation in package/endpoint/data_stream in a lightweight SQLite database.  We will
    use this when generating markdown documentation for the fields defined in the custom_documentation.

    overrides are also added to the database here.

    Args:
        db_path: path to the database

    Returns:
        database Engine
    """
    if db_path.exists():
        logging.info(f"Using existing database at {db_path}")
        return create_engine(f"sqlite:///{db_path}")

    logging.info(f"Creating database at {db_path}")
    engine = create_engine(f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        populate_packages_fields(session)
        populate_overrides(session)
        session.commit()
    return engine
