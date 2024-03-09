from flask import Blueprint, render_template, url_for, flash
from werkzeug.utils import redirect
from ..models import Order, Item, session
from .forms_admin import AddItemForm, OrderEditForm
from .utils import admin_only

admin = Blueprint("admin", __name__, url_prefix="/admin", static_folder="static", template_folder="templates")


@admin.route("/")
@admin_only
def dashboard():
    orders = session.query(Order).all()
    return render_template("admin.html", orders=orders)


@admin.route("/items")
@admin_only
def items():
    items = session.query(Item).all()
    return render_template("items.html", items=items)


@admin.route("/add", methods=["GET", "POST"])
@admin_only
def add():
    form = AddItemForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        category = form.category.data
        details = form.details.data
        form.data.save("static/uploads" + form.image.data.filename)
        image = url_for("static", filename=f"uploads/{form.image.data.filename}")
        price_id = form.price_id.data

        item = Item(
            name=name,
            price=price,
            category=category,
            details=details,
            image=image,
            price_id=price_id
        )

        try:
            session.add(item)
            session.commit()
            flash(f"{name} added successfully", "success")
            return redirect(url_for("admin.items"))
        except Exception as exc:
            raise exc
        finally:
            session.close()
    else:
        return render_template("add.html", form=form)


@admin.route("/edit/<string: type>/int:id>", methods=["GET", "POST"])
@admin_only
def edit(type, id):
    if type == "item":
        item = session.query(Item).get(id)
        form = AddItemForm(
            name=item.name,
            price=item.price,
            category=item.category,
            details=item.details,
            image=item.image,
            price_id=item.price_id
        )
        if form.validate_on_submit():
            item.name = form.name.data
            item.price = form.price.data
            item.category = form.category.data
            item.details = form.details.data
            item.price_id = form.price_id.data

            form.data.save("static/uploads/" + form.image.data.filename)
            item.image = url_for("static", filename=f"uploads/{form.image.data.filename}")
            session.commit()
            return redirect(url_for("admin.items"))
        elif type == "order":
            order = session.query(Order).get(id)
            form = OrderEditForm(
                status=order.status

            )
            if form.validate_on_submit():
                order.status = form.status.data
                session.commit()
                return redirect(url_for("admin.dashboard"))
        else:
            return render_template("add.html", form=form)


@admin.route("/delete/<int:id>")
@admin_only
def delete(id):
    item_to_delete = session.query(Item).get(id)
    session.delete(item_to_delete)
    session.commit()
    flash(f"{item_to_delete} deleted successfully", "error")
    return redirect(url_for("admin.items"))