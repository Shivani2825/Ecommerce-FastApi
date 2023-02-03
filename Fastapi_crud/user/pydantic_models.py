from pydantic import BaseModel
import uuid
from pydantic import BaseModel



class categoryitem(BaseModel):
    name : str
    description:str

class categoryUpdate(BaseModel):
    id:int
    name : str
    description:str


class categorydelete(BaseModel):
    category_id:int
   

class subcategoryitem(BaseModel):
    category_id:int
    name:str
    description:str


class subcategoryupdate(BaseModel):
    id:int
    category_id:int
    name:str
    description:str


class subcategorydelete(BaseModel):
    subcategory_id:int
    

class product(BaseModel):
    subcategory_id:int
    category_id:int
    name:str
    selling_price:int
    discount_price:int
    brand:str
    description:str


class productupdate(BaseModel):
    id:int
    subcategory_id:int
    category_id:int
    name:str
    selling_price:int
    discount_price:int
    brand:str
    description:str


class productdelete(BaseModel):
    product_id:int



class Useradmin(BaseModel):
    fullname:str
    mobile:str
    email:str
    password:str

class Adminlogin(BaseModel):
    email:str
    password:str
    

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
# class loginuser(BaseModel):
#     username : str
#     password : str
    
# class categoryupdate(BaseModel):
#     id :uuid.UUID
#     name : str
#     description:str

# class deleteuser(BaseModel):
#     user_id : uuid.UUID

