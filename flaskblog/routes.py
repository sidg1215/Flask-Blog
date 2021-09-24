from flask import  render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateForm, PostForm, EditPost
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db
from flask_login import login_user, logout_user, login_required, current_user

import secrets
import os
from PIL import Image

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html", posts = Post.query.all(), title = "Home")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():

        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username = form.username.data, password = hashedPassword, email = form.email.data)
        db.session.add(user)
        db.session.commit()

        flash('Account created!', 'success')


        return redirect(url_for("login"))
    return render_template("register.html", form = form, title = "Register")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember = True)
            flash("Logged in as " + user.username, "success")
            nextPage = request.args.get('next')
            if (nextPage):
                return redirect(nextPage)            
            return redirect(url_for("index"))
        flash("Login Unsuccessful.", "danger")
    return render_template("login.html", form = form, title = "login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/account")
@login_required
def account():
    imageFile = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    print(imageFile)
    print(current_user.posts)
    return render_template("account.html", imageFile = imageFile, user = current_user)


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.profilePicture.data:
            randomHex = secrets.token_hex(8)
            _, fileExtension = os.path.splitext(form.profilePicture.data.filename)
            pictureFileName = str(randomHex) + fileExtension
            picturePath = os.path.join(app.root_path, 'static/profile_pics', pictureFileName)

            resizedImage = Image.open(form.profilePicture.data)
            resizedImage.thumbnail((125,125))

            resizedImage.save(picturePath)

            current_user.image_file = pictureFileName
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash("Account Information changed", "info")
        return redirect(url_for("index"))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.profilePicture.data = current_user.image_file
    return render_template("updateAccount.html", form = form)

@app.route("/post/new" ,methods = ["GET", "POST"])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        flash("Your post has been created", "success")
        post = Post(title = form.title.data, content = form.content.data, userId = current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("makePost.html", form = form)

@app.route("/post/<postId>")
def viewPost(postId):
    post = Post.query.get(postId)
    if post:
        return render_template("post.html", post = post)
    return "<h1>Post does not exist</h1>"

@app.route("/post/<postId>/edit", methods = ["GET", "POST"])
@login_required
def editPost(postId):
    post = Post.query.get(postId)
    if current_user != post.author:
        return "<h1>You do not have permission to edit this post</h1>"
    if post:
        form = EditPost()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Post has been edited", "info")
            return redirect(url_for("viewPost", postId = post.id))
        form.title.data = post.title
        form.content.data = post.content
        return render_template("makePost.html", form = form)
    return "<h1>Post does not exist</h1>"

@app.route("/post/<postId>/delete")
@login_required
def deletePost(postId):
    post = Post.query.get(postId)
    if current_user != post.author:
        return "<h1>You do not have permission to delete this post</h1>"
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("The post has been successfully deleted.")
        return redirect(url_for("index"))
    return "<h1>Post does not exist</h1>"

@app.route("/<username>")
def userPage(username):
    user = User.query.filter_by(username = username).first()

    print(user == current_user)
    if user  == current_user:
        return redirect("account")
    if user:
        imageFile = url_for('static', filename = 'profile_pics/' + user.image_file)
        print(imageFile)
        return render_template("account.html", filename = imageFile, user = user)
    return "<h1>User does not exist</h1>"
