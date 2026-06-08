import re
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from app.countries.schemas import CountryResponse
from app.categories.schemas import CategoryResponse

allowed_citites = [
    "Bogota", "Medellin", "Guadalajara", "Ciudad de Mexico", 
    "Barcelona", "Madrid", "Buenos Aires", "Cordoba"
]

class ClientBase(BaseModel):
    name_client: str = Field(..., min_length=3, max_length=100)
    city: str
    country_id: int
    category_id: int
    is_active: bool = True

class ClientCreate(ClientBase):
    user_created: str = "admin"

    @field_validator('name_client')
    @classmethod
    def validate_name_no_numbers(cls, v: str) -> str:
        if re.search(r'\d', v):
            raise ValueError('The client name cannot contain numeric characters.')
        return v

    @field_validator('city')
    @classmethod
    def validate_city_exists(cls, v: str) -> str:
        cleaned_city = v.strip()
        if cleaned_city not in allowed_citites:
            raise ValueError(f'City "{cleaned_city}" is not valid. Allowed cities: {", ".join(allowed_citites)}')
        return cleaned_city

class ClientResponse(ClientBase):
    id: int
    user_created: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    country: CountryResponse
    category: CategoryResponse

    class Config:
        from_attributes = True