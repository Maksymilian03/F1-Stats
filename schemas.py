from pydantic import BaseModel
from typing import Optional

class Driver(BaseModel):
    full_name: str
    team_name: Optional[str] = None
    driver_number: int
    country_code: Optional[str] = None
    headshot_url: Optional[str] = None
