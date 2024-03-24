from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,RadioField,DateField, SelectField
from wtforms.validators import Email,DataRequired,EqualTo,Length
from flask_wtf.file import FileAllowed



class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message="The Username is a must")])
    usermail = StringField('Email', validators=[DataRequired(), Email(message="Invalid Email format")])
    userphone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    pwd = PasswordField("Enter Password", validators=[DataRequired(message="Enter Password")])
    confirm_pwd = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('pwd',message="Please, Let the two passwords match")])
    btnsubmit = SubmitField("Register!")


class userlogin(FlaskForm):
    username = StringField(validators=[DataRequired(message="The Username is a must")])
    password = PasswordField(validators=[DataRequired(message="Enter Password")])
    btnsubmit = SubmitField("Register!")