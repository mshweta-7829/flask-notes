from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional, Email


class UserRegisterForm(FlaskForm):
    """Form for registering users."""

    username = StringField("User Name: ", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField("First Name: ", validators=[InputRequired()])
    last_name = StringField("Last Name: ", validators=[InputRequired()])

class UserLoginForm(FlaskForm):
    """Form for registering users."""

    username = StringField("User Name: ", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])