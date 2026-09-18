from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

print("MySQL Database Connected Successfully!")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)