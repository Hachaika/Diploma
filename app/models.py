from flask_login import UserMixin
from __init__ import db
from sqlalchemy.orm import relationship


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(10000))
    name = db.Column(db.String(1000))
    kpd = db.Column(db.Float)
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
    p1_sp13 = db.Column(db.Integer, default=0)
    p1_sp21 = db.Column(db.Integer, default=0)
    p1_sp55 = db.Column(db.Integer, default=0)
    p2_sp0 = db.Column(db.Integer, default=0)
    p2_sp1 = db.Column(db.Integer, default=0)
    p2_sp2 = db.Column(db.Integer, default=0)
    p2_sp3 = db.Column(db.Integer, default=0)
    p2_sp5 = db.Column(db.Integer, default=0)
    p2_sp8 = db.Column(db.Integer, default=0)
    p2_sp13 = db.Column(db.Integer, default=0)
    p2_sp21 = db.Column(db.Integer, default=0)
    p2_sp55 = db.Column(db.Integer, default=0)
    p3_sp0 = db.Column(db.Integer, default=0)
    p3_sp1 = db.Column(db.Integer, default=0)
    p3_sp2 = db.Column(db.Integer, default=0)
    p3_sp3 = db.Column(db.Integer, default=0)
    p3_sp5 = db.Column(db.Integer, default=0)
    p3_sp8 = db.Column(db.Integer, default=0)
    p3_sp13 = db.Column(db.Integer, default=0)
    p3_sp21 = db.Column(db.Integer, default=0)
    p3_sp55 = db.Column(db.Integer, default=0)
    p4_sp0 = db.Column(db.Integer, default=0)
    p4_sp1 = db.Column(db.Integer, default=0)
    p4_sp2 = db.Column(db.Integer, default=0)
    p4_sp3 = db.Column(db.Integer, default=0)
    p4_sp5 = db.Column(db.Integer, default=0)
    p4_sp8 = db.Column(db.Integer, default=0)
    p4_sp13 = db.Column(db.Integer, default=0)
    p4_sp21 = db.Column(db.Integer, default=0)
    p4_sp55 = db.Column(db.Integer, default=0)
    p5_sp0 = db.Column(db.Integer, default=0)
    p5_sp1 = db.Column(db.Integer, default=0)
    p5_sp2 = db.Column(db.Integer, default=0)
    p5_sp3 = db.Column(db.Integer, default=0)
    p5_sp5 = db.Column(db.Integer, default=0)
    p5_sp8 = db.Column(db.Integer, default=0)
    p5_sp13 = db.Column(db.Integer, default=0)
    p5_sp21 = db.Column(db.Integer, default=0)
    p5_sp55 = db.Column(db.Integer, default=0)

    assignments = db.relationship('TaskAssignment', cascade='all, delete-orphan', back_populates='task')
    hard_tasks = relationship('HardTasks', cascade='all, delete-orphan', backref='task')

    def __repr__(self):
        return f'<Task {self.id}>'


class TaskAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    week_num = db.Column(db.Integer)
    assigned = db.Column(db.Boolean, default=True)
    done = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float)
    start = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    task = db.relationship('Task', back_populates='assignments')
    user = db.relationship('Users', back_populates='assigned_tasks')


class UsersPro(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(10000))
    name = db.Column(db.String(1000))
    KPD_P1_SP1 = db.Column(db.Float)
    KPD_P2_SP0 = db.Column(db.Float)
    KPD_P2_SP1 = db.Column(db.Float)
    KPD_P2_SP2 = db.Column(db.Float)
    KPD_P2_SP3 = db.Column(db.Float)
    KPD_P2_SP5 = db.Column(db.Float)
    KPD_P3_SP0 = db.Column(db.Float)
    KPD_P3_SP1 = db.Column(db.Float)
    KPD_P3_SP2 = db.Column(db.Float)
    KPD_P3_SP3 = db.Column(db.Float)
    KPD_P3_SP5 = db.Column(db.Float)
    KPD_P3_SP8 = db.Column(db.Float)
    KPD_P4_SP0 = db.Column(db.Float)
    KPD_P4_SP1 = db.Column(db.Float)
    KPD_P4_SP2 = db.Column(db.Float)
    KPD_P4_SP3 = db.Column(db.Float)
    KPD_P4_SP5 = db.Column(db.Float)
    KPD_P4_SP8 = db.Column(db.Float)
    KPD_P4_SP13 = db.Column(db.Float)
    KPD_P4_SP55 = db.Column(db.Float)
    KPD_P5_SP1 = db.Column(db.Float)
    KPD_P5_SP2 = db.Column(db.Float)
    KPD_P5_SP3 = db.Column(db.Float)
    KPD_P5_SP8 = db.Column(db.Float)
    KPD_P5_SP5 = db.Column(db.Float)
    vacation_start = db.Column(db.Date)
    vacation_end = db.Column(db.Date)


class HardTasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task_name = db.Column(db.String)
    assigned = db.Column(db.Boolean, default=True)

    task_assignment_pro = relationship('TaskAssignmentPro', back_populates='hard_task')


class TaskAssignmentPro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    hard_task_id = db.Column(db.Integer, db.ForeignKey('hard_tasks.id'))
    task_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users_pro.id'))
    assigned = db.Column(db.Boolean, default=True)
    done = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float)

    hard_task = relationship('HardTasks', back_populates='task_assignment_pro')

    user = relationship('UsersPro')


class TaskAssignmentFinal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users_pro.id'))
    week_num = db.Column(db.Integer)
    assigned = db.Column(db.Boolean, default=True)
    done = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float)
    deadline = db.Column(db.DateTime)


class TaskPro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    project_duration = db.Column(db.Float)
    start_project_date = db.Column(db.Date)
    ending_project_date = db.Column(db.Date)
