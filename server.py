import os

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

import campus_views
import views
from database import Database


UPLOAD_FOLDER = '/media'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}
SECRET_KEY = os.urandom(32)
lm = LoginManager()
csrf = CSRFProtect()
lm.login_view = "views.login_page"


def init_db(db_url):
    db = Database(db_url)
    # try:
    #     db.add_person(
    #         Person("11111111110", "Ahmet", "Mehmet", "+905508004060", "mehmet19@itu.edu.tr",
    #                "password", 2, "Fatma", "Ali", "M", "Istanbul", "01-01-2000", "Istanbul",
    #                "Sariyer"))
    #     db.add_person(
    #         Person("12111111110", "Veli", "Mehmet", "+905508004060", "veli19@itu.edu.tr",
    #                "password", 0, "Fatma", "Ali", "M", "Istanbul", "01-01-2000", "Istanbul",
    #                "Sariyer"))
    #     db.add_person(
    #         Person("13111111110", "Deli", "Mehmet", "+905508004060", "deli19@itu.edu.tr",
    #                "password", 5, "Fatma", "Ali", "M", "Istanbul", "01-01-2000", "Istanbul",
    #                "Sariyer"))
    #     db.add_person(
    #         Person("14111111110", "Ucar", "Mehmet", "+905508004060", "ucar19@itu.edu.tr",
    #                "password", 3, "Fatma", "Ali", "F", "Istanbul", "01-01-2000", "Istanbul",
    #                "Sariyer"))
    #     db.add_person(
    #         Person("15111111110", "Ucmaz", "Mehmet", "+905508004060", "ucmaz19@itu.edu.tr",
    #                "password", 5, "Fatma", "Ali", "M", "Istanbul", "01-01-2000", "Istanbul",
    #                "Sariyer"))
    #     db.add_person(
    #         Person("16111111110", "Ucarmi", "Mehmet", "+905508004060", "ucarmi19@itu.edu.tr",
    #                "password", 1, "Fatma", "Ali", "F", "Istanbul", "01-01-2000", "Istanbul",
    #                "Sariyer"))
    # except dbapi2.errors.UniqueViolation:
    #     print("A person with the same TR ID already exists")
    return db


def create_app(db_url):
    app = Flask(__name__, static_url_path="/static")
    # Triangle(app)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config.from_object("settings")
    csrf.init_app(app)

    app.add_url_rule("/", view_func=views.landing_page,
                     methods=['GET', 'POST'])
    app.add_url_rule("/login", view_func=views.login_page,
                     methods=['GET', 'POST'])
    app.add_url_rule("/logout", view_func=views.logout_page,
                     methods=['GET', 'POST'])
    app.add_url_rule("/people", view_func=views.people_page,
                     methods=['GET', 'POST'])
    app.add_url_rule("/people/<tr_id>",
                     view_func=views.person_page, methods=['GET', 'POST'])
    app.add_url_rule("/campuses/campus",
                     view_func=campus_views.campus, methods=['GET', 'POST'])
    app.add_url_rule("/test",
                     view_func=views.test_page, methods=['GET', 'POST'])
    db = init_db(db_url)
    app.config["db"] = db
    lm.init_app(app)
    lm.login_view = "login_page"

    @lm.user_loader
    def load_user(id):
        return db.get_user(id)

    return app


db_url = os.getenv("DATABASE_URL")
app = create_app(db_url)

if __name__ == "__main__":
    host = app.config.get("HOST")
    port = app.config.get("PORT")
    debug = app.config.get("DEBUG")
    app.run(host=host, port=port, debug=debug)
