from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField


class OrderEditForm(FlaskForm):
    status = StringField("Status:", validators=[DataRequired()])
    submit = SubmitField("Update")


