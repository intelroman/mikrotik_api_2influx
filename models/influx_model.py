"""
Influx Class model
"""
from typing import List
from datetime import datetime
from pydantic import BaseModel

class MyInflux(BaseModel):
    '''
    Influx dictionary model
    '''
    measurement: str
    fields: dict
    tags: dict
    time: datetime
class InfluxModel(BaseModel):
    '''
    Model expected to be sent for processing
    '''
    Output: List[MyInflux]
 