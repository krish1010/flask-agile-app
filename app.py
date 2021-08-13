from flask import Flask, redirect, url_for
from database.db import db

from blueprints.users import USERS_BLUEPRINT
from blueprints.tasks import TASKS_BLUEPRINT

app = Flask(__name__)
app.config.from_pyfile('config/settings.staging.cfg')
db.init_app(app)

app.register_blueprint(USERS_BLUEPRINT, url_prefix='/users')
app.register_blueprint(TASKS_BLUEPRINT, url_prefix='/tasks')


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return redirect(url_for('users.register_user'))


if __name__ == '__main__':
    app.run()
