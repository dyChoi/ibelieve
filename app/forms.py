from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    user_id = StringField('user_id', validators=[DataRequired()])
    user_nickname = StringField('user_nickname')
    remember_me = BooleanField('remember_me', default=False)
    child_user = BooleanField('role', default=False)
    parent_user = BooleanField('role', default=False)


class EnrollmentForm(Form):
    my_phone = StringField('my_phone', validators=[DataRequired()])
    partner1_phone = StringField('partner1_phone', validators=[DataRequired()])
    partner2_phone = StringField('partner2_phone')
