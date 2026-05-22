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


class GroupConflict(Serializeable):
    __tablename__ = "group_conflict"

    group_id_1: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    group_id_2: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    reason: Mapped[str] = mapped_column(String(1024), nullable=True)


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
