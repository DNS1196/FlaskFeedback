from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(),  Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete form"""
    
class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField("Title",validators=[InputRequired(), Length(max=100)])
    content = StringField("Content",validators=[InputRequired()])