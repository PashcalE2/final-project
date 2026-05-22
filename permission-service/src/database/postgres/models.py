from typing import Any
from sqlalchemy import ForeignKey, inspect
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.types import String


Base = declarative_base()


class Serializeable(Base):
    __abstract__ = True

    def as_dict(self) -> dict[str, Any]:
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self).mapper.column_attrs
        }


class Group(Serializeable):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(length=256), nullable=True)


class UserGroup(Serializeable):
    __tablename__ = "user_groups"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Permission(Serializeable):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)


class Resource(Serializeable):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="SET NULL")
    )
    name: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(length=256), nullable=True)


class Status(Serializeable):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)


class Request(Serializeable):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    admin_id: Mapped[int] = mapped_column(nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(length=1024), nullable=True)
