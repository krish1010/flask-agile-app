from flask import Blueprint, request, render_template, session, redirect, url_for
from database.models.enums.task_status import TaskStatus
from managers.tasks import create_task, get_all_tasks, get_task_by_id, update_task

TASKS_BLUEPRINT = Blueprint('tasks', __name__)
CREATE_TASK = 'create_task.html'


@TASKS_BLUEPRINT.route('/', methods=['GET'])
def index():
    if 'user_idx' not in session:
        return redirect(url_for('users.login'))
    all_tasks = get_all_tasks()
    filtered_tasks = filter(lambda x: x.status.value != 'approved', all_tasks)
    context = {
        'all_tasks': filtered_tasks
    }
    return render_template('display_tasks.html', **context)


@TASKS_BLUEPRINT.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_idx' not in session:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template(CREATE_TASK, **{'source': 'tasks.create'})
    else:
        title = request.form.get('title')
        description = request.form.get('description')
        taken_on = request.form.get('taken-on')
        completed_on = request.form.get('completed-on')

        create_task(title, description, taken_on, completed_on, session.get('user_idx'))

        return render_template(CREATE_TASK, **{'source': 'tasks.create'})


@TASKS_BLUEPRINT.route('/update/<idx>', methods=['GET', 'POST'])
def update(idx):
    task = get_task_by_id(idx)
    if request.method == 'GET':
        return render_template(CREATE_TASK, **{'source': 'tasks.update', 'idx': idx, 'task': task})
    if request.method == 'POST' and task:
        if session.get('user_type') == 'manager':
            title = request.form.get('title')
            description = request.form.get('description')
            taken_on = request.form.get('taken-on')
            completed_on = request.form.get('completed-on')
            status = request.form.get('status')

            update_task(task=task, title=title, description=description, taken_on=taken_on,
                        completed_on=completed_on, status=status)
        else:
            task.update(status=TaskStatus(request.form.get('status')), developer_user_id=session.get('user_idx'))

        return redirect(url_for('tasks.index'))


@TASKS_BLUEPRINT.route('/delete/<idx>', methods=['GET'])
def delete(idx):
    task = get_task_by_id(idx)
    task.delete()
    return redirect(url_for('tasks.index'))


@TASKS_BLUEPRINT.route('/history', methods=['GET'])
def history():
    if 'user_idx' not in session:
        return redirect(url_for('users.login'))
    all_tasks = get_all_tasks()
    filtered_tasks = filter(lambda x: session.get('username') in (x.created_by_username, x.developer_username), all_tasks)
    context = {
        'all_tasks': filtered_tasks,
        'source': 'history'
    }
    return render_template('display_tasks.html', **context)
