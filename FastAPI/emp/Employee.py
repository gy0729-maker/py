from pydantic import BaseModel
from typing import Optional
from datetime import date


class Employee(BaseModel):
    id: Optional[int]
    name: str
    department: str
    hire_date: date
