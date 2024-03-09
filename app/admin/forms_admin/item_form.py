from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, FloatField, FileField


class AddItemForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired(), Length(max=50)])
    price = FloatField("Price:", validators=[DataRequired()])
    category = StringField("Category: ", validators=[DataRequired(), Length(max=50)])
    image = FileField("Image: ", validators=[DataRequired()])
    details = StringField("Details: ", validators=[DataRequired()])
    price_id = StringField("Price_id: ", validators=[DataRequired()])
    submit = SubmitField("Add")


