from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired(), Length(max=50)])
    phone = StringField("Phone No: ", validators=[DataRequired(), Length(max=30)])
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: " , validators=[DataRequired()])
    confirm = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo(
        "password",
        message="Password must match"
    )])
    submit = SubmitField("Register")
