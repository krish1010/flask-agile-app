from database.db import db
from database.models.enums.task_status import TaskStatus
from datetime import datetime


class Task(db.Model):
    __tablename__ = 'task'

    idx = db.Column(db.String, primary_key=True)

    user_id = db.Column(db.String, db.ForeignKey('users.idx'))

    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    taken_on = db.Column(db.DateTime)
    completed_on = db.Column(db.DateTime)
    status = db.Column(db.Enum(TaskStatus), default='OPEN')
    user = db.relationship('User')

    @classmethod
    def get(cls, pk):
        return cls.query.get(pk)

    @classmethod
    def get_by_uid(cls, idx: str):
        task = cls.query.filter_by(idx=idx).first()
        return task

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get_all_tasks(cls):
        return cls.query.all()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            self.save()
        return self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()
