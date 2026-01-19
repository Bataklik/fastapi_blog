from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    """ User object

    Args:
        Base (_type_): De basis klasse voor alle modellen

    Returns:
        User: Een gebruiker in de database
    """
    #* Naam van de tabel in de database
    __tablename__ = "users"
    #* Id is het primaire sleutelveld
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    #* Username en email zijn unieke velden
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    #* Optioneel profielafbeeldingsbestand
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )
    #* Relatie met posts, een gebruiker kan meerdere posts hebben.
    #* De back_populates zorgt voor bidirectionele relatie.
    #* Ook gebruiken we Post zonder Post te definiëren vanwege
    #* from __future__ import annotations
    posts: Mapped[list[Post]] = relationship(back_populates="author", cascade="all, delete-orphan")

    #* Property om het pad naar de profielafbeelding te krijgen,
    #* anders standaardafbeelding gebruiken.
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    #* Foreign key naar de gebruiker die de post heeft gemaakt
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        #? Foreign keys krijgen niet automatisch een index,
        #? dus expliciet toevoegen
        index=True,
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    #* Relatie met de user die de post heeft gemaakt,
    #* back_populates zorgt voor bidirectionele relatie
    author: Mapped[User] = relationship(back_populates="posts")
