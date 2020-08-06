from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, TextField, \
    SelectField
from wtforms.validators import Required, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password:', validators=[Required(), \
        EqualTo('confirm', message='Password must match!')])
    confirm = PasswordField('Password:', validators=[Required()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[Required()])
    password = PasswordField('Password:', validators=[Required()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    content = TextField('Description:', validators=[Required()])
    status = SelectField('Status', choices=[('1','Todo'), ('2','Doing'), ('3', 'Done')],
        default='1')
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')