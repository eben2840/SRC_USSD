
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp,Length


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    comment =  StringField('comment', validators=[DataRequired()])
    submit = SubmitField('submit')  
 
 
class Account(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password =  PasswordField('comment', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('submit')  
 
class First(FlaskForm):
    name =  StringField('name', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('submit')
 


class SRCC(FlaskForm):
    srcname =  StringField('srcname', validators=[DataRequired()])
    srcnumb =  StringField('srcnumb', validators=[DataRequired(), Length(min=10, max=15, message="Your phone number should be more than 10 digits and less than 15")])
    Hoodie =  StringField('hoodie', validators=[DataRequired()])
    sweat =  StringField('sweat', validators=[DataRequired()])
    shirt = StringField('shirt', validators=[DataRequired()])
    bag =  StringField('bag', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('submit')  
 
 
class Add(FlaskForm):
    phone =  StringField('phone', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('submit')  
   # budget =SelectField('budget', validate_choice=[('Gh<span>&#8373;</span>:10,Gh<span>&#8373;</span>:100')('Gh<span>&#8373;</span>:100,,Gh<span>&#8373;</span>:500,')])
    
    
class Reviewcomment(FlaskForm):
    reviewname = StringField('reviewname', validators=[DataRequired()])
    review =  StringField('review', validators=[DataRequired()])
    submit = SubmitField('submit')  
 