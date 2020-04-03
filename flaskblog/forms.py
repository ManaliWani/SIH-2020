from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField,TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User,Post





def returnlist():
    list1=[]
    list=['a','b','c','d']
    for x in list:
        list1.append(x)
    print(list1)
    list_final=zip(list1,list)
    return list_final

test=returnlist()
print(test)
name="ABC"

class TextForm(FlaskForm):
    test = TextAreaField('Text')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])   
    qualification = StringField('Qualification',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone',
                           validators=[DataRequired()]) 
    hospital = StringField('Hospital',
                           validators=[DataRequired(), Length(min=2, max=20)])  
    address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])    
    signature = FileField('Signature', validators=[FileAllowed(['png'])]) 
    license = StringField('License',
                           validators=[DataRequired()])         
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    #To do : add phone validation
    
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])   
    qualification = StringField('Qualification',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone',
                           validators=[DataRequired()]) 
    hospital = StringField('Hospital',
                           validators=[DataRequired(), Length(min=2, max=20)])  
    address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])    
    license = StringField('License',
                           validators=[DataRequired()])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    #file = FileField('Update File', validators=[FileAllowed(['csv', 'xlsx'])])
    
    tablename = StringField('Table Name', validators=[DataRequired()])
    #tabletype = StringField('Data Type', validators=[DataRequired()])
    tabletype = SelectField('Data Type', choices = ([('csv','csv'),('parquet','parquet')]))
    #file = FileField(' File', validators=[FileAllowed(['csv', 'xlsx'])])
    file = FileField('Upload File',validators=[FileRequired()])
    submit = SubmitField('Save')
    def validate_title(self, title):
        user1 = Post.query.filter_by(title=title.data).first()
        if user1:
            raise ValidationError('That title is taken. Please choose a different one.')


class PostFormhive(FlaskForm):
    title = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    #file = FileField('Update File', validators=[FileAllowed(['csv', 'xlsx'])])
    
    tablename1 = SelectField('Table ', choices = test)
    tabletype1 = SelectField('Type ', choices = ([('hive','hive')]))
    #tabletype = SelectField('Data Type', choices = ([('hive','hive')]))
    databasename=TextField('Database',default=name)
    #file = FileField(' File', validators=[FileAllowed(['csv', 'xlsx'])])
    #file = FileField('Upload File',validators=[FileRequired()])
    submit = SubmitField('Save')
    def validate_title(self, title):
        user1 = Post.query.filter_by(title=title.data).first()
        if user1:
            raise ValidationError('That title is taken. Please choose a different one.')
'''class DataForm(FlaskForm):
    tablename = StringField('Table Name', validators=[DataRequired()])
    tabletype = StringField('Table Type', validators=[DataRequired()])
    #file = FileField(' File', validators=[FileAllowed(['csv', 'xlsx'])])
    file = FileField('Update File',validators=[FileRequired()])
    submit = SubmitField('Add')'''

class CustomForm(FlaskForm):
    title = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    #file = FileField('Update File', validators=[FileAllowed(['csv', 'xlsx'])])
    no_param = IntegerField('Number of Parameters', validators=[DataRequired()])
    name_param = StringField('Name of Parameters (comma separated)', validators=[DataRequired()])
    #tabletype = StringField('Data Type', validators=[DataRequired()])
    
    #file = FileField(' File', validators=[FileAllowed(['csv', 'xlsx'])])
    file = FileField('Upload Python File',validators=[FileRequired()])
    submit = SubmitField('Save')
    def validate_title1(self, title):
        custom1 = Custom.query.filter_by(title=title.data).first()
        if custom1:
            raise ValidationError('That title is taken. Please choose a different one.') 
    
                            