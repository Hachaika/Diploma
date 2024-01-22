from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from __init__ import login_manager
from .__init__ import users, tasks
from .models import Users, Admins, db, Task, TaskAssignment
from .forms import LoginForm, TaskForm
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import numpy as np


def calculate_project_duration(num_people, p1_sp0, p1_sp1, p1_sp2, p1_sp3, p1_sp5, p1_sp8, p1_sp55, p2_sp0,
                               p2_sp1, p2_sp2, p2_sp3, p2_sp5, p2_sp8, p2_sp55, p3_sp0, p3_sp1,
                               p3_sp2, p3_sp3, p3_sp5, p3_sp8, p3_sp55, p4_sp0, p4_sp1, p4_sp2,
                               p4_sp3, p4_sp5, p4_sp8, p4_sp55, p5_sp0, p5_sp1, p5_sp2, p5_sp3,
                               p5_sp5, p5_sp8, p5_sp55):
    project_duration = ((p1_sp0 * 0 + p1_sp1 * 1 + p1_sp2 * 0 + p1_sp3 * 0 + p1_sp5 * 0 + p1_sp8 * 0 + p1_sp55 * 0 +
                         p2_sp0 * 0.2 + p2_sp1 * 1.36 + p2_sp2 * 13.11 + p2_sp3 * 30.45 + p2_sp5 * 66.43 + p2_sp8 * 0 +
                         p2_sp55 * 0 + p3_sp0 * 4.68 + p3_sp1 * 5.82 + p3_sp2 * 14.96 + p3_sp3 * 34.64 + p3_sp5 * 57.51
                         + p3_sp8 * 123.57 + p3_sp55 * 0 + p4_sp0 * 4.88 + p4_sp1 * 4.49 + p4_sp2 * 14.4 + p4_sp3 *
                         33.95 + p4_sp5 * 63.55 + p4_sp8 * 106.43 + p4_sp55 * 0 + p5_sp0 * 0.24 + p5_sp1 * 6.55 + p5_sp2
                         * 14.13 + p5_sp3 * 26.05 + p5_sp5 * 24 + p5_sp8 * 108 + p5_sp55 * 150) / num_people) / 1.3
    return project_duration


def calculate_date(start_date, project_duration):
    start_date_str = start_date.data.strftime('%Y-%m-%d')
    start_date_dt = datetime.strptime(start_date_str, '%Y-%m-%d')

    if project_duration <= 0:
        flash('Проект не может быть выполнен за указанный период', 'error')
        return None

    workdays_count = 0
    current_day = start_date_dt

    while workdays_count < project_duration:
        if current_day.weekday() not in [5, 6]:
            workdays_count += 1
        current_day += timedelta(days=1)

    end_date = current_day - timedelta(days=1)

    return end_date.strftime('%Y-%m-%d')



@users.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()

    if form.validate_on_submit():
        task = Task(
            name_project=form.name_project.data,
            num_people=form.num_people.data,
            p1_sp0=form.p1_sp0.data,
            p1_sp1=form.p1_sp1.data,
            p1_sp2=form.p1_sp2.data,
            p1_sp3=form.p1_sp3.data,
            p1_sp5=form.p1_sp5.data,
            p1_sp8=form.p1_sp8.data,
            p1_sp55=form.p1_sp55.data,
            p2_sp0=form.p2_sp0.data,
            p2_sp1=form.p2_sp1.data,
            p2_sp2=form.p2_sp2.data,
            p2_sp3=form.p2_sp3.data,
            p2_sp5=form.p2_sp5.data,
            p2_sp8=form.p2_sp8.data,
            p2_sp55=form.p2_sp55.data,
            p3_sp0=form.p3_sp0.data,
            p3_sp1=form.p3_sp1.data,
            p3_sp2=form.p3_sp2.data,
            p3_sp3=form.p3_sp3.data,
            p3_sp5=form.p3_sp5.data,
            p3_sp8=form.p3_sp8.data,
            p3_sp55=form.p3_sp55.data,
            p4_sp0=form.p4_sp0.data,
            p4_sp1=form.p4_sp1.data,
            p4_sp2=form.p4_sp2.data,
            p4_sp3=form.p4_sp3.data,
            p4_sp5=form.p4_sp5.data,
            p4_sp8=form.p4_sp8.data,
            p4_sp55=form.p4_sp55.data,
            p5_sp0=form.p5_sp0.data,
            p5_sp1=form.p5_sp1.data,
            p5_sp2=form.p5_sp2.data,
            p5_sp3=form.p5_sp3.data,
            p5_sp5=form.p5_sp5.data,
            p5_sp8=form.p5_sp8.data,
            p5_sp55=form.p5_sp55.data
        )
        db.session.add(task)

        db.session.flush()
        task.project_duration = int(calculate_project_duration(
            task.num_people,
            task.p1_sp0, task.p1_sp1, task.p1_sp2, task.p1_sp3, task.p1_sp5, task.p1_sp8, task.p1_sp55,
            task.p2_sp0, task.p2_sp1, task.p2_sp2, task.p2_sp3, task.p2_sp5, task.p2_sp8, task.p2_sp55,
            task.p3_sp0, task.p3_sp1, task.p3_sp2, task.p3_sp3, task.p3_sp5, task.p3_sp8, task.p3_sp55,
            task.p4_sp0, task.p4_sp1, task.p4_sp2, task.p4_sp3, task.p4_sp5, task.p4_sp8, task.p4_sp55,
            task.p5_sp0, task.p5_sp1, task.p5_sp2, task.p5_sp3, task.p5_sp5, task.p5_sp8, task.p5_sp55))

        task.start_project_date = form.start_date_project.data
        task.ending_project_date = calculate_date(form.start_date_project, task.project_duration)

        db.session.commit()

        return redirect(url_for('users.index'))

    tasks = Task.query.all()

    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=current_user, form=form, tasks=tasks)
    else:
        return redirect(url_for('users.login'))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        admin = Admins.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('users.index'))
        elif user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('users.tasks_page'))
        else:
            flash('Неправильный пароль или почта', 'error')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Проект удален успешно', 'success')
    else:
        flash('Проект не найден', 'error')

    return redirect(url_for('users.index'))


@users.route('/tasks', methods=['GET'])
@login_required
def tasks_page():
    form = TaskForm()

    tasks = TaskAssignment.query.filter_by(user_id=current_user.id).all()

    return render_template('tasks.html', title='Tasks', user=current_user, tasks=tasks, form=form)
