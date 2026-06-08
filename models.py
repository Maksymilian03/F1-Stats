from datetime import datetime

from sqlalchemy import String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
 

class DriverStanding(Base):
    __tablename__ = "driver_standings"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    position: Mapped[int]
    full_name: Mapped[str] = mapped_column(String(100))
    team: Mapped[str | None] = mapped_column(String(100))
    points: Mapped[int]
    wins: Mapped[int]
    driver_number: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("year", "position", name="uq_year_position"),
        UniqueConstraint("year", "driver_number", name="uq_year_driver_number"),
    )


class ConstructorStanding(Base):
    __tablename__ = "constructor_standings"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    position: Mapped[int]
    team: Mapped[str] = mapped_column(String(100))
    points: Mapped[int]
    wins: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("year", "position", name="uq_constructor_year_position"),
        UniqueConstraint("year", "team", name="uq_constructor_year_team"),
    )