import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request
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
from itsdangerous import URLSafeTimedSerializer
from .utils import send_confirmation_email, mail

load_dotenv()

app = Flask(__name__)
app.register_blueprint(admin)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

Bootstrap(app)
mail.init_app(app)
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
    return render_template("home.html", items=items)


@app.route("/login", methods=["POST", "GET"])
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
            login_user(user=user)
            return redirect(url_for("home"))
        else:
            flash("Email or password are incorrect!", "error")
            return redirect(url_for("login"))

    else:
        return render_template("login.html", form=form)


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
            password=generate_password_hash(form.password.data)
        )

        try:
            session.add(new_user)
            session.commit()
            flash("You have successfully registered! You can now login.", "success")
            return redirect(url_for("login"))
        except Exception as exc:
            return exc
        finally:
            session.close()

    return render_template("register.html", form=form)


@app.route("/confirm/<token>")
def confirm_email(token):
    try:
        serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        email = serializer.loads(token, salt="email-confirmation_salt", max_age=3600)
    except:
        flash("The confirmation link is invalid or spent", "error")
        return redirect(url_for("login"))
    user = session.query(User).filter_by(email=email).first()
    if user.email_confirmed:
        flash("Account already confirmed. Please login!", "success")
    else:
        user.email_confirmed = True
        try:
            session.add(user)
            session.commit()
            flash("Email address successfully confimed", "success")
        except Exception as exc:
            raise exc
        finally:
            session.close()
    return redirect(url_for("login"))


@app.route("/resend")
@login_required
def resend():
    send_confirmation_email(current_user.email)
    logout_user()
    flash("Confirmation email was sent successfully", "success")
    return redirect(url_for("login"))


@app.route("/add/<id>", methods=["POST"])
def add_to_cart(id):
    if not current_user.is_authenticated:
        flash("you must login first!")
        return render_template(url_for("home"))
    item = session.query(Item).get(id)
    if request.method == "POST":
        quantity = request.form["quantity"]
        current_user.add_to_cart(id, quantity)
        flash(f'''{item.name} successfully added to the <a href=cart>cart</a>.<br> <a href={url_for("cart")}>view cart!</a>''','success')
        return redirect(url_for("home"))


@app.route("/cars")
@login_required
def cars():
    price = 0
    quantity = []
    items = []
    price_ids = []
    for cart in current_user.cart:
        items.append(cars.item)
        quantity.append(cart.quantity)
        price_id_dict = {
            "price": cart.item.price_id,
            "quantity": cart.quantity
        }
        price_ids.append(price_id_dict)
        price += cart.item.price * cart.quantity
    return render_template("cart.html", items=items, quantity=quantity, price_ids=price_ids, price=price)


@app.route("/orders")
@login_required
def orders():
    return render_template("orders.html", orders=current_user.orders)


@app.route("/remove/<id>/<quantity>")
@login_required
def remove(id, quantity):
    current_user.remove_from_cart(id, quantity)
    return redirect(url_for("cart"))

@app.route("/cart")
@login_required
def cart():
    price = 0
    quantity = []
    items = []
    price_ids = []
    for cart in current_user.cart:
        items.append(cart.item)
        quantity.append(cart.quantity)
        price_id_dict = {
            "price": cart.item.price_id,
            "quantity": cart.quantity
        }
        price_ids.append(price_id_dict)
        price += cart.item.price * cart.quantity
    return render_template("cart.html", items=items, quantity=quantity, price_ids=price_ids, price=price)
@app.route("/item/<int:id>")
def item(id):
    item = session.query(Item).get(id)
    return render_template("item.html", item=item)


@app.route("/search")
def search():
    query = request.args["query"]
    search = f"%{query}%"
    items = session.query(Item).filter(Item.name.like(search)).all
    return render_template("home.html", items=items, search=True, query=query)


@app.route("/payment_success")
def payment_success():
    return render_template("success.html")


@app.route("/payment_failure")
def payment_failure():
    return render_template("failure.html")






