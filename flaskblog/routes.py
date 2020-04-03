import os
import os.path
import secrets
import sqlite3
import numpy as np
import pandas as pd
import json

from fpdf import FPDF

import sys

sys.path.append("/home/dell/Desktop/SIH_flask/flaskblog/static/custom_files/test")

#from test import make_plot
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post, Data1 ,Custom ,Data_hive,Post2
from flaskblog.forms import TextForm,RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CustomForm,PostFormhive
from flask_login import login_user, current_user, logout_user, login_required
#from flaskblog.simple import LineGraph, Histogram
#from bokeh.embed import components, file_html,json_item,server_document
from bokeh.plotting import figure
#from bokeh.models import ColumnDataSource, Div
#from bokeh.models.widgets import Tabs, Panel, Slider, Select, TextInput
#from bokeh.io import curdoc
#from bokeh.resources import CDN
#from bokeh.server.server import Server
from bokeh.themes import Theme
#from tornado.ioloop import IOLoop
from bokeh.layouts import column
import speech_recognition as sr
import nltk
import spacy
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
smtp_server = "smtp.gmail.com"

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
stop_words = set(stopwords.words('english')) 

nlp = spacy.load('D:/PythonWorkSpace/SIH-2020/flaskblog/DPEntities') 

keywordDict = {}

#MANALI
#speech recognition
@app.route("/echo", methods=['GET', 'POST'])
@login_required
def speak():
    text=''
    print("in speak....")
    r = sr.Recognizer()
    form = TextForm()
    with sr.Microphone() as source:
        print("SAY")

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=30)
            text = r.recognize_google(audio)
            print(text)
            form.test.data=text 
            
        except:
            pass;
    return render_template('echo.html', form = form)


def extract(words,skey, ekey = ""):
    if skey not in ["advice", "prescription"]: # if not advice then remove stop words else keep them
        wlist = remStopWords(words)
    else:
        wlist = words
    sindex = wlist.index(skey)+1
    if ekey != "":
        eindex = wlist.index(ekey)
        wlist = wlist[sindex:eindex]
        return listToString(wlist)
    else:
        return listToString(words[sindex:])
    
    
def getPrescription(mystring, lastKey, w):
    mystring = mystring.split(lastKey)[1]
    mystring  = mystring.split(w)[0]# contains string after word prescription
        
    nouns = getNouns(mystring)
    #extract sentence which has medicine name
    pDict = {}
    sentences =  sent_tokenize(mystring)
    for n in nouns:
        my_sentence=[sent for sent in sentences if n in word_tokenize(sent)]
        pDict[n] = my_sentence
        
    return pDict

def remStopWords(words):
    wlist = list()
    for w in words:
            if not w in stop_words:
                wlist.append(w)
    return wlist

def listToString(l):
    #listToStr = ' '.join([str(elem) for elem in li]) 
    listToStr = ""
    for elem in l:
        listToStr += " "+((elem))
    return listToStr

def getNouns(mystring):
    sentences = nltk.sent_tokenize(mystring) #tokenize sentences
    nouns = [] #empty to array to hold all nouns
    for sentence in sentences:
         for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
             if (pos == 'NNP'):
                 nouns.append(word)   
    return nouns

def setEntities(text,keywordDict,key):
    text = text.title()
    print('Updating for  -')
    print(key)
    doc = nlp(text)
    toUppend = ''
    print("Entities in '%s'" % text)
    for ent in doc.ents:
        print(ent.label_, ent.text)
        toUppend += ent.text
        toUppend +=  " "
        print(type(text))
        print()
        
    keywordDict[key] = toUppend
    print('New value')
    print(keywordDict[key])
    
@app.route("/test", methods=['GET', 'POST'])
@login_required
def test():
    form = TextForm(request.form)
    if request.method == 'POST':
        
        text=request.form['test']

    words = text.split()
    
    keywordList = ["name","age","gender","symptoms", "diagnosis", "prescription", "advice"]
    tobeTagged = ["name", "diagnosis"]
    keywordDict = {}
    
    lastKey = "name"
    for w in words:
        #    print(w)
        if keywordList.__contains__(w): 
            if(lastKey != "prescription"):
                keywordDict[lastKey] = extract(words, lastKey,w)
            else:# it is prescription
                keywordDict[lastKey] = extract(words, lastKey, w)
            lastKey = w
    if lastKey == "prescription":
        keywordDict[lastKey] = extract(words, lastKey)
    else:
        keywordDict[lastKey] = extract(words, lastKey)
    print(keywordDict)
    
    for key,value in keywordDict.items():

        text1 = keywordDict[key]
        
        print("Text is '%s'" % text1)
        if key in tobeTagged:        
            setEntities(text1,keywordDict,key)
        else:
            keywordDict[key] = text1

    print(keywordDict)
    
    convertToPDF(keywordDict)
    
    return render_template('pdfView.html',keywordDict=keywordDict)


# NICKY
# CONVERT TO PDF
    
class PDF(FPDF):
    def ___init__(self):
        super().__init__('P','mm','A4')	
        #content = cotent_dictionary
        
        
        
    def header(self):
        # Logo
        self.image('D:/PythonWorkSpace/SIH-2020/flaskblog/logo.png', 10, 10,w=30)
        
        # Arial bold 15
        self.set_font('Arial', 'I', 15)
        # Move to the right
        self.cell(80)
        # Title
        form = UpdateAccountForm()
        if form.validate_on_submit():
            
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.name=form.name.data
            current_user.qualification=form.qualification.data
            current_user.phone=form.phone.data
            current_user.hospital=form.hospital.data
            current_user.address=form.address.data
            current_user.license=form.license.data
            
            
       
        self.cell(0,10,'')
        self.cell(0, 6, current_user.name, 0, 1, 'R')
        self.cell(0, 6,current_user.qualification, 0, 1, 'R')
        self.cell(0, 6, current_user.phone, 0, 1, 'R')
        
        # Line break
        self.ln(30)
        self.line(10,50,200,50)
        

    # Page footer
    def footer(self):
        
        self.alias_nb_pages()
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        
    def add_content(self,content):
        self.add_page()
        self.set_font('Times', '', 12)
        for key,value in content.items():
            if key != 'symptoms' and key != 'diagnosis':
                 self.cell(50,5,key.capitalize()+' :',0,0)
#                 if key == 'prescription' :
#                      
#                      for k,v in value.items() :
#                          self.ln(10)
#                          self.cell(20)
#                          self.cell(50,5,k.capitalize()+' :',0,0)
#                          self.cell(0,5,v,0,0)
#                      
#                 else :        
                 self.cell(0,5,str(value),0,0)
                 self.ln(10)
        self.image('D:/PythonWorkSpace/SIH-2020/flaskblog/signature.png',170,250,w=30)
        filename = content['name'].replace(" ","")
        self.output(filename+'.pdf', 'F')
        

def convertToPDF(keywordDict):
       pdf = PDF()
       pdf.add_content(keywordDict) 

# SEJAL
# MAILIND TO PATIENT    
@app.route("/send", methods=['GET', 'POST'])
@login_required
def sendToPatient():
        port= 587
        sender = "mailattachtest@gmail.com"
        password="mailattachtest@1"
        receiver = "mailattachtest@gmail.com"
        msg=MIMEMultipart()
        file = "D:/PythonWorkSpace/SIH-2020/Manali.pdf"
#        file = "C:/Users/Lenovo/Desktop/CSPPT.pdf"
        with open(file,"rb") as attachment:
            part=MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
       
        part.add_header("Content-Disposition",f"attachment;filename={file}")
        msg.attach(part)
        text=msg.as_string()
        context=ssl.create_default_context()
        with smtplib.SMTP(smtp_server,port) as server:
            server.starttls(context=context)
            server.login(sender,password)
            server.sendmail(sender,receiver,text)
        flash('Your account has been created! You are now able to log in', 'success')
        return render_template('land.html')
    
    
@app.route("/", methods=['GET', 'POST'])
@login_required
def land():
    

    return render_template('land.html')

def save_file1(form_file):
    #random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_file.filename)
    file_fn = f_name + f_ext
    file_path = os.path.join(app.root_path, 'static/custom_files', file_fn)
    form_file.save(file_path)
    print(file_fn)
    print(file_path)
    return file_fn


@app.route("/admin")
@login_required
def admin():
    custom = Custom.query.all()
    return render_template('custom_exist.html', title='Custom',custom=custom)

'''
@app.route("/admin/custom", methods=['GET', 'POST'])
@login_required
def custom_exist():
    custom = Custom.query.all()

    
    return render_template('custom_exist.html', title='Custom',custom=custom)
'''


@app.route("/admin/custom/new", methods=['GET', 'POST'])
@login_required
def custom():
    form = CustomForm()
    if form.validate_on_submit():

        
        
        
        if form.file.data:
            file2 = save_file1(form.file.data)
       
        custom = Custom(title=form.title.data, content=form.content.data, no_param=form.no_param.data, name_param=form.name_param.data, file=file2 )                 
        db.session.add(custom)
        db.session.commit()
        flash('Your custom visualization code has been saved!', 'success')
        return redirect(url_for('land'))
        file_name = url_for('static', filename='custom_files/')
    

    return render_template('custom.html', title='New Custom',form=form, legend='New Custom visualization')



@app.route("/admin/user", methods=['GET', 'POST'])
@login_required
def user():
    users = User.query.all()

    return render_template('user.html', title='User',users=users)




@app.route("/admin/user/register", methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
    #    return redirect(url_for('land'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, qualification=form.qualification.data,phone=form.phone.data,hospital=form.hospital.data,address=form.address.data,signature=form.signature.data,license=form.license.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('land'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('land'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #return redirect(next_page) if next_page else redirect(url_for('land'))
            return redirect(url_for('land'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('land'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #form_picture.save(picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/files', file_fn)
    form_file.save(file_path)
    print(file_fn)
    print(file_path)
    return file_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name=form.name.data
        current_user.qualification=form.qualification.data
        current_user.phone=form.phone.data
        current_user.hospital=form.hospital.data
        current_user.address=form.address.data
        current_user.license=form.license.data
        
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.qualification.data = current_user.qualification
        form.phone.data = current_user.phone
        form.hospital.data = current_user.hospital
        form.address.data = current_user.address
        form.license.data = current_user.license
    
    return render_template('account.html', title='Account', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():

        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        
        
        if form.file.data:
            file2 = save_file(form.file.data)
       
        #data = Data(tablename=form.tablename.data, tabletype=form.tabletype.data, author=current_user,file=file2)
        
        #post= Post(or)
        #db.session.add(post)
        db.session.add(post)
        db.session.commit()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "123.db")
        with sqlite3.connect(db_path) as db1:
            cursor = db1.cursor()
            cursor1 = db1.cursor()
            z=cursor.execute("SELECT id FROM Post WHERE title=? ",(form.title.data,))
            abc=(list(z)[0])[0]
            count=0

            if(abc>1):
                cursor1.execute("SELECT id FROM Data1 WHERE tablename=? ",(form.tablename.data,))
                for row in cursor1:
                    x=row
                    count=count+1
                if count!=0:
                    abc1=x[0]
                    print(abc1)
                else:
                    abc1=abc
            else:
                abc1=abc
                         
                '''if z1.fetchall():
                    abc1=z1.fetchall()

                    print(z1)
                    print(list(z1))
                    print(abc1)'''

                
                
                    #print(abc)    
                    #abc1=(list(z1)[0])[0]



            
        '''conn = sqlite3.connect('123.db')
        cur = conn.cursor()
        z=cur.execute("SELECT id FROM Post WHERE title=? ",(form.title.data,))'''
        data = Data1(id=abc1,tablename=form.tablename.data, tabletype=form.tabletype.data,file=file2,post_id=abc)
        db.session.add(data)
        db.session.commit()
        flash('Your project has been created!', 'success')
        return redirect(url_for('land'))
        file_name = url_for('static', filename='files/')
    return render_template('create_post.html', title='New Project',
                           form=form, legend='New Project')

    
    
'''@app.route("/post/new/data", methods=['GET', 'POST'])
@login_required
def new_data():

    form = DataForm() 
    
    #print (form.file.data)
    if form.validate_on_submit():
        
        if form.file.data:
            file2 = save_file(form.file.data)
       
        #data = Data(tablename=form.tablename.data, tabletype=form.tabletype.data, author=current_user,file=file2)
        data = Data(tablename=form.tablename.data, tabletype=form.tabletype.data,file=file2)
        #post= Post(or)
        #db.session.add(post)
        db.session.add(data)
        db.session.commit()
        flash('Your data has been created!', 'success')
        return redirect(url_for('land'))
    

    file_name = url_for('static', filename='files/')
    return render_template('data.html', title='New Data',file_name=file_name,
                          form=form, legend='New Data')'''

               


@app.route("/post/new_hive", methods=['GET', 'POST'])
@login_required
def new_hive():
    form=PostFormhive()
    if form.validate_on_submit():
        
        
        
        post = Post2(title=form.title.data, content=form.content.data, author=current_user)
        
        db.session.add(post)
        db.session.commit()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "123.db")
        with sqlite3.connect(db_path) as db1:
            cursor = db1.cursor()
            cursor1 = db1.cursor()
            #x=cursor.execute("SELECT id FROM Post2 WHERE id=? ",(form.title.id,))

            z=cursor.execute("SELECT id FROM Post2 WHERE title=? ",(form.title.data,))
            abc=(list(z)[0])[0]
            print(abc)
            count=0

            if(abc>1):
                cursor1.execute("SELECT id FROM Data_hive WHERE tablename1=? ",(form.tablename1.data,))
                for row in cursor1:
                    x=row
                    count=count+1
                if count!=0:
                    abc1=x[0]
                    print(abc1)
                else:
                    abc1=abc
            else:
                abc1=abc
            
            
        hive = Data_hive(id=abc1,tablename1=form.tablename1.data, tabletype1=form.tabletype1.data,databasename=form.databasename.data,post2_id=abc)
        db.session.add(hive)
        db.session.commit()
        return redirect(url_for('land'))
    return render_template("create_post_hive.html",form=form,legend='New Hive Project',title='New Hive Project')
    


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# Trial code for visualise

@app.route("/post/<int:post_id>/visualise",methods=['GET', 'POST'])
@login_required
def visualise(post_id):
    if post_id<1000:
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "123.db")
        with sqlite3.connect(db_path) as db1:
            cursor = db1.cursor()
            z=cursor.execute("SELECT file FROM Data1 WHERE post_id=? ",(post_id,))
            print(z)
            abc=(list(z)[0])[0]
            print(abc)
            print(type(abc))
            cursor1 = db1.cursor()
            z1=cursor1.execute("SELECT tablename FROM Data1 WHERE post_id=? ",(post_id,))
            print(z1)
            abc1=(list(z1)[0])[0]
            print(abc1)
            print(type(abc1))
            




        name = abc1      
        #headers = list(pd.read_csv(r"C:\Users\Aditya\citi_flask\flaskblog\static\files\{}".format(abc)).head(0))
        #headers1 = pd.read_csv(r"C:\Users\Aditya\citi_flask\flaskblog\static\files\{}".format(abc)).head()
        headers = list(pd.read_csv(r"/home/dell/citi_flask/flaskblog/static/files/{}".format(abc)).head(0))
        headers1 = pd.read_csv(r"/home/dell/citi_flask/flaskblog/static/files/{}".format(abc)).head()    
        jkl=list(headers1.dtypes)
        for n, i in enumerate(jkl):
            if i == "float64":
                jkl[n] = "num"
            else:
                jkl[n]="str"

        print(jkl)
        dictionary = zip(headers, jkl)
        dictionary = set(dictionary)

        print("-------oooooooooooooo-------------")
        print(dictionary)
        print("-------oooooooooooooo-------------")
        plot_num=0
        custom = Custom.query.all()
        return render_template('visualise.html',dictionary=dictionary,name=name,post_id=post_id,custom=custom,plot_num=plot_num)

    else:
        post = Post2.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)

        
        return render_template('visualise.html',post_id=post_id)


    



@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    if post_id<1000:
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "123.db")
        with sqlite3.connect(db_path) as db1:
            cursor = db1.cursor()
            z=cursor.execute("SELECT id FROM Data1 WHERE post_id=? ",(post_id,))
            print(z)
            abc=(list(z)[0])[0]
            print(abc)
            print(type(abc))
        post = Post.query.get_or_404(post_id)
        data1 = Data1.query.get_or_404((abc,post_id))
        if post.author != current_user:
            abort(403)

        db.session.delete(post)
        db.session.delete(data1)
        db.session.commit()
        flash('Your project has been deleted!', 'success')
        return redirect(url_for('land'))
    else:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "123.db")
        with sqlite3.connect(db_path) as db1:
            cursor = db1.cursor()
            z=cursor.execute("SELECT id FROM Data_hive WHERE post2_id=? ",(post_id,))
            print(z)
            abc=(list(z)[0])[0]
            print(abc)
            print(type(abc))
        post = Post2.query.get_or_404(post_id)
        data1 = Data_hive.query.get_or_404((abc,post_id))
        if post.author != current_user:
            abort(403)

        db.session.delete(post)
        db.session.delete(data1)
        db.session.commit()
        flash('Your project has been deleted!', 'success')
        return redirect(url_for('land'))


# ------------- testing histogram.html------------------------------





@app.route("/post/<int:post_id>/visualise/histogram",methods=['GET', 'POST'])
#@login_required
def histogram(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "123.db")
    with sqlite3.connect(db_path) as db1:
        cursor = db1.cursor()
        z=cursor.execute("SELECT file FROM Data1 WHERE post_id=? ",(post_id,))
        print(z)
        abc=(list(z)[0])[0]
        print(abc)
        print(type(abc))
        cursor1 = db1.cursor()
        z1=cursor1.execute("SELECT tablename FROM Data1 WHERE post_id=? ",(post_id,))
        print(z1)
        abc1=(list(z1)[0])[0]
        print(abc1)
        print(type(abc1))

        print("-------------------------------------------")
        




    name = str(abc1) 

    data_df = pd.read_csv(r"/home/dell/Desktop/SIH_flask/flaskblog/static/files/{}".format(abc))


    headers = list(pd.read_csv(r"/home/dell/Desktop/SIH_flask/flaskblog/static/files/{}".format(abc)).head(0))
    headers1 = pd.read_csv(r"/home/dell/Desktop/SIH_flask/flaskblog/static/files/{}".format(abc)).head()
    
    

    jkl=list(headers1.dtypes)
    for n, i in enumerate(jkl):
        if i == "float64":
            jkl[n] = "num"
        else:
            jkl[n]="str"

    #print(jkl)
    dictionary = zip(headers, jkl)
    '''     
    source=ColumnDataSource(data_df)


    
    #x1=range(len(data_df.iloc[0:,1:2]))
    plots=[]
    tab=[]

    for i in range(len(headers)-1):

        plot = figure(plot_height=500, plot_width=500)
        
        plot.line(x=headers[0],y=headers[i], source=source,line_width=2)
        tab.append( Panel(child = plot,title = headers[i]))

        #script, div = components(plot)
        #plots.append((script,div))
    #print(x)
    #print(y)

    tabs = Tabs(tabs=tab)
    t=make_plot(data_df)
    
    script, div = components(tabs)
    print("...............................................")
    print(div)
    print("...............................................")
    print(t)
    print("...............................................")
    plots.append((script,div))
    '''
    
    plots=[]
    plots=Histogram(data_df)
    

    
    plot_num=1
    custom = Custom.query.all()
    #return json.dumps(json_item(plot, "myplot"))
    
    return render_template('histogram.html',dictionary=dictionary,name=name,plots=plots,post_id=post_id,custom=custom,plot_num=plot_num)
'''
    item_text= json.dumps(json_item(plot,"myplot"))
    #item=JSON.parse(item_text)
    return item_text
'''

def modify_doc(doc):
    

    source = ColumnDataSource(data=df)

    plot = figure(y_range=(0, 10),
                  y_axis_label='iris dataset',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('x', 'y', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data
        
    def callback1(attr, old, new):
        if new == 0:
            data = df
        else:
            data=df
            data['y'] = data[y_axis.value]
        source.data = ColumnDataSource(data=data).data
    
    def callback2(attr, old, new):
        if new == 0:
            data = df
        else:
            data=df
            data['x'] = data[x_axis.value]
        source.data = ColumnDataSource(data=data).data

    
    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)
    
    x_axis = Select(title="X Axis", options=list((df.iloc[:,0:-2]).columns), value=df.columns[0])
    x_axis.on_change('value', callback2)
    
    
    y_axis = Select(title="Y Axis", options=list((df.iloc[:,0:-2]).columns), value=df.columns[1])
    y_axis.on_change('value', callback1)
    
    doc.add_root(column(slider,x_axis,y_axis, plot))

    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """))
    
