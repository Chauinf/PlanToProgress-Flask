from flask.ext.wtf import Form
from wtforms import StringField, PasswordField,  BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User


class RegisterForm(Form):
	email = StringField('Email', validators = [Required(), Length(1,64),Email()])
	nickname = StringField('Nickname', validators = [Required(),Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0, 'Nickname must have only letters, numbers, dots or underscores')])
	password = PasswordField('Password', validators = [Required(), EqualTo('password2', message = 'Password must match.')])
	password2 = PasswordField('Confirm Password', validators = [Required()])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already register.')
	
	def validate_username(self, field):
                if User.query.filter_by(nickname=field.data).first():
                        raise ValidationError('Nickname already in use.')

class LoginForm(Form):
	email = StringField('Email', validators = [Required(), Length(1,64),Email()])
	password = PasswordField('Password', validators = [Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')