import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager,
                         current_user,
                         login_user,
                         logout_user,
                         login_required
)
from .admin.routes import admin
from .models import create_db, session, User, Item
from datetime import datetime
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()

app = Flask(__name__)
app.register_blueprint(admin)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

create_db()


@app.context_processor
def inject():
    return {"now": datetime.utcnow()}


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route("/")
def home():
    items = session.query(Item).all()
    return render_template("home_not_admin.html", items=items)


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = session.query(User).filter_by(email=email).first()
        if not user:
            flash(f"User with email {email} does not exist.<br> <a href={url_for('register')}>Register</a>", "error")
            return redirect(url_for("login"))
        elif check_password_hash(user.password, form.password.data):
            load_user(user=user)
            return redirect(url_for("home"))
        else:
            flash("Email or password are incorrect!", "error")
            return redirect(url_for("login"))

    else:
        return render_template("login_not_admin.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        if user:
            flash(f"User with email {user.email} exists.<br> <a href={url_for('login')}>Login</a>", "error")
            return redirect(url_for("register"))
        new_user = User(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data
        )
        session.add(new_user)
        session.commit()

        flash("You have successfully registered! You can now login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)



