
from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms import validators, ValidationError

class LoginForm(Form):
	uname = TextField("Username", [validators.Required("Please enter a username")])
	upass = PasswordField("Password", [validators.Required("Please enter a password")])
	submit = SubmitField("Submit")