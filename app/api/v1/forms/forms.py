from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Length, InputRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=250)])
    remember = BooleanField('Remember me')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[
                        InputRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=250)])
