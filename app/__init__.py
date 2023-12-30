from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__, static_url_path="/static")

app.config["SECRET_KEY"] = os.urandom(255)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_PORT"] = 8111
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Mamank546"
app.config["MYSQL_DB"] = "sok"

mysql = MySQL(app)


from app.routes import user_routes, admin_routes, main
