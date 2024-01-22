from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100,
                                                                            message="Пароль должен быть от 4 до 100 "
                                                                                    "символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class TaskForm(FlaskForm):
    name_project = StringField('Название проекта', validators=[DataRequired()])
    num_people = IntegerField('Количество участников', validators=[DataRequired()])
    start_date_project = DateField('Дата начала проекта', validators=[DataRequired()])
    p1_sp0 = IntegerField('P1 SP 0', default=0)
    p1_sp1 = IntegerField('P1 SP 1', default=0)
    p1_sp2 = IntegerField('P1 SP 2', default=0)
    p1_sp3 = IntegerField('P1 SP 3', default=0)
    p1_sp5 = IntegerField('P1 SP 5', default=0)
    p1_sp8 = IntegerField('P1 SP 8', default=0)
    p1_sp55 = IntegerField('P2 SP 55', default=0)
    p2_sp0 = IntegerField('P2 SP 0', default=0)
    p2_sp1 = IntegerField('P2 SP 1', default=0)
    p2_sp2 = IntegerField('P2 SP 2', default=0)
    p2_sp3 = IntegerField('P2 SP 3', default=0)
    p2_sp5 = IntegerField('P2 SP 5', default=0)
    p2_sp8 = IntegerField('P2 SP 8', default=0)
    p2_sp55 = IntegerField('P2 SP 55', default=0)
    p3_sp0 = IntegerField('P3 SP 0', default=0)
    p3_sp1 = IntegerField('P3 SP 1', default=0)
    p3_sp2 = IntegerField('P3 SP 2', default=0)
    p3_sp3 = IntegerField('P3 SP 3', default=0)
    p3_sp5 = IntegerField('P3 SP 5', default=0)
    p3_sp8 = IntegerField('P3 SP 8', default=0)
    p3_sp55 = IntegerField('P3 SP 55', default=0)
    p4_sp0 = IntegerField('P4 SP 0', default=0)
    p4_sp1 = IntegerField('P4 SP 1', default=0)
    p4_sp2 = IntegerField('P4 SP 2', default=0)
    p4_sp3 = IntegerField('P4 SP 3', default=0)
    p4_sp5 = IntegerField('P4 SP 5', default=0)
    p4_sp8 = IntegerField('P4 SP 8', default=0)
    p4_sp55 = IntegerField('P4 SP 55', default=0)
    p5_sp0 = IntegerField('P5 SP 0', default=0)
    p5_sp1 = IntegerField('P5 SP 1', default=0)
    p5_sp2 = IntegerField('P5 SP 2', default=0)
    p5_sp3 = IntegerField('P5 SP 3', default=0)
    p5_sp5 = IntegerField('P5 SP 5', default=0)
    p5_sp8 = IntegerField('P5 SP 8', default=0)
    p5_sp55 = IntegerField('P5 SP 55', default=0)
    submit = SubmitField('Submit')