from flask import Flask, render_template, request, redirect
from threading import Thread
from mqtt_client import start_mqtt
import os

from models import db, User, Log

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parkpi.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html", users=User.query.all(), logs=Log.query.all())


@app.post("/users")
def add_user():
    db.session.add(User(name=request.form["name"], code=request.form["code"]))
    db.session.commit()
    return redirect("/")


@app.post("/users/delete")
def del_user():
    User.query.filter_by(code=request.form["code"]).delete()
    db.session.commit()
    return redirect("/")


# starts the MQTT client in the background
Thread(target=start_mqtt, args=(app, db, User, Log), daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
