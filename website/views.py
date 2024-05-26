from flask import Blueprint , render_template , redirect , flash , request
from flask_login import login_required , current_user
from .models import Post , User
from . import db

views = Blueprint('views' , __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html" , posts=posts , user=current_user)

@views.route("/create-post" , methods=['GET' , 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        caption = request.form.get('caption')
        if len(text) < 2:
            flash("Too short" , category='error')
        else:
            new_post = Post(text=text , caption=caption ,author=current_user.id )
            db.session.add(new_post)
            db.session.commit()
    return render_template("create_post.html")

@views.route("/update/<post_id>" , methods=['GET' , 'POST'])
def update(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        caption = request.form.get('caption')
        text = request.form.get('text')
        post.caption = caption
        post.text = text
        db.session.commit()
        return redirect("/")
    return render_template("update_post.html",  caption=post.caption , text=post.text)

@views.route("/delete/<post_id>" , methods=['GET' , 'POST'])
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


#last thing to do
@views.route("/user/<name>")
def user_profile(name):
    user = User.query.filter_by(username=name).first()
    if user:
        return render_template("profile_page.html" , user=user)
    else:
        return render_template("404.html")