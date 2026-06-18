from typing import Literal
from pydantic import BaseModel


class Driver(BaseModel):
    full_name: str
    team_name: str | None = None
    driver_number: int
    country_code: str | None = None
    headshot_url: str | None = None


# F1 Api zwraca czasem "gap_to_leader" jako string (np. "1 lap"), a czasem jako float (np. 12.345)

class RaceResult(BaseModel):
    position: int | None = None
    full_name: str
    driver_number: int | None = None
    gap_to_leader: float | str | None = None
    dnf: bool | None = None
    dns: bool | None = None
    dsq: bool | None = None


class StandingsEntry(BaseModel):
    position: int
    full_name: str
    team: str | None = None
    points: int
    wins: int
    driver_number: int


class ConstructorEntry(BaseModel):
    position: int
    team: str
    points: int
    wins: int


class DriverStandingInfo(BaseModel):
    position: int
    full_name: str
    driver_number: int
    team: str | None = None
    points: int
    wins: int


class Comparison(BaseModel):
    points_difference: int
    wins_difference: int
    position_difference: int
    leader: DriverStandingInfo | Literal["draw"]


class CompareResponse(BaseModel):
    driver1: DriverStandingInfo
    driver2: DriverStandingInfo
    comparison: Comparison



