from pydantic import BaseModel
from typing import Optional

class Driver(BaseModel):
    full_name: str
    team_name: Optional[str] = None
    driver_number: int
    country_code: Optional[str] = None
    headshot_url: Optional[str] = None


class RaceResult(BaseModel):
    position: Optional[int] = None
    full_name: str
    driver_number: Optional[int] = None
    gap_to_leader: Optional[float] = None
    dnf: Optional[bool] = None
    dns: Optional[bool] = None
    dsq: Optional[bool] = None
   

class StandingsEntry(BaseModel):
    position: int
    full_name: str
    team: Optional[str] = None
    points: int
    wins: int
    driver_number: int


