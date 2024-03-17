import os
from __init__ import app
from __init__ import db
from app.routes import users, tasks
from app.models import Admins, Users


app.register_blueprint(users)
app.register_blueprint(tasks)


def create_admin_user():
    admin_email = "vip.polyakov1911@bk.ru"
    admin_password = "Zxcasd1234"

    existing_admin = Admins.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin_user = Admins(email=admin_email, password=admin_password, name="Admin")
        db.session.add(admin_user)
        db.session.commit()


if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            create_admin_user()
            print('ok')
    except Exception as e:
        print(f"Error during table creation: {str(e)}")
    app.run(debug=True)