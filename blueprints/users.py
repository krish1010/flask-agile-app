from flask import Blueprint, request, render_template, session, redirect, url_for

from managers.users import create_user, get_user

USERS_BLUEPRINT = Blueprint('users', __name__)
TASKS_INDEX = 'tasks.index'
USERS_LOGIN = 'users.login'


@USERS_BLUEPRINT.route('', methods=['POST'])
def index():
    ...


@USERS_BLUEPRINT.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        user_type = request.form.get('manager') or request.form.get('developer')
        password = request.form.get('psw')
        _ = request.form.get('psw-repeat')
        print(username, password, user_type)
        create_user(username, password, user_type=user_type)
        user = get_user(username, password)
        session['user_idx'] = user.idx
        session['username'] = user.username
        session['user_type'] = user.user_type.value
        return redirect(url_for(TASKS_INDEX))


@USERS_BLUEPRINT.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_idx' in session:
        # flash('You are already logged in', 'info')
        return redirect(url_for(TASKS_INDEX))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('psw')
        user = get_user(username, password)
        if user:
            session['user_idx'] = user.idx
            session['username'] = user.username
            return redirect(url_for(TASKS_INDEX))
        else:
            return redirect(url_for(USERS_LOGIN))


@USERS_BLUEPRINT.route('/logout')
def logout():
    try:
        if 'user_type' in session:
            del session['user_type']
        if 'user_idx' in session:
            del session['user_idx']
        if 'username' in session:
            del session['username']

    except KeyError:
        return redirect(url_for(USERS_LOGIN))
    return redirect(url_for(USERS_LOGIN))
