from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.types import String


Base = declarative_base()


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)
    description: Mapped[str]

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class UserGroup(Base):
    __tablename__ = "user_group"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(primary_key=True)


"""
class GroupRequest(Base):
    __tablename__ = "group_request"

    user_id: Mapped[int] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(nullable=False)
"""
