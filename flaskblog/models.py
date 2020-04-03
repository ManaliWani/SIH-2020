from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    qualification = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    hospital= db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(20), unique=True, nullable=False)
    signature = db.Column(db.String(20), nullable=False, default='default.png')
    license = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    

    def __repr__(self):
        #return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        return "User({username}, {email},{name},{qualification},{phone},{hospital},{address}, {signature},{license})".format(username=self.username,email=self.email,name=self.name,qualification=self.qualification,phone=self.phone,hospital=self.hospital,address=self.address,signature=self.signature,license=self.license)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #file = db.Column(db.String(100), nullable=False, default='default.csv')
    
    data = db.relationship('Data1', backref='author', lazy=True)



    def __repr__(self):
        return "Post({title}, {date_posted})".format(title=self.title,date_posted=self.date_posted)
        #return f"Post('{self.title}', '{self.date_posted}')"

class Post2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #file = db.Column(db.String(100), nullable=False, default='default.csv')
   
    data = db.relationship('Data_hive', backref='author', lazy=True)



    def __repr__(self):
        id=1000
        return "Post2({title}, {date_posted})".format(title=self.title,date_posted=self.date_posted)
        #return f"Post('{self.title}', '{self.date_posted}')"

class Data1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tablename = db.Column(db.String(100), nullable=False)
    tabletype=db.Column(db.String(100), nullable=False)
    
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file= db.Column(db.String(20), nullable=False, default='default.csv')
    
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False,primary_key=True)


    def __repr__(self):
        #return f"Data1('id:{self.id}','{self.tablename}','{self.tabletype}','{self.file}','{self.post_id}')"

        return "Data1({id}, {tablename}, {tabletype},{file},{post_id})".format(id=self.id,tablename=self.tablename, tabletype=self.tabletype,file=self.file,post_id=self.post_id)

class Data_hive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tablename1 = db.Column(db.String(100), nullable=False)
    tabletype1=db.Column(db.String(100), nullable=False)
    databasename=db.Column(db.String(100),nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #file= db.Column(db.String(20), nullable=False, default='default.csv')
    
    post2_id=db.Column(db.Integer, db.ForeignKey('post2.id'), nullable=False,primary_key=True)


    def __repr__(self):
        #return f"Data1('id:{self.id}','{self.tablename}','{self.tabletype}','{self.file}','{self.post_id}')"

        return "Data_hive({id}, {tablename1}, {tabletype1},{databasename},{post2_id})".format(id=self.id,tablename1=self.tablename1, tabletype1=self.tabletype1,databasename=databasename,post2_id=self.post2_id)


class Custom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    no_param = db.Column(db.Integer, nullable=False)
    #file = db.Column(db.String(100), nullable=False, default='default.csv')
    name_param = db.Column(db.String(120), nullable=False)
    file= db.Column(db.String(20), nullable=False, default='default.py')
    #data = db.relationship('Data1', backref='author', lazy=True)

    def __repr__(self):
        return "Custom({id}, {title}, {content}, {no_param}, {name_param}, {file})".format(id=self.id,title=self.title,content=self.content,no_param=self.no_param,name_param=self.name_param,file=self.file)
    

