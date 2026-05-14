from pydantic import BaseModel
from typing import Optional

class Driver(BaseModel):
    full_name: str
    team_name: Optional[str] = None
    driver_number: int
    country_code: Optional[str] = None
    headshot_url: Optional[str] = None


# F1 Api zwraca czasem "gap_to_leader" jako string (np. "1 lap"), a czasem jako float (np. 12.345)

class RaceResult(BaseModel):
    position: Optional[int] = None
    full_name: str
    driver_number: Optional[int] = None
    gap_to_leader: Optional[float | str] = None
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


class ConstructorEntry(BaseModel):
    position: int
    team: str
    points: int
    wins: int


