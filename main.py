import os
from __init__ import app
from __init__ import db
from app.routes import users, tasks
from app.models import Admins, Users
from werkzeug.security import generate_password_hash


app.register_blueprint(users)
app.register_blueprint(tasks)


def create_admin_user():
    admin_email = "vip.polyakov1911@bk.ru"
    admin_password = "Zxcasd1234"

    existing_admin = Admins.query.filter_by(email=admin_email).first()
    if not existing_admin:
        hashed_password = generate_password_hash(admin_password)
        admin_user = Admins(email=admin_email, password=hashed_password, name="Admin")
        db.session.add(admin_user)
        db.session.commit()


def create_user():
    user_email = "vip.polyakov1911@bk.ru"
    user_password = "Zxcasd1234"

    existing_user = Users.query.filter_by(email=user_email).first()
    if not existing_user:
        hashed_password = generate_password_hash(user_password)
        user = Users(email=user_email, password=hashed_password, name="Admin")
        db.session.add(user)
        db.session.commit()


def create_user2():
    user_email = "vip.polyakov@bk.ru"
    user_password = "Zxcasd1234"

    existing_admin = Users.query.filter_by(email=user_email).first()
    if not existing_admin:
        hashed_password = generate_password_hash(user_password)
        user = Users(email=user_email, password=hashed_password, name="Admin")
        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            create_admin_user()
            create_user()
            create_user2()
            print('ok')
    except Exception as e:
        print(f"Error during table creation: {str(e)}")
    app.run(debug=True)