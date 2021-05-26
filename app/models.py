from typing import Optional
from pydantic import BaseModel, validator


class Customer(BaseModel):
    id: int
    name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    
    @validator('age')
    def age_must_have_1_to_3_digits(cls, v):
        digits = len(str(v))
        if digits == 0:
            raise ValueError(f'Age does not have any digit!')
        elif digits > 3:
            raise ValueError(f'Age has more than 3 digits! ({digits})')
        return v
