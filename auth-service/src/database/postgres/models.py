from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.types import String


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "login": self.login,
            "password": self.password,
        }
