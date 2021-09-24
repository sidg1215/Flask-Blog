from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
    validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField("Email",
    validators=[DataRequired(), Email()])

    password = PasswordField('Password',
    validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',
    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('Email already exists')
        

class LoginForm(FlaskForm):
    email = StringField("Email",
    validators=[DataRequired(), Email()])

    password = PasswordField('Password',
    validators=[DataRequired()])

    submit = SubmitField("Log In")


class UpdateForm(FlaskForm):
    profilePicture = FileField('Update Profile Picture', 
    validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    username = StringField('Username', 
    validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField("Email",
    validators=[DataRequired(), Email()])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                print("cartier and gucci they dont go together")
                raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError('Email already exists')

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Type your thoughts away...", validators=[DataRequired()])
    submit = SubmitField("Post")

class EditPost(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Edit Post")