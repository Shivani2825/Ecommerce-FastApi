from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from user import api as UserRoute
from configs.connection import DATABASE_URL 



db_url = DATABASE_URL()



app = FastAPI()

app.include_router(UserRoute.router, prefix="/user", tags=["Users"]),

register_tortoise(
    app,
    db_url=db_url,
    modules={'models': ['user.models']},
    generate_schemas=True,
    add_exception_handlers=True
)