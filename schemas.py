from datetime import date
from pydantic import BaseModel


class Hardware(BaseModel):
    id: int
    hardware: date
    
    class Config:
        orm_mode = True

class Port(BaseModel):
    id: int
    port: str
    status: int
    hardware_child: int

    class Config:
        orm_mode = True

class Instruction(BaseModel):
    id: int
    name: str
    port: str
    status: int
    hardware_child: int

    class Config:
        orm_mode = True