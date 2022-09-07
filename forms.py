from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Length(min=1, max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=50)])
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class NewFeedbackForm(FlaskForm):
    title = StringField("Feedback Title", validators=[InputRequired(), Length(min=1, max=100)])
    content = TextAreaField("Feedback", validators=[InputRequired()])

class EditFeedbackForm(FlaskForm):
    title = StringField("Feedback Title", validators=[InputRequired(), Length(min=1, max=100)], default="title")
    content = TextAreaField("Feedback", validators=[InputRequired()], default="content")