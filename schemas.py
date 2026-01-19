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

class UserUpdate(UserBase):
    """ Update class

    Args:
        UserBase (_type_): _description_
    """
    username:str| None = Field(default=None, min_length=1, max_length=100)
    email:EmailStr | None = Field(default=None, max_length=120)
    image_file:str| None = Field(default=None, min_length=1, max_length=200)


class PostBase(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    content:str = Field(min_length=1)
    author:str = Field(min_length=1, max_length=50)


class PostCreate(PostBase):
    #! Tijdelijk
    user_id:int


#* Geen id, want die mogen we niet updaten
class PostUpdate(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    content:str = Field(default=None, min_length=1)

class PostResponse(PostBase):
    #* In pydantic v2 moet je from_attributes instellen
    #* om ORM objecten te kunnen gebruiken
    model_config = ConfigDict(from_attributes=True)

    #* Velden die geretourneerd worden in de response
    id:int
    user_id:int
    date_posted:datetime
    author:UserResponse
