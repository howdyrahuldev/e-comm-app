import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Float,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )


class Product(Base):
    __tablename__ = "Products"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = Column(Text, nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    price: Mapped[float] = Column(Float, nullable=False)


class User(Base):
    __tablename__ = "Users"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = Column(Text, unique=True, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    hashed_password: Mapped[str] = Column(Text, nullable=False)
