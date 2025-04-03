import pathlib
import logging

from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from sqlalchemy import Engine, Column, JSON

from .models.custom_documentation import DocumentationOverrideMap
from .models.packages import Package, PackageList

from typing import Optional


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
                    ),
                    session,
                )
    session.commit()


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
