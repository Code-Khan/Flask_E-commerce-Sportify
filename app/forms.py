from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, EqualTo, Email





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


class PostForm(FlaskForm):
    name = StringField('name')
    last_name = StringField('last_name')
    phone = StringField('phone', validators=[DataRequired()])
    submit = SubmitField()






# --------------------------------------------------------------------------------------------------------

class DeletePostForm(FlaskForm):
    submit = SubmitField()


class Add(FlaskForm):
    Add_to_Cart = SubmitField()    