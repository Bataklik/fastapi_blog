from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username:str = Field(min_length=1, max_length=100)
    email:EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    pass

#* Door dat de response UserBase erft, gaat het email retourneren,
#* dit gaan we later aanpassen
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    image_file:str | None
    image_path:str

class PostBase(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    content:str = Field(min_length=1)
    author:str = Field(min_length=1, max_length=50)


class PostCreate(PostBase):
    #! Tijdelijk
    user_id:int

class PostResponse(PostBase):
    #* In pydantic v2 moet je from_attributes instellen
    #* om ORM objecten te kunnen gebruiken
    model_config = ConfigDict(from_attributes=True)

    #* Velden die geretourneerd worden in de response
    id:int
    user_id:int
    date_posted:datetime
    author:UserResponse
