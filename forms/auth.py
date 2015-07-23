from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from .base import BaseForm


class LoginForm(BaseForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[Length(min=6, max=20)])


class RegisterForm(BaseForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    username = StringField('昵称', validators=[DataRequired()])
    password = PasswordField('密码', validators=[Length(min=6, max=20)])
