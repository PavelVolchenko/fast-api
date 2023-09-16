import logging
from fastapi import FastAPI
from model import TaskList, Task, Base, db, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/tasks/")
async def read_root():
    logger.info("GET: список всех задач")
    return [{"id": i.id, "title": i.title, "text": i.text, "is_done": i.is_done, "is_del": i.is_del} for i in
            db.query(TaskList).all()]


@app.get("/tasks/{id}")
async def read_root(id: int):
    logger.info(f"GET: задача № {id}.")
    task = db.query(TaskList).filter(TaskList.id == id).first()
    return {"id": task.id, "title": task.title, "text": task.text, "is_done": task.is_done, "is_del": task.is_del}


@app.post("/tasks")
async def create_item(task: Task):
    logger.info(f'POST: новая задача {task}.')
    new_task = TaskList(title=task.title, text=task.text)
    db.add(new_task)
    db.commit()
    return task


@app.put("/tasks/{id}")
async def update_item(id: int, task_upd: Task):
    logger.info(f'PUT: обновление задачи № {id}. Новые параметры: {task_upd}.')
    task = db.query(TaskList).filter(TaskList.id == id).first()
    for i, param in enumerate(task_upd):
        if not param[1]:
            task_upd.__dict__[param[0]] = task.__dict__[param[0]]
    task.title = task_upd.title
    task.text = task_upd.text
    task.is_done = task_upd.is_done
    task.is_del = task_upd.is_del
    db.commit()
    return {"id": id, "task": task_upd}


@app.delete("/tasks/{id}")
async def delete_item(id: int):
    logger.info(f'DELETE: удаление задачи № {id}.')
    tasks = db.query(TaskList).filter(TaskList.id == id).all()
    for task in tasks:
        db.delete(task)
        db.commit()
    return {"id": id, "DELETED": "SUCCESS"}


# curl -X 'POST' 'http://127.0.0.1:8000/tasks/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"id": 1,"title": "TEST","text": "TEST"}'
