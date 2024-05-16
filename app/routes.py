from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import current_user, login_user, login_required, logout_user
from __init__ import login_manager
from .__init__ import users
from .models import Users, Admins, db, Task, TaskAssignment, UsersPro, TaskAssignmentPro, HardTasks, \
    TaskAssignmentFinal, TaskPro
from .forms import LoginForm, TaskForm
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from math import ceil
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import logging
from itertools import cycle
import math

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
                                p5_sp55 * task_type_avg_time.get('P5_SP55', 0)) / num_people) / 2.32

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

    while workdays_count <= project_duration:
        if current_day.weekday() not in [5, 6]:
            workdays_count += 1
        current_day += timedelta(days=1)

    end_date = current_day

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

    task_pro = TaskPro.query.all()

    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=current_user, form=form, tasks=tasks, task_pro=task_pro)
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


@users.route('/assign_and_distribute_tasks', methods=['POST'])
@login_required
def assign_and_distribute_tasks():
    tasks = Task.query.all()
    users = Users.query.all()
    hours_per_week = 11.6

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

    # Создаем цикл пользователей, чтобы равномерно распределить задачи между ними
    users_cycle = cycle(users)

    for task in tasks:
        for i in range(1, 6):
            for j in [8, 5, 3, 2, 1, 0]:
                task_name = f"p{i}_sp{j}"
                current_assignments_count = TaskAssignment.query.filter_by(task_id=task.id, task_name=task_name).count()
                total_assignments_count = getattr(task, task_name)
                if current_assignments_count < total_assignments_count:
                    assignments_to_add = total_assignments_count - current_assignments_count
                    for _ in range(assignments_to_add):
                        user = next(users_cycle)
                        new_assignment = TaskAssignment(
                            task_name=task_name,
                            task_id=task.id,
                            user_id=user.id,
                            start=task.start_project_date,
                            deadline=task.ending_project_date
                        )
                        db.session.add(new_assignment)

    # Разбиваем задачи по неделям
    for user in users:
        user_assignments = TaskAssignment.query.filter_by(user_id=user.id).order_by(TaskAssignment.deadline).all()
        remaining_hours = hours_per_week
        week_num = 1

        for assignment in user_assignments:
            task_name = assignment.task_name
            task_hours = task_durations.get(task_name, 0)

            weeks_needed = ceil(task_hours / hours_per_week)
            assignment.week_num = week_num + weeks_needed - 1
            if task_hours > remaining_hours:
                assignment.hours = remaining_hours
                remaining_hours = hours_per_week * weeks_needed - task_hours % hours_per_week
                week_num += weeks_needed
            else:
                assignment.hours = task_hours
                remaining_hours -= task_hours

    db.session.commit()
    return redirect(url_for('users.index'))


@login_manager.user_loader
def load_user(user_id):
    if Admins.query.get(int(user_id)):
        return Admins.query.get(int(user_id))
    else:
        return Users.query.get(int(user_id))


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        admin = Admins.query.filter_by(email=email).first()

        if admin and admin.password == password:
            login_user(admin)
            return redirect(url_for('users.index'))
        elif user and user.password == password:
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
    deleted_assignments = TaskAssignmentFinal.query.filter_by(task_id=task_id).all()
    deleted_tasks = TaskPro.query.filter_by(task_id=task_id).all()
    deleted_hard = TaskAssignmentPro.query.filter_by(task_id=task_id).all()

    if task:
        if deleted_assignments:
            for assignment in deleted_assignments:
                db.session.delete(assignment)
            db.session.commit()
            flash('Распределения удалены успешно', 'success')
        else:
            flash('Распределения не найдены', 'error')

        if deleted_tasks:
            for assignment in deleted_tasks:
                db.session.delete(assignment)
            db.session.commit()
            flash('Финальные рассчеты удалены успешно', 'success')
        else:
            flash('Финальные рассчеты не найдены', 'error')

        if deleted_hard:
            for assignment in deleted_hard:
                db.session.delete(assignment)
            db.session.commit()
            flash('Финальные рассчеты удалены успешно', 'success')
        else:
            flash('Финальные рассчеты не найдены', 'error')

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
    user2 = UsersPro.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.delete(user2)
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


@users.route('/update_kpd_from_excel', methods=['POST'])
@login_required
def update_kpd_from_excel():
    try:
        df = pd.read_excel('results.xlsx', sheet_name='participants_stats')
    except FileNotFoundError:
        flash('Файл results.xlsx не найден', 'error')
        return redirect(url_for('users.users_page'))

    all_users = Users.query.all()
    for user in all_users:
        user.kpd = 1
        db.session.commit()

    # Затем переписываем кпд для пользователей из results.xlsx
    for index, row in df.iterrows():
        user_name = row['Участник']
        kpd = row['Total_KPD']

        # Поиск пользователя в таблице Users по имени
        user = Users.query.filter_by(name=user_name).first()

        if user:
            # Обновление кпд пользователя в таблице Users
            user.kpd = kpd
            db.session.commit()
        else:
            continue

    # Добавление всех пользователей в таблицу UsersPro
    for user in all_users:
        user_pro = UsersPro.query.filter_by(name=user.name).first()

        if not user_pro:
            user_pro = UsersPro(id=user.id, name=user.name, email=user.email, password=user.password)
            db.session.add(user_pro)
            db.session.commit()
        else:
            # Если пользователь уже существует, обновляем email и пароль
            user_pro.email = user.email
            user_pro.password = user.password
            db.session.commit()

    # Обновление KPD для каждого пользователя в таблице UsersPro
    for index, row in df.iterrows():
        user_name = row['Участник']
        kpd = row['Total_KPD']

        user_pro = UsersPro.query.filter_by(name=user_name).first()

        if user_pro:
            user_pro.KPD_P1_SP1 = row.get('KPD_P1_SP1', 1)
            user_pro.KPD_P2_SP0 = row.get('KPD_P2_SP0', 1)
            user_pro.KPD_P2_SP1 = row.get('KPD_P2_SP1', 1)
            user_pro.KPD_P2_SP2 = row.get('KPD_P2_SP2', 1)
            user_pro.KPD_P2_SP3 = row.get('KPD_P2_SP3', 1)
            user_pro.KPD_P2_SP5 = row.get('KPD_P2_SP5', 1)
            user_pro.KPD_P3_SP0 = row.get('KPD_P3_SP0', 1)
            user_pro.KPD_P3_SP1 = row.get('KPD_P3_SP1', 1)
            user_pro.KPD_P3_SP2 = row.get('KPD_P3_SP2', 1)
            user_pro.KPD_P3_SP3 = row.get('KPD_P3_SP3', 1)
            user_pro.KPD_P3_SP5 = row.get('KPD_P3_SP5', 1)
            user_pro.KPD_P3_SP8 = row.get('KPD_P3_SP8', 1)
            user_pro.KPD_P4_SP0 = row.get('KPD_P4_SP0', 1)
            user_pro.KPD_P4_SP1 = row.get('KPD_P4_SP1', 1)
            user_pro.KPD_P4_SP2 = row.get('KPD_P4_SP2', 1)
            user_pro.KPD_P4_SP3 = row.get('KPD_P4_SP3', 1)
            user_pro.KPD_P4_SP5 = row.get('KPD_P4_SP5', 1)
            user_pro.KPD_P4_SP8 = row.get('KPD_P4_SP8', 1)
            user_pro.KPD_P4_SP13 = row.get('KPD_P4_SP13', 1)
            user_pro.KPD_P4_SP55 = row.get('KPD_P4_SP55', 1)
            user_pro.KPD_P5_SP1 = row.get('KPD_P5_SP1', 1)
            user_pro.KPD_P5_SP2 = row.get('KPD_P5_SP2', 1)
            user_pro.KPD_P5_SP5 = row.get('KPD_P5_SP5', 1)
            user_pro.KPD_P5_SP3 = row.get('KPD_P5_SP3', 1)
            user_pro.KPD_P5_SP8 = row.get('KPD_P5_SP8', 1)
            # Заполните остальные атрибуты аналогичным образом
            db.session.commit()
        else:
            flash(f'Пользователь с именем {user_name} не найден в таблице UsersPro', 'error')
    all_users_pro = UsersPro.query.all()

    for user_pro in all_users_pro:
        if user_pro.KPD_P1_SP1 is None or np.isnan(user_pro.KPD_P1_SP1):
            user_pro.KPD_P1_SP1 = 1
        if user_pro.KPD_P2_SP0 is None or np.isnan(user_pro.KPD_P2_SP0):
            user_pro.KPD_P2_SP0 = 1
        if user_pro.KPD_P2_SP1 is None or np.isnan(user_pro.KPD_P2_SP1):
            user_pro.KPD_P2_SP1 = 1
        if user_pro.KPD_P2_SP2 is None or np.isnan(user_pro.KPD_P2_SP2):
            user_pro.KPD_P2_SP2 = 1
        if user_pro.KPD_P2_SP3 is None or np.isnan(user_pro.KPD_P2_SP3):
            user_pro.KPD_P2_SP3 = 1
        if user_pro.KPD_P2_SP5 is None or np.isnan(user_pro.KPD_P2_SP5):
            user_pro.KPD_P2_SP5 = 1
        if user_pro.KPD_P3_SP0 is None or np.isnan(user_pro.KPD_P3_SP0):
            user_pro.KPD_P3_SP0 = 1
        if user_pro.KPD_P3_SP1 is None or np.isnan(user_pro.KPD_P3_SP1):
            user_pro.KPD_P3_SP1 = 1
        if user_pro.KPD_P3_SP2 is None or np.isnan(user_pro.KPD_P3_SP2):
            user_pro.KPD_P3_SP2 = 1
        if user_pro.KPD_P3_SP3 is None or np.isnan(user_pro.KPD_P3_SP3):
            user_pro.KPD_P3_SP3 = 1
        if user_pro.KPD_P3_SP5 is None or np.isnan(user_pro.KPD_P3_SP5):
            user_pro.KPD_P3_SP5 = 1
        if user_pro.KPD_P3_SP8 is None or np.isnan(user_pro.KPD_P3_SP8):
            user_pro.KPD_P3_SP8 = 1
        if user_pro.KPD_P4_SP0 is None or np.isnan(user_pro.KPD_P4_SP0):
            user_pro.KPD_P4_SP0 = 1
        if user_pro.KPD_P4_SP1 is None or np.isnan(user_pro.KPD_P4_SP1):
            user_pro.KPD_P4_SP1 = 1
        if user_pro.KPD_P4_SP2 is None or np.isnan(user_pro.KPD_P4_SP2):
            user_pro.KPD_P4_SP2 = 1
        if user_pro.KPD_P4_SP3 is None or np.isnan(user_pro.KPD_P4_SP3):
            user_pro.KPD_P4_SP3 = 1
        if user_pro.KPD_P4_SP5 is None or np.isnan(user_pro.KPD_P4_SP5):
            user_pro.KPD_P4_SP5 = 1
        if user_pro.KPD_P4_SP8 is None or np.isnan(user_pro.KPD_P4_SP8):
            user_pro.KPD_P4_SP8 = 1
        if user_pro.KPD_P4_SP13 is None or np.isnan(user_pro.KPD_P4_SP13):
            user_pro.KPD_P4_SP13 = 1
        if user_pro.KPD_P4_SP55 is None or np.isnan(user_pro.KPD_P4_SP55):
            user_pro.KPD_P4_SP55 = 1
        if user_pro.KPD_P5_SP1 is None or np.isnan(user_pro.KPD_P5_SP1):
            user_pro.KPD_P5_SP1 = 1
        if user_pro.KPD_P5_SP2 is None or np.isnan(user_pro.KPD_P5_SP2):
            user_pro.KPD_P5_SP2 = 1
        if user_pro.KPD_P5_SP3 is None or np.isnan(user_pro.KPD_P5_SP3):
            user_pro.KPD_P5_SP3 = 1
        if user_pro.KPD_P5_SP5 is None or np.isnan(user_pro.KPD_P5_SP5):
            user_pro.KPD_P5_SP5 = 1
        if user_pro.KPD_P5_SP8 is None or np.isnan(user_pro.KPD_P5_SP8):
            user_pro.KPD_P5_SP8 = 1
        db.session.commit()

    return redirect(url_for('users.users_page'))


@users.route('/vacation_page/<int:user_id>', methods=['GET', 'POST'])
@login_required
def vacation_page(user_id):
    user_pro = UsersPro.query.get(user_id)
    if not user_pro:
        flash('Пользователь не найден', 'error')
        return redirect(url_for('users.users_page'))

    user = Users.query.get(user_id)

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        user_pro.vacation_start = start_date
        user_pro.vacation_end = end_date
        db.session.commit()

        flash('Даты отпуска успешно сохранены', 'success')
        return render_template('vacation_page.html', user_id=user_id, user=user, start_date=start_date, end_date=end_date)

    start_date = user_pro.vacation_start
    end_date = user_pro.vacation_end

    return render_template('vacation_page.html', user_id=user_id, user=user, start_date=start_date, end_date=end_date)


@users.route('/assign_hard_tasks', methods=['GET', 'POST'])
@login_required
def insert_hard_tasks():
    HardTasks.query.filter_by(assigned=False).delete()

    tasks = Task.query.all()

    for task in tasks:
        for column in task.__table__.columns:
            if column.name in ['p1_sp13', 'p1_sp21', 'p1_sp55', 'p2_sp13', 'p2_sp21', 'p2_sp55', 'p3_sp13',
                               'p3_sp21', 'p3_sp55', 'p4_sp13', 'p4_sp21', 'p4_sp55', 'p5_sp13', 'p5_sp21', 'p5_sp55']:
                priority_value = getattr(task, column.name)
                if priority_value > 0:
                    existing_true_count = HardTasks.query.filter_by(task_id=task.id, task_name=column.name,
                                                                    assigned=True).count()
                    remaining_priority_value = max(0, priority_value - existing_true_count)

                    for _ in range(remaining_priority_value):
                        hard_task = HardTasks(task_id=task.id, task_name=column.name, assigned=False)
                        db.session.add(hard_task)

    db.session.commit()

    hard_tasks = HardTasks.query.all()
    users_pro = UsersPro.query.all()

    return render_template('assign_hard_tasks.html', hard_tasks=hard_tasks, users_pro=users_pro)


@users.route('/final_assign_hard_task/<int:hard_task_id>', methods=['GET', 'POST'])
@login_required
def final_assign_hard_task(hard_task_id):
    hard_task = HardTasks.query.get_or_404(hard_task_id)
    users = UsersPro.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user')
        hours = request.form.get('hours')

        existing_assignment = TaskAssignmentPro.query.filter_by(hard_task_id=hard_task_id).first()

        if existing_assignment:
            db.session.delete(existing_assignment)
            db.session.commit()

        task_assignment = TaskAssignmentPro(
            task_id=hard_task.task_id,
            hard_task_id=hard_task_id,
            task_name=hard_task.task_name,
            user_id=user_id,
            hours=hours
        )

        db.session.add(task_assignment)
        db.session.commit()

        hard_task.assigned = True
        db.session.commit()

        flash('Task assigned successfully!', 'success')
        return render_template('final_assign_hard_task.html', hard_task=hard_task, users=users)

    return render_template('final_assign_hard_task.html', hard_task=hard_task, users=users)


@users.route('/delete_hard_assignment/<int:hard_task_id>', methods=['POST'])
@login_required
def delete_hard_assignment(hard_task_id):
    assignment = TaskAssignmentPro.query.filter_by(hard_task_id=hard_task_id).first()

    if assignment:
        db.session.delete(assignment)
        db.session.commit()

        hard_task = HardTasks.query.get_or_404(hard_task_id)
        hard_task.assigned = False
        db.session.commit()

    hard_tasks = HardTasks.query.all()

    return render_template('assign_hard_tasks.html', hard_tasks=hard_tasks)


@users.route('/assign_tasks_final', methods=['POST'])
@login_required
def assign_tasks_final():
    task_durations_data = pd.read_excel('results.xlsx', sheet_name='priority_sp_stats')
    # Преобразование данных в словарь
    task_durations = {}
    for index, row in task_durations_data.iterrows():
        priority = row['Приоритет'].lower()
        sp = row['Сложность в SP']
        task_type = f"{priority}_sp{sp}"
        if sp not in [13, 21, 55]:
            task_durations[task_type] = row['Среднее время выполнения в часах']

    # Получение списка всех заданий из таблицы TaskAssignment
    tasks = TaskAssignment.query.all()

    # Проходимся по каждому заданию из TaskAssignment и добавляем его в TaskAssignmentFinal
    for task in tasks:
        new_task_final = TaskAssignmentFinal(
            task_id=task.task_id,
            task_name=task.task_name,
            assigned=False
        )
        db.session.add(new_task_final)

    # Получение списка всех пользователей из таблицы UsersPro
    users = UsersPro.query.all()

    # Переменная для отслеживания предыдущей назначенной недели для каждого пользователя
    previous_weeks = {}

    # Расчет общего количества часов работы
    total_hours_required = sum(task_durations.values())

    # Проверяем, что общее количество часов больше нуля, прежде чем делить
    if total_hours_required > 0:
        # Расчет количества рабочих часов в неделю для каждого пользователя
        weekly_hours_per_user = total_hours_required / len(users)

        # Рассчитываем количество недель, необходимых для выполнения всех заданий
        total_weeks_required = math.ceil(total_hours_required / (weekly_hours_per_user * len(users)))

        # Создаем список заданий для каждого типа
        tasks_by_type = {task_type: [] for task_type in task_durations.keys()}

        # Группируем задания по типу
        for task_final in TaskAssignmentFinal.query.all():
            tasks_by_type[task_final.task_name].append(task_final)

        # Создаем словарь для хранения пользователей и их КПД
        users_kpd = {user.id: user for user in users}

        # Начинаем с первого пользователя
        current_user_index = 0

        # Проходимся по каждому типу заданий по приоритетам
        for task_type in sorted(tasks_by_type.keys()):
            tasks = tasks_by_type[task_type]
            users_with_kpd = [(user.id, getattr(user, f"KPD_{task_type}".upper(), 0)) for user in users]

            # Сортируем пользователей по КПД
            users_with_kpd.sort(key=lambda x: x[1], reverse=True)

            # Проходимся по заданиям этого типа
            for task_final in tasks:
                # Если задание уже назначено, пропускаем его
                if task_final.assigned:
                    continue

                # Получаем пользователя для назначения задания
                user_id, _ = users_with_kpd[current_user_index]
                current_user_index = (current_user_index + 1) % len(users_with_kpd)

                # Получаем количество часов, необходимых для выполнения этого типа задания
                hours_required = task_durations.get(task_type, 0)

                # Находим следующую доступную неделю для назначения задания
                next_week = previous_weeks.get(user_id, 0) + 1

                # Проверяем, находится ли неделя в промежутке отпусков для этого пользователя
                user = UsersPro.query.get(user_id)
                task = Task.query.first()  # Получаем первую запись из таблицы Task
                start_project_date = task.start_project_date
                if user and user.vacation_start and user.vacation_end:
                    vacation_start_week = (user.vacation_start - start_project_date).days // 7 + 1
                    vacation_end_week = (user.vacation_end - start_project_date).days // 7 + 1
                    if next_week >= vacation_start_week and next_week <= vacation_end_week:
                        # Если неделя находится в промежутке отпусков, переносим задание за этот период отпуска
                        next_week = vacation_end_week + 1

                # Обновляем данные задания в таблице TaskAssignmentFinal
                task_final.assigned = True
                task_final.hours = hours_required
                task_final.week_num = next_week
                task_final.user_id = user_id

                db.session.commit()

                # Обновляем значение предыдущей назначенной недели для этого пользователя
                previous_weeks[user_id] = next_week

        # Получение списка всех заданий из таблицы TaskAssignmentPro
        tasks_pro = TaskAssignmentPro.query.all()

        # Проходимся по каждому заданию из TaskAssignmentPro и добавляем его в TaskAssignmentFinal
        for task_pro in tasks_pro:
            task_type = f"{task_pro.task_name}"
            hours_required = task_pro.hours
            next_week = previous_weeks.get(task_pro.user_id, 0) + (hours_required/17.11)

            # Проверяем, находится ли неделя в промежутке отпусков для этого пользователя
            user = UsersPro.query.get(task_pro.user_id)
            task = Task.query.first()  # Получаем первую запись из таблицы Task
            start_project_date = task.start_project_date
            if user and user.vacation_start and user.vacation_end:
                vacation_start_week = (user.vacation_start - start_project_date).days // 7 + 1
                vacation_end_week = (user.vacation_end - start_project_date).days // 7 + 1
                if next_week >= vacation_start_week and next_week <= vacation_end_week:
                    # Если неделя находится в промежутке отпусков, переносим задание за этот период отпуска
                    next_week = vacation_end_week + 1

            new_pro_task_final = TaskAssignmentFinal(
                task_id=task_pro.task_id,
                task_name=task_type,
                assigned=True,
                hours=hours_required,
                week_num=next_week,
                user_id=task_pro.user_id
            )
            db.session.add(new_pro_task_final)

            db.session.commit()

        return redirect(url_for('users.index'))


@users.route('/delete_final_assignment/<int:task_id>', methods=['POST'])
@login_required
def delete_final_assignment(task_id):
    deleted_assignments = TaskAssignmentFinal.query.filter_by(task_id=task_id).all()
    deleted_tasks = TaskPro.query.filter_by(task_id=task_id).all()
    deleted_hard = TaskAssignmentPro.query.filter_by(task_id=task_id).all()

    if deleted_assignments:
        for assignment in deleted_assignments:
            db.session.delete(assignment)
        db.session.commit()
        flash('Распределения удалены успешно', 'success')
    else:
        flash('Распределения не найдены', 'error')

    if deleted_tasks:
        for assignment in deleted_tasks:
            db.session.delete(assignment)
        db.session.commit()
        flash('Финальные рассчеты удалены успешно', 'success')
    else:
        flash('Финальные рассчеты не найдены', 'error')

    if deleted_hard:
        for assignment in deleted_hard:
            db.session.delete(assignment)
        db.session.commit()
        flash('Финальные рассчеты удалены успешно', 'success')
    else:
        flash('Финальные рассчеты не найдены', 'error')

    return redirect(url_for('users.index'))


@users.route('/delete_vacation/<int:user_id>', methods=['POST'])
@login_required
def delete_vacation(user_id):
    user = UsersPro.query.get_or_404(user_id)

    if user:
        user.vacation_start = None
        user.vacation_end = None
        db.session.commit()
        flash('Отпуск удален успешно', 'success')
    else:
        flash('Пользователь не найден', 'error')

    return redirect(url_for('users.vacation_page', user_id=user_id))


@users.route('/calc_date', methods=['GET', 'POST'])
@login_required
def calc_date():
    try:
        # Получаем максимальное значение столбца week_num из TaskAssignmentFinal
        max_week_num = db.session.query(db.func.max(TaskAssignmentFinal.week_num)).scalar()

        # Получаем дату начала проекта из таблицы Task
        start_project_date = Task.query.first().start_project_date

        task_id = Task.query.first().id

        # Вычисляем конечную дату проекта
        ending_project_date = start_project_date + timedelta(weeks=max_week_num)

        # Обновляем информацию о проекте в таблице TaskPro
        task_pro = TaskPro.query.first()

        # Проверяем, есть ли записи в таблице TaskPro
        existing_task_pro = TaskPro.query.first()

        # Если в таблице нет записей, создаем новую запись
        if not existing_task_pro:
            new_task_pro = TaskPro(
                task_id=task_id,
                start_project_date=start_project_date,
                ending_project_date=ending_project_date,
                project_duration=calculate_working_days(start_project_date, ending_project_date)
            )
            db.session.add(new_task_pro)
            db.session.commit()

        else:

            # Обновляем информацию о проекте
            task_pro.task_id = Task.id
            task_pro.start_project_date = start_project_date
            task_pro.ending_project_date = ending_project_date
            task_pro.project_duration = calculate_working_days(start_project_date, ending_project_date)

            # Сохраняем изменения в базе данных
            db.session.commit()

        # Получаем результаты для вставки в таблицу HTML
        project_duration = TaskPro.query.first().project_duration
        ending_project_date_s = TaskPro.query.first().ending_project_date
        ending_project_date_str = ending_project_date_s.strftime("%Y-%m-%d")

        return redirect(url_for('users.index'))
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def calculate_working_days(start_date, end_date):
    total_work_days = 0
    current_date = start_date
    while current_date <= end_date:
        # Проверяем, является ли текущий день рабочим
        if current_date.weekday() < 5:
            total_work_days += 1
        # Переходим к следующему дню
        current_date += timedelta(days=1)
    return total_work_days


@users.route('/tasks', methods=['GET'])
def tasks_page():
    form = TaskForm()

    tasks = TaskAssignmentFinal.query.filter_by(user_id=current_user.id).order_by(TaskAssignmentFinal.week_num).all()

    # Получаем start_project_date из таблицы task
    task = Task.query.first()
    start_project_date = datetime.combine(task.start_project_date, datetime.min.time())  # Приводим к типу datetime
    start_project_date_page = start_project_date.date()

    # Определяем номер текущей недели
    current_week_number = (datetime.now() - start_project_date).days // 7 + 1

    return render_template('tasks.html', title='Tasks', user=current_user, tasks=tasks, form=form,
                           current_week_number=current_week_number, start_project_date=start_project_date_page)


@users.route('/update_task_assignment', methods=['POST'])
def update_task_assignment():
    if request.method == 'POST':
        task_assignment_ids = [key.split('_')[-1] for key in request.form.keys() if key.startswith('task_assignment_')]

        # Получаем все задания пользователя
        all_task_assignments = TaskAssignmentFinal.query.filter_by(user_id=current_user.id).all()

        # Обновляем состояние задания в базе данных
        for task_assignment in all_task_assignments:
            # Проверяем, был ли чекбокс для задания отмечен
            checkbox_name = 'task_assignment_' + str(task_assignment.id)
            if checkbox_name in request.form:
                task_assignment.done = True
            else:
                task_assignment.done = False  # Иначе, отмечаем как невыполненное (False)

        # Сохраняем изменения в базе данных
        db.session.commit()

        flash('Состояние заданий успешно обновлено.', 'success')
        return redirect(url_for('users.tasks_page'))
    else:
        return redirect(url_for('users.tasks_page'))



