from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField 
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Alex' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security_updates.sqlite3'

db = SQLAlchemy(app)
class Security_Updates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow()) 

    def __init__(self, name):
        self.name = name 

class Accounts(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50)) 
    password = db.Column(db.String(50))
    email = db.Column(db.String(50)) 

    def __init__(self, username, password, email):
        self.username = username 
        self.password = password
        self.email = email
        

class NameForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('username') 
    password = PasswordField('password')
    submit = SubmitField('Submit')

class AccountCreation(FlaskForm):
    username = StringField('username')
    password = PasswordField('password') 
    email =  StringField('email')
    submit = SubmitField('submit') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.username.data = ''
        form.password.data = ''
        return redirect(url_for('home'))
    
    return render_template('login.html', form=form, username=username, password=password)

@app.route('/login/accountcreation', methods=['GET', 'POST'])
def account_creation():
    username = None
    email = None
    password = None
    form = AccountCreation() 
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data 
        new_log = AccountCreation(username, password, email)
        db.session.add(new_log) 
        db.session.commit() 
        form.username.data = ''
        form.password.data = ''
        form.email.data = ''

    return render_template('account_creation.html', username=username, password=password, email=email, form=form)
    

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/PostForm', methods=['GET', 'POST'])
def form():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data 
        new_log = Security_Updates(name)
        db.session.add(new_log)
        db.session.commit()
        form.name.data = ''
               
    return render_template('Webform.html', form=form, name=name)

@app.route('/PostLog')
def log():
    entrys = Security_Updates.query.order_by(Security_Updates.id.desc())
    return render_template('postlog.html', entrys=entrys) 

@app.route('/delete/<int:id>')
def delete(id):
    record_to_delete = Security_Updates.query.get_or_404(id)
    try:
        db.session.delete(record_to_delete) 
        db.session.commit() 
        return redirect('/PostLog')
    except:
        return "Error"


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)