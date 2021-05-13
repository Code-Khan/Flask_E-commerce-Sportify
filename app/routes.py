from app import app, db, mail
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
from app.forms import UserInfoForm, LoginForm, UserInfoPhone
from app.models import User, UserPhone, Post
# from app.forms import PostForm


@app.route('/')
def index():
    context = {
        'title': 'HOME',
        'posts': Post.query.all()


    }
    return render_template('index.html', **context)


@app.route('/phone_register', methods=['GET', 'POST'])
@login_required
def registerphone():
    title = 'POHONE_REGISTER'
    form = UserInfoPhone()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        phone = form.phone.data
        user_id = current_user.id
        # print(username, email, password)
        # Check if username/email already exists
        existing_user = UserPhone.query.filter((UserPhone.name == name) | (
            UserPhone.last_name == last_name) | (UserPhone.phone == phone)).all()
        if existing_user:
            flash(
                'That name , last name or phone already exists. Please try again', 'danger')
            return redirect(url_for('phone_register'))

        new_user = UserPhone(name, last_name, phone)
        db.session.add(new_user)
        db.session.commit()

        flash(
            f'Thank you {name} {last_name} your contact has been saved!', 'success')
        return redirect(url_for('index'))

    return render_template('phone_register.html', title=title, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'REGISTER'
    form = UserInfoForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print(username, email, password)
        # Check if username/email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).all()
        if existing_user:
            flash('That username or email already exists. Please try again', 'danger')
            return redirect(url_for('register'))

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {username} for registering!', 'success')

        msg = Message(f'Thank you, {username}', recipients=[email])
        msg.body = f'Dear {username}, thank you so much for signing up for this super cool app. I hope you enjoy and also you look super good today!'
        mail.send(msg)

        return redirect(url_for('index'))

    return render_template('register.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'LOGIN'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect Username/Password. Please try again.', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        flash('You have succesfully logged in!', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out!', 'primary')
    return redirect(url_for('index'))


# @app.route('/createpost', methods=['GET', 'POST'])
# @login_required
# def createpost():
#     title = 'CREATE POST'
#     form = PostForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         post_title = form.title.data
#         post_body = form.body.data
#         user_id = current_user.id

#         new_post = Post(post_title, post_body, user_id)

#         db.session.add(new_post)
#         db.session.commit()

#         flash(f"You have created a post: {post_title}", 'info')

#         return redirect(url_for('index'))

#     return render_template('createpost.html', title=title, form=form)
