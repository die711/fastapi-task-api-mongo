from fastapi import FastAPI, Depends
from typing import Annotated
from routes.task import task_routes
from routes.auth import auth_routes
from auth.auth import get_current_user

app = FastAPI()
app.include_router(task_routes)
app.include_router(auth_routes)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/hello/user/current_user')
async def say_hello(current_user: Annotated[dict, Depends(get_current_user)]):
    return {
        'message': f"Hello {current_user['username']}"
    }
