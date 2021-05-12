from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, EqualTo, Email

class UserInfoForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    phone = IntegerField('phone', validators=[DataRequired()])
    submit = SubmitField()
