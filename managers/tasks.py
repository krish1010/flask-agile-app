from database.models.tables.tasks import Task
from uuid import uuid4
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


def create_task(title, description, taken_on, completed_on):
    taken_on_f = datetime.strptime(taken_on, DATE_FORMAT)
    completed_on_f = datetime.strptime(completed_on, DATE_FORMAT)

    Task.create(idx=str(uuid4()), title=title, description=description, taken_on=taken_on_f,
                completed_on=completed_on_f)


def get_all_tasks():
    return Task.get_all_tasks()


def get_task_by_id(idx):
    return Task.get_by_uid(idx=idx)


def update_task(task, title, description, taken_on, completed_on):
    taken_on_f = datetime.strptime(taken_on, DATE_FORMAT)
    completed_on_f = datetime.strptime(completed_on, DATE_FORMAT)

    task.update(idx=str(uuid4()), title=title, description=description, taken_on=taken_on_f,
                completed_on=completed_on_f)
