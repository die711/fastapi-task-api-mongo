from typing import List
from bson import ObjectId

from schemas.task import Task, UpdateTask, CreateTask
from database.database import database

collection = database.tasks


async def get_all_tasks() -> List[Task]:
    tasks = []
    cursor = collection.find()

    async for document in cursor:
        task = __collection_to_schema(document)
        tasks.append(task)

    return tasks


async def get_one_task_id(id: str) -> Task:
    task = await __get_task_by_id(id)
    if task is None:
        raise Exception('Task  not found')

    return __collection_to_schema(task)


async def create_task(task: CreateTask) -> Task:
    task_db = await __get_task_by_title(task.title)
    if task_db is not None:
        raise Exception('Task duplicated')

    new_task = await collection.insert_one(task.dict())
    created_task = await __get_task_by_id(new_task.inserted_id)

    return __collection_to_schema(created_task)


async def update_task(id: str, task: UpdateTask) -> Task:
    task_db = await __get_task_by_id(id)
    if task_db is None:
        raise Exception('Task not found')

    if task_db['title'] != task.title:
        task_db = await __get_task_by_title(task.title)
        if task_db is not None:
            raise Exception('Task duplicated')

    task_dict = {k: v for k, v in task.dict().items() if v is not None}
    # await collection.replace_one({'_id': ObjectId(id)}, task_dict)
    await collection.update_one({'_id': ObjectId(id)}, {'$set': task_dict})
    task_db = await __get_task_by_id(id)

    return __collection_to_schema(task_db)


async def delete_task(id: str):
    task_db = await __get_task_by_id(id)
    if task_db is None:
        raise Exception('Task not found')

    await collection.delete_one({'_id': ObjectId(id)})


def __collection_to_schema(task: dict) -> Task:
    return Task(
        id=str(task['_id']),
        title=str(task['title']),
        description=str(task['description']),
        completed=str(task['completed'])
    )


async def __get_task_by_id(id: str):
    return await collection.find_one({'_id': ObjectId(id)})


async def __get_task_by_title(title: str):
    return await collection.find_one({'title': title})
