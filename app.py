from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from model import db, User
from form import RegistrationForm
import hashlib
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)
app.secret_key = b"d5097495d6eb4072e854e2503c54ef76d755219a06a636545be3b30226ee4ddd"

with app.app_context():
    db.create_all()

csrf = CSRFProtect(app)

@app.route("/")
def index():
    return redirect(url_for("registration"))

@app.route("/registration/", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if request.method == "POST" and form.validate():
        name = form.username.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        print(name, surname, email, password)
        salt = os.urandom(32)
        password_protection = password
        key = hashlib.pbkdf2_hmac(
            "sha256", password_protection.encode("utf-8"), salt, 1000, dklen=60
        )
        user = User(username=name, surname=surname, email=email, password=key)
        print(user)
        db.session.add(user)
        db.session.commit()
        return (
            f"<h1>Username: {name} добавлен в базу !</h1>"
            f"<h2>Date:<br>{user}</h2><br>"
        )
    return render_template("registration.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
