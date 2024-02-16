from flask_login import UserMixin
from __init__ import db


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(10000))
    name = db.Column(db.String(1000))
    assigned_tasks = db.relationship('TaskAssignment', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(10000))
    name = db.Column(db.String(1000))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_project = db.Column(db.String)
    num_people = db.Column(db.Integer)
    project_duration = db.Column(db.Float)
    start_project_date = db.Column(db.Date)
    ending_project_date = db.Column(db.Date)
    p1_sp0 = db.Column(db.Integer, default=0)
    p1_sp1 = db.Column(db.Integer, default=0)
    p1_sp2 = db.Column(db.Integer, default=0)
    p1_sp3 = db.Column(db.Integer, default=0)
    p1_sp5 = db.Column(db.Integer, default=0)
    p1_sp8 = db.Column(db.Integer, default=0)
    p1_sp55 = db.Column(db.Integer, default=0)
    p2_sp0 = db.Column(db.Integer, default=0)
    p2_sp1 = db.Column(db.Integer, default=0)
    p2_sp2 = db.Column(db.Integer, default=0)
    p2_sp3 = db.Column(db.Integer, default=0)
    p2_sp5 = db.Column(db.Integer, default=0)
    p2_sp8 = db.Column(db.Integer, default=0)
    p2_sp55 = db.Column(db.Integer, default=0)
    p3_sp0 = db.Column(db.Integer, default=0)
    p3_sp1 = db.Column(db.Integer, default=0)
    p3_sp2 = db.Column(db.Integer, default=0)
    p3_sp3 = db.Column(db.Integer, default=0)
    p3_sp5 = db.Column(db.Integer, default=0)
    p3_sp8 = db.Column(db.Integer, default=0)
    p3_sp55 = db.Column(db.Integer, default=0)
    p4_sp0 = db.Column(db.Integer, default=0)
    p4_sp1 = db.Column(db.Integer, default=0)
    p4_sp2 = db.Column(db.Integer, default=0)
    p4_sp3 = db.Column(db.Integer, default=0)
    p4_sp5 = db.Column(db.Integer, default=0)
    p4_sp8 = db.Column(db.Integer, default=0)
    p4_sp55 = db.Column(db.Integer, default=0)
    p5_sp0 = db.Column(db.Integer, default=0)
    p5_sp1 = db.Column(db.Integer, default=0)
    p5_sp2 = db.Column(db.Integer, default=0)
    p5_sp3 = db.Column(db.Integer, default=0)
    p5_sp5 = db.Column(db.Integer, default=0)
    p5_sp8 = db.Column(db.Integer, default=0)
    p5_sp55 = db.Column(db.Integer, default=0)

    assignments = db.relationship('TaskAssignment', back_populates='task')

    def __repr__(self):
        return f'<Task {self.id}>'


class TaskAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    week_num = db.Column(db.Integer)
    assigned = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float)

    task = db.relationship('Task', back_populates='assignments')
    user = db.relationship('Users', back_populates='assigned_tasks')

