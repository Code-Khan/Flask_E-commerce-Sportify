from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, EqualTo, Email


class UserInfoPhone(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    submit = SubmitField()


class UserInfoForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[
                                 DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField()


# class PostForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     body = StringField('Body', validators=[DataRequired()])
#     submit = SubmitField()
