from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from database.task import crud
from schemas.task import Task, UpdateTask, CreateTask
from auth.auth import auth_schema

task_routes = APIRouter(prefix='/api/tasks', tags=['tasks'])


@task_routes.get('/', status_code=status.HTTP_200_OK, response_model=List[Task])
async def get_tasks():
    return await crud.get_all_tasks()


@task_routes.get('/{id}', dependencies=[Depends(auth_schema)], status_code=status.HTTP_200_OK, response_model=Task)
async def get_task(id: str):
    try:
        return await crud.get_one_task_id(id)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@task_routes.post('/', dependencies=[Depends(auth_schema)], status_code=status.HTTP_201_CREATED, response_model=Task)
async def save_task(task: CreateTask):
    try:
        return await crud.create_task(task)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@task_routes.put('/{id}', dependencies=[Depends(auth_schema)], status_code=status.HTTP_200_OK, response_model=Task)
async def update_task(id: str, task: UpdateTask):
    try:
        return await crud.update_task(id, task)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@task_routes.delete('/{id}', dependencies=[Depends(auth_schema)], status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(id: str):
    try:
        await crud.delete_task(id)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
