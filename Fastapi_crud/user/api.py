from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi_login import LoginManager
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from email_validator import validate_email,EmailNotValidError
import os
import jwt
import json
from fastapi import FastAPI
from fastapi import APIRouter
from . models import *
from user.pydantic_models import categoryitem,Token, subcategoryitem, product, categoryUpdate, categorydelete , subcategoryupdate,subcategorydelete,productupdate,productdelete,Useradmin,Adminlogin
from passlib.context import CryptContext
from configs import appinfo
from fastapi.encoders import jsonable_encoder
from functools import lru_cache
from slugify import slugify
from datetime import datetime, timedelta


# @lru_cache()
# def app_setting():
#     return appinfo.Setting()

# settings=app_setting()
# app_url=settings.app_url


SECRET="your-secret-key"
router = APIRouter()
manager=LoginManager(SECRET,token_url='/admin_login/')
pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")


@router.post('/category/')
async def create_category(data: categoryitem = Depends(), category_image: UploadFile = File(...)):
    if await Category.exists(name=data.name):
        return {"status": False, "message": "category already exists"}
    else:
        slug = slugify(data.name)
        FILEPATH = "static/images/category"

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ['png', 'jpg', 'jpeg']:
            return {"status": "error", "detail": "file extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"_"+str(dt_timestamp)+" "+extension
        generate_name = FILEPATH+modified_image_name

        file_content = await category_image.read()

        with open(generate_name, "wb") as file:
            file.write(file_content)
            file.close()
        image_url = generate_name

        category_obj = await Category.create(
            category_image=image_url,
            description=data.description,
            name=data.name,
            slug=slug
        )

        if category_obj:
            return {"status": True, "message": "category added"}
        else:
            return {"status": False, "message": "something wrong"}
# update category


@router.put('/category/')
async def update_category_details(data: categoryUpdate = Depends(), category_image: UploadFile = File(...)):
    if await Category.exists(id=data.id):
        slug = slugify(data.name)
        FILEPATH = "static/images/category"

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ['png', 'jpg', 'jpeg']:
            return {"status": "error", "detail": "file extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"_"+str(dt_timestamp)+" "+extension
        generate_name = FILEPATH+modified_image_name

        file_content = await category_image.read()

        with open(generate_name, "wb") as file:
            file.write(file_content)
            file.close()

        category_obj = await Category.filter(id=data.id).update(
            category_image=generate_name,
            description=data.description,
            name=data.name,
            slug=slug
        )

        return {"message": "Update category"}

# delete category
@router.delete("/delete_category",)
async def read_item(data: categorydelete,):
    delete_category = await Category.filter(id=data.category_id).delete()
    return {"message": " category deleted"}


@router.get('/allcategories/')
async def get_category():
    cat_obj = await Category.all()
    return cat_obj


@router.post('/subcategory/')
async def create_subcategory(data: subcategoryitem = Depends(), subcategory_image: UploadFile = File(...)):
    if await Category.exists(id=data.category_id):
        category_obj = await Category.get(id=data.category_id)

        if await SubCategory.exists(name=data.name):
            return {"status": False, "message": "category already exists"}
        else:
            slug = slugify(data.name)

            FILEPATH = "static/images/subcategory"

            if not os.path.isdir(FILEPATH):
                os.mkdir(FILEPATH)

            filename = subcategory_image.filename
            extension = filename.split(".")[1]
            imagename = filename.split(".")[0]

            if extension not in ['png', 'jpg', 'jpeg']:
                return {"status": "error", "detail": "file extension not allowed"}

            dt = datetime.now()
            dt_timestamp = round(datetime.timestamp(dt))

            modified_image_name = imagename+"_"+str(dt_timestamp)+" "+extension
            generated_name = FILEPATH+modified_image_name

            file_content = await subcategory_image.read()

            with open(generated_name, "wb") as file:
                file.write(file_content)
                file.close()
            # image_url = generated_name

            subcategory_obj = await SubCategory.create(
                subcategory_image=generated_name,
                description=data.description,
                category=category_obj,
                name=data.name,
                slug=slug
            )

            if subcategory_obj:
                return {"status": True, "message": "sub category added"}
            else:
                return {"status": False, "message": "something wrong"}


# subcategory update


@router.put('/subcategory/')
async def update_subcategory(data: subcategoryupdate = Depends(), subcategory_image: UploadFile = File(...)):
    if await SubCategory.exists(id=data.id):
        category= await Category.get(id=data.category_id)
        slug = slugify(data.name)

        FILEPATH = "static/images/subcategory"

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = subcategory_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ['png', 'jpg', 'jpeg']:
            return {"status": "error", "detail": "file extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"_"+str(dt_timestamp)+" "+extension
        generated_name = FILEPATH+modified_image_name

        file_content = await subcategory_image.read()

        with open(generated_name, "wb") as file:
            file.write(file_content)
            file.close()
            # image_url = generated_name

        subcategory_obj = await SubCategory.filter(id=data.id).update(
            subcategory_image=generated_name,
                description=data.description,
                category=category,
                name=data.name,
                slug=slug
            )

        return {"message":"Update Subcategory"}


# delete category
@router.delete("/delete_subcategory",)
async def read_item(data: subcategorydelete,):
    delete_subcategory = await SubCategory.filter(id=data.subcategory_id).delete()
    return {"message": " Subcategory deleted"}


@router.get('/allsubcategories/')
async def get_category():
    cat_obj = await SubCategory.all()
    return cat_obj


@router.post('/product/')
async def add_product(data: product = Depends(), product_image: UploadFile = File(...)):
    try:
        if await Category.exists(id=data.category_id):
            category_obj = await Category.get(id=data.category_id)

        if await SubCategory.exists(id=data.subcategory_id):
            subcat_obj = await SubCategory.get(id=data.subcategory_id)

            if await Product.exists(name=data.name):
                return {'status': False, 'message': 'Product alreay exists'}
            else:
                FILEPATH = "static/images/product_img"

                if not os.path.isdir(FILEPATH):
                    os.mkdir(FILEPATH)

                filename = product_image.filename
                extension = filename.split(".")[1]
                imagename = filename.split(".")[0]

                if extension not in ['png', 'jpg', 'jpeg']:
                    return {"status": "error", "detail": "file extension not allowed"}

                dt = datetime.now()
                dt_timestamp = round(datetime.timestamp(dt))

                modified_image_name = imagename+"_" + \
                    str(dt_timestamp)+" "+extension
                generated_name = FILEPATH+modified_image_name

                file_content = await product_image.read()

                with open(generated_name, "wb") as file:
                    file.write(file_content)
                    file.close()
                # image_url = generated_name

                product_obj = await Product.create(

                    product_image=generated_name,
                    description=data.description,
                    category=category_obj,
                    subcategory=subcat_obj,
                    name=data.name,
                    selling_price=data.selling_price,
                    discount_price=data.discount_price,


                )

            if product_obj:
                return {"status": True, "message": "Product category added"}
            else:
                return {"status": False, "message": "something wrong"}
    except Exception as ex:
        return {str(ex)}


    # update product
    
@router.put('/product/')
async def update_product(data: productupdate = Depends(), product_image: UploadFile = File(...)):
  if await Product.exists(id=data.id):
    category_obj = await Category.get(id=data.category_id)
    subcat_obj = await SubCategory.get(id=data.subcategory_id)
    FILEPATH = "static/images/product_img"

    if not os.path.isdir(FILEPATH):
        os.mkdir(FILEPATH)

    filename = product_image.filename
    extension = filename.split(".")[1]
    imagename = filename.split(".")[0]

    if extension not in ['png', 'jpg', 'jpeg']:
        return {"status": "error", "detail": "file extension not allowed"}

    dt = datetime.now()
    dt_timestamp = round(datetime.timestamp(dt))

    modified_image_name = imagename+"_" + \
    str(dt_timestamp)+" "+extension
    generated_name = FILEPATH+modified_image_name

    file_content = await product_image.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)
        file.close()
    
    product_obj = await Product.filter(id=data.id).update(
                    product_image=generated_name,
                    description=data.description,
                    category=category_obj,
                    subcategory=subcat_obj,
                    name=data.name,
                    selling_price=data.selling_price,
                    discount_price=data.discount_price,
                )
    return {"message":"Update Product"}


         
#  delete product
@router.delete("/delete_product",)
async def read_item(data: productdelete,):
    delete_product = await Product.filter(id=data.product_id).delete()
    return {"message": " product deleted"}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post('/admin.registration',)
async def create_admin(data:Useradmin):
    try:
        try:
            valid=validate_email(data.email)
        except EmailNotValidError as e:
            return { "status":False, "message":"invalid email id"}
        if len(data.mobile)!=10:
            return { "status":False, "message":"invalid number"}

        if await Admin.exists(mobile=data.mobile):
            { "status":False, "message":"This number already register"}
        elif await Admin.exists(email=data.email):
            { "status":False, "message":"email already register"}
        else:
            add_user=await Admin.create(email=data.email,Full_name=data.fullname,mobile=data.mobile,password=get_password_hash(data.password))
        return JSONResponse({
            "status":True,
            "message":"Registered Successfully"
        })
    except Exception as e:
        return JSONResponse({
            "status":True,
            "message":"Registered Successfully"
        })


@manager.user_loader()
async def load_user(email:str):
    if await Admin.exists(email=email):
        user=await Admin.get(email=email)
        return user

@router.post('/admin.login/')
async def login(data:Adminlogin):
     
    
    email = data.email
    user = await load_user(email)
    
    if not user:
        return JSONResponse({'status':False,'message':'User not Registered'},status_code=403)
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False,'message':'Invalid password'},status_code=403)
    print(user.id)
    access_token = manager.create_access_token(
        data={'sub':jsonable_encoder(user.email),}
    
    )
    '''test  current user'''
    
    
    new_dict = jsonable_encoder(user)
    new_dict.update({"access_token":access_token})
    return Token(access_token=access_token, token_type='bearer')
