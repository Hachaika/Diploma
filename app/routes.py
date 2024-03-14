from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import current_user, login_user, login_required, logout_user
from __init__ import login_manager
from .__init__ import users, tasks
from .models import Users, Admins, db, Task, TaskAssignment
from .forms import LoginForm, TaskForm
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from math import ceil
import pandas as pd

results_data = pd.read_excel('results.xlsx', sheet_name='priority_sp_stats')


def calculate_project_duration(num_people, p1_sp0, p1_sp1, p1_sp2, p1_sp3, p1_sp5, p1_sp8, p1_sp13, p1_sp21, p1_sp55,
                               p2_sp0, p2_sp1, p2_sp2, p2_sp3, p2_sp5, p2_sp8, p2_sp13, p2_sp21, p2_sp55, p3_sp0,
                               p3_sp1, p3_sp2, p3_sp3, p3_sp5, p3_sp8, p3_sp13, p3_sp21, p3_sp55, p4_sp0, p4_sp1,
                               p4_sp2, p4_sp3, p4_sp5, p4_sp8, p4_sp13, p4_sp21, p4_sp55, p5_sp0, p5_sp1, p5_sp2,
                               p5_sp3, p5_sp5, p5_sp8, p5_sp13, p5_sp21, p5_sp55):
    # Создание словаря среднего времени выполнения для каждого типа задания из priority_sp_stats
    task_type_avg_time = {}
    for index, row in results_data.iterrows():
        task_type = f"{row['Приоритет']}_SP{row['Сложность в SP']}"
        task_type_avg_time[task_type] = row['Среднее время выполнения в часах']

    # Замена значений в формуле на среднее время выполнения из priority_sp_stats
    project_duration = (
                               (p1_sp0 * task_type_avg_time.get('P1_SP0', 0) + p1_sp1 * task_type_avg_time.get('P1_SP1',
                                                                                                               0) +
                                p1_sp2 * task_type_avg_time.get('P1_SP2', 0) + p1_sp3 * task_type_avg_time.get('P1_SP3',
                                                                                                               0) +
                                p1_sp5 * task_type_avg_time.get('P1_SP5', 0) + p1_sp8 * task_type_avg_time.get('P1_SP8',
                                                                                                               0) +
                                p1_sp13 * task_type_avg_time.get('P1_SP13', 0) + p1_sp21 * task_type_avg_time.get(
                                           'P1_SP21', 0) +
                                p1_sp55 * task_type_avg_time.get('P1_SP55', 0) + p2_sp0 * task_type_avg_time.get(
                                           'P2_SP0', 0) +
                                p2_sp1 * task_type_avg_time.get('P2_SP1', 0) + p2_sp2 * task_type_avg_time.get('P2_SP2',
                                                                                                               0) +
                                p2_sp3 * task_type_avg_time.get('P2_SP3', 0) + p2_sp5 * task_type_avg_time.get('P2_SP5',
                                                                                                               0) +
                                p2_sp8 * task_type_avg_time.get('P2_SP8', 0) + p2_sp13 * task_type_avg_time.get(
                                           'P2_SP13', 0) +
                                p2_sp21 * task_type_avg_time.get('P2_SP21', 0) + p2_sp55 * task_type_avg_time.get(
                                           'P2_SP55', 0) +
                                p3_sp0 * task_type_avg_time.get('P3_SP0', 0) + p3_sp1 * task_type_avg_time.get('P3_SP1',
                                                                                                               0) +
                                p3_sp2 * task_type_avg_time.get('P3_SP2', 0) + p3_sp3 * task_type_avg_time.get('P3_SP3',
                                                                                                               0) +
                                p3_sp5 * task_type_avg_time.get('P3_SP5', 0) + p3_sp8 * task_type_avg_time.get('P3_SP8',
                                                                                                               0) +
                                p3_sp13 * task_type_avg_time.get('P3_SP13', 0) + p3_sp21 * task_type_avg_time.get(
                                           'P3_SP21', 0) +
                                p3_sp55 * task_type_avg_time.get('P3_SP55', 0) + p4_sp0 * task_type_avg_time.get(
                                           'P4_SP0', 0) +
                                p4_sp1 * task_type_avg_time.get('P4_SP1', 0) + p4_sp2 * task_type_avg_time.get('P4_SP2',
                                                                                                               0) +
                                p4_sp3 * task_type_avg_time.get('P4_SP3', 0) + p4_sp5 * task_type_avg_time.get('P4_SP5',
                                                                                                               0) +
                                p4_sp8 * task_type_avg_time.get('P4_SP8', 0) + p4_sp13 * task_type_avg_time.get(
                                           'P4_SP13', 0) +
                                p4_sp21 * task_type_avg_time.get('P4_SP21', 0) + p4_sp55 * task_type_avg_time.get(
                                           'P4_SP55', 0) +
                                p5_sp0 * task_type_avg_time.get('P5_SP0', 0) + p5_sp1 * task_type_avg_time.get('P5_SP1',
                                                                                                               0) +
                                p5_sp2 * task_type_avg_time.get('P5_SP2', 0) + p5_sp3 * task_type_avg_time.get('P5_SP3',
                                                                                                               0) +
                                p5_sp5 * task_type_avg_time.get('P5_SP5', 0) + p5_sp8 * task_type_avg_time.get('P5_SP8',
                                                                                                               0) +
                                p5_sp13 * task_type_avg_time.get('P5_SP13', 0) + p5_sp21 * task_type_avg_time.get(
                                           'P5_SP21', 0) +
                                p5_sp55 * task_type_avg_time.get('P5_SP55', 0)) / num_people) / 4


    project_duration = ceil(project_duration)


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
            p1_sp13=form.p1_sp13.data,
            p1_sp21=form.p1_sp21.data,
            p1_sp55=form.p1_sp55.data,
            p2_sp0=form.p2_sp0.data,
            p2_sp1=form.p2_sp1.data,
            p2_sp2=form.p2_sp2.data,
            p2_sp3=form.p2_sp3.data,
            p2_sp5=form.p2_sp5.data,
            p2_sp8=form.p2_sp8.data,
            p2_sp13=form.p2_sp13.data,
            p2_sp21=form.p2_sp21.data,
            p2_sp55=form.p2_sp55.data,
            p3_sp0=form.p3_sp0.data,
            p3_sp1=form.p3_sp1.data,
            p3_sp2=form.p3_sp2.data,
            p3_sp3=form.p3_sp3.data,
            p3_sp5=form.p3_sp5.data,
            p3_sp8=form.p3_sp8.data,
            p3_sp13=form.p3_sp13.data,
            p3_sp21=form.p3_sp21.data,
            p3_sp55=form.p3_sp55.data,
            p4_sp0=form.p4_sp0.data,
            p4_sp1=form.p4_sp1.data,
            p4_sp2=form.p4_sp2.data,
            p4_sp3=form.p4_sp3.data,
            p4_sp5=form.p4_sp5.data,
            p4_sp8=form.p4_sp8.data,
            p4_sp13=form.p4_sp13.data,
            p4_sp21=form.p4_sp21.data,
            p4_sp55=form.p4_sp55.data,
            p5_sp0=form.p5_sp0.data,
            p5_sp1=form.p5_sp1.data,
            p5_sp2=form.p5_sp2.data,
            p5_sp3=form.p5_sp3.data,
            p5_sp5=form.p5_sp5.data,
            p5_sp8=form.p5_sp8.data,
            p5_sp13=form.p5_sp13.data,
            p5_sp21=form.p5_sp21.data,
            p5_sp55=form.p5_sp55.data
        )
        db.session.add(task)

        db.session.flush()
        task.project_duration = calculate_project_duration(
            task.num_people,
            task.p1_sp0, task.p1_sp1, task.p1_sp2, task.p1_sp3, task.p1_sp5, task.p1_sp8, task.p1_sp13, task.p1_sp21,
            task.p1_sp55, task.p2_sp0, task.p2_sp1, task.p2_sp2, task.p2_sp3, task.p2_sp5, task.p2_sp8, task.p2_sp13,
            task.p2_sp21, task.p2_sp55, task.p3_sp0, task.p3_sp1, task.p3_sp2, task.p3_sp3, task.p3_sp5, task.p3_sp8,
            task.p3_sp13, task.p3_sp21, task.p3_sp55, task.p4_sp0, task.p4_sp1, task.p4_sp2, task.p4_sp3, task.p4_sp5,
            task.p4_sp8, task.p4_sp13, task.p4_sp21, task.p4_sp55, task.p5_sp0, task.p5_sp1, task.p5_sp2, task.p5_sp3,
            task.p5_sp5, task.p5_sp8, task.p5_sp13, task.p5_sp21, task.p5_sp55)

        task.start_project_date = form.start_project_date.data
        task.ending_project_date = calculate_date(form.start_project_date, task.project_duration)

        db.session.commit()

        return redirect(url_for('users.index'))

    tasks = Task.query.all()

    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=current_user, form=form, tasks=tasks)
    else:
        return redirect(url_for('users.login'))


@users.route('/users/edit_project/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_project(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.name_project = form.name_project.data
        task.num_people = form.num_people.data
        task.start_project_date = form.start_project_date.data
        task.p1_sp0 = form.p1_sp0.data
        task.p1_sp1 = form.p1_sp1.data
        task.p1_sp2 = form.p1_sp2.data
        task.p1_sp3 = form.p1_sp3.data
        task.p1_sp5 = form.p1_sp5.data
        task.p1_sp8 = form.p1_sp8.data
        task.p1_sp13 = form.p1_sp13.data
        task.p1_sp21 = form.p1_sp21.data
        task.p1_sp55 = form.p1_sp55.data
        task.p2_sp0 = form.p2_sp0.data
        task.p2_sp1 = form.p2_sp1.data
        task.p2_sp2 = form.p2_sp2.data
        task.p2_sp3 = form.p2_sp3.data
        task.p2_sp5 = form.p2_sp5.data
        task.p2_sp8 = form.p2_sp8.data
        task.p2_sp13 = form.p2_sp13.data
        task.p2_sp21 = form.p2_sp21.data
        task.p2_sp55 = form.p2_sp55.data
        task.p3_sp0 = form.p3_sp0.data
        task.p3_sp1 = form.p3_sp1.data
        task.p3_sp2 = form.p3_sp2.data
        task.p3_sp3 = form.p3_sp3.data
        task.p3_sp5 = form.p3_sp5.data
        task.p3_sp8 = form.p3_sp8.data
        task.p3_sp13 = form.p3_sp13.data
        task.p3_sp21 = form.p3_sp21.data
        task.p3_sp55 = form.p3_sp55.data
        task.p4_sp0 = form.p4_sp0.data
        task.p4_sp1 = form.p4_sp1.data
        task.p4_sp2 = form.p4_sp2.data
        task.p4_sp3 = form.p4_sp3.data
        task.p4_sp5 = form.p4_sp5.data
        task.p4_sp8 = form.p4_sp8.data
        task.p4_sp13 = form.p4_sp13.data
        task.p4_sp21 = form.p4_sp21.data
        task.p4_sp55 = form.p4_sp55.data
        task.p5_sp0 = form.p5_sp0.data
        task.p5_sp1 = form.p5_sp1.data
        task.p5_sp2 = form.p5_sp2.data
        task.p5_sp3 = form.p5_sp3.data
        task.p5_sp5 = form.p5_sp5.data
        task.p5_sp8 = form.p5_sp8.data
        task.p5_sp13 = form.p5_sp13.data
        task.p5_sp21 = form.p5_sp21.data
        task.p5_sp55 = form.p5_sp55.data

        db.session.commit()

        task.project_duration = int(calculate_project_duration(
            task.num_people,
            task.p1_sp0, task.p1_sp1, task.p1_sp2, task.p1_sp3, task.p1_sp5, task.p1_sp8, task.p1_sp13, task.p1_sp21,
            task.p1_sp55, task.p2_sp0, task.p2_sp1, task.p2_sp2, task.p2_sp3, task.p2_sp5, task.p2_sp8, task.p2_sp13,
            task.p2_sp21, task.p2_sp55, task.p3_sp0, task.p3_sp1, task.p3_sp2, task.p3_sp3, task.p3_sp5, task.p3_sp8,
            task.p3_sp13, task.p3_sp21, task.p3_sp55, task.p4_sp0, task.p4_sp1, task.p4_sp2, task.p4_sp3, task.p4_sp5,
            task.p4_sp8, task.p4_sp13, task.p4_sp21, task.p4_sp55, task.p5_sp0, task.p5_sp1, task.p5_sp2, task.p5_sp3,
            task.p5_sp5, task.p5_sp8, task.p5_sp13, task.p5_sp21, task.p5_sp55))

        task.ending_project_date = calculate_date(form.start_project_date, task.project_duration)

        db.session.commit()

    return render_template('edit_project.html', title='Изменение проекта', form=form, task=task)


@users.route('/assign_tasks', methods=['POST'])
@login_required
def assign_tasks():
    tasks = Task.query.all()
    users = Users.query.all()

    for task in tasks:
        for i in range(1, 6):
            for j in [8, 5, 3, 2, 1, 0]:
                task_name = f"p{i}_sp{j}"
                current_assignments_count = TaskAssignment.query.filter_by(task_id=task.id, task_name=task_name).count()
                total_assignments_count = getattr(task, task_name)
                if current_assignments_count < total_assignments_count:
                    assignments_to_add = total_assignments_count - current_assignments_count
                    user_index = 0
                    for _ in range(assignments_to_add):
                        user = users[user_index % len(users)]
                        new_assignment = TaskAssignment(
                            task_name=task_name,
                            task_id=task.id,
                            user_id=user.id,
                            deadline=task.ending_project_date
                        )
                        db.session.add(new_assignment)
                        user_index += 1

    db.session.commit()
    return redirect(url_for('users.index'))


import pandas as pd
from math import ceil


@users.route('/distribute_tasks_per_week', methods=['POST'])
@login_required
def distribute_tasks_per_week():
    users = Users.query.all()
    hours_per_week = 20

    # Чтение данных из файла Excel
    task_durations_data = pd.read_excel('results.xlsx', sheet_name='priority_sp_stats')

    # Преобразование данных в словарь
    task_durations = {}
    for index, row in task_durations_data.iterrows():
        priority = row['Приоритет'].lower()
        sp = row['Сложность в SP']
        task_type = f"{priority}_sp{sp}"
        if sp not in [13, 21, 55]:
            task_durations[task_type] = row['Среднее время выполнения в часах']

    for user in users:
        user_assignments = TaskAssignment.query.filter_by(user_id=user.id).order_by(TaskAssignment.deadline).all()
        remaining_hours = hours_per_week
        week_num = 1

        for assignment in user_assignments:
            task_name = assignment.task_name
            task_hours = task_durations.get(task_name, 0)

            if task_hours > remaining_hours:
                weeks_needed = ceil(task_hours / hours_per_week)
                assignment.hours = remaining_hours
                assignment.week_num = week_num
                remaining_hours = 0
                task_hours -= remaining_hours
                week_num += weeks_needed
            else:
                assignment.hours = task_hours
                assignment.week_num = week_num
                remaining_hours -= task_hours
                task_hours = 0

            db.session.commit()

    return redirect(url_for('users.index'))


@users.route('/update_task_assignment', methods=['POST'])
@login_required
def update_task_assignment():
    if request.method == 'POST':
        flash_displayed = False
        for assignment in current_user.assigned_tasks:
            assignment_id = request.form.get(f'assignment_id_{assignment.id}')
            task_assignment = TaskAssignment.query.get(assignment_id)
            if task_assignment:
                task_assignment.done = True if request.form.get(f'task_assignment_{assignment.id}') else False
                db.session.commit()
                if not flash_displayed:
                    flash('Состояние задания успешно обновлено', 'success')
                    flash_displayed = True
            else:
                if not flash_displayed:
                    flash('Задание не найдено', 'error')
                    flash_displayed = True
    return redirect(url_for('users.tasks_page'))


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
        try:
            TaskAssignment.query.filter_by(task_id=task_id).delete()
            db.session.delete(task)
            db.session.commit()
            flash('Проект удален успешно', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Ошибка удаления проекта: сначала удалите связанные задания', 'error')
    else:
        flash('Проект не найден', 'error')

    return redirect(url_for('users.index'))


@users.route('/delete_assignment/<int:task_id>', methods=['POST'])
@login_required
def delete_assignment(task_id):
    deleted_assignments = TaskAssignment.query.filter_by(task_id=task_id).all()

    if deleted_assignments:
        for assignment in deleted_assignments:
            db.session.delete(assignment)
        db.session.commit()
        flash('Распределения удалены успешно', 'success')
    else:
        flash('Распределения не найдены', 'error')

    return redirect(url_for('users.index'))


@users.route('/users')
@login_required
def users_page():
    users = Users.query.all()
    return render_template('users.html', users=users)


@users.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        kpd = request.form['kpd']

        if kpd == '':
            kpd = None

        new_user = Users(email=email, password=password, name=name, kpd=kpd)
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('users.users_page'))


@users.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удален', 'success')
    return redirect(url_for('users.users_page'))


@users.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    if request.method == 'POST':
        user.email = request.form.get('email', user.email)
        user.password = request.form.get('password', user.password)
        user.name = request.form.get('name', user.name)
        user.kpd = request.form.get('kpd', user.kpd)
        if user.kpd == '':
            user.kpd = None
        db.session.commit()
        flash('Информация о пользователе успешно обновлена', 'success')
    return render_template('edit_user.html', user=user)


@users.route('/tasks', methods=['GET'])
@login_required
def tasks_page():
    form = TaskForm()

    tasks = TaskAssignment.query.filter_by(user_id=current_user.id).all()

    return render_template('tasks.html', title='Tasks', user=current_user, tasks=tasks, form=form)


