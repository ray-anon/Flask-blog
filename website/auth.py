from flask import Blueprint , render_template , flash , redirect , request , session
from .models import User
from . import db
from flask_login import login_required , login_user , logout_user , current_user

auth = Blueprint('auth' , __name__)

@auth.route("/sign-up" , methods=['GET' , 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_name = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user_email:
            flash("The email already exists" , category='error')
        elif user_name:
            flash("The username already exists" , category='error')
        elif len(username) < 2:
            flash("Username is too short" , category='error')
        elif len(email) < 10:
            flash("Email is too short" , category='error')
        elif len(password1) < 6:
            flash("Password is too weak" , category='error')
        elif password1 != password2:
            flash('The passwords do not match' , category='error')
        else:
            new_user = User(username=username , email=email , password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user , remember=True)
            flash("New user created" , category='success')
            session['logged_in'] = True
            #redirect("/")
    return render_template("signup.html")

@auth.route("/login" , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        log_user = User.query.filter_by(email=email).first()
        if log_user:
            if password == log_user.password:
                flash("User Logged in Successfully" , category='success')
                login_user(log_user , remember=True)
                session['logged_in'] = True
                return redirect('/')
            else:
                flash('Password is Incorrect' , category='error')
        else:
            flash('Email is incorrect' , category='error')
    return render_template("login.html")


#take care of this
@auth.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect("/home")
