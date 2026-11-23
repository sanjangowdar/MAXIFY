from pydantic import BaseModel, EmailStr, Field
class Credentials(BaseModel):
    email:EmailStr
    password:str=Field(min_length=6,max_length=128)
class ProfileIn(BaseModel):
    display_name:str=Field(default="",max_length=100)
    data:dict=Field(default_factory=dict)
class ChatIn(BaseModel):
    message:str=Field(min_length=1,max_length=4000)
