from pydantic import BaseModel
import datetime as dt
from typing import Any, List, Optional
from operating_resource import OperatingResource

class Incident(BaseModel) :
    incident_id: str
    alarm_keyword: Optional[str]
    alarm_description: str
    place: Optional[str]
    incident_number: int
    district: str
    start_dtime: dt.datetime
    end_dtime: Optional[dt.datetime]
    operating_ressources: List[OperatingResource]

    class Config:
        fields = {'incident_id': '_id'}