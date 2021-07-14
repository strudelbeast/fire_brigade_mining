from pydantic import BaseModel
import datetime as dt
from typing import Optional, Union

class OperatingResource(BaseModel):
    name: str
    disposition: dt.datetime
    alert: Union[Optional[dt.datetime], str]
    move_out: Optional[dt.datetime]
    move_in: Optional[dt.datetime]
    dispatch_number: int
    

    class Config:
        fields = {'name': '_id'}