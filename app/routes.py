from app import app, db, mail
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
from app.forms import UserInfoForm, LoginForm,DeletePostForm
from app.models import User, Post
from app.forms import PostForm


@app.route('/')
def index():
    context = {
        'title': 'HOME',
        'posts': Post.query.all()


    }
    return render_template('index.html', **context)



@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'REGISTER'
    form = UserInfoForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
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


@app.route('/phone_register', methods=['GET', 'POST'])
@login_required
def createpost():
    title = 'CREATE POST'
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post_name = form.name.data
        post_last_name = form.last_name.data
        post_phone = form.phone.data
        user_id = current_user.id

        new_post = Post(post_name, post_last_name, post_phone, user_id)

        db.session.add(new_post)
        db.session.commit()

        flash(f"You have entered a phone number for: {post_name}", 'info')

        return redirect(url_for('index'))

    return render_template('phone_register.html', title=title, form=form)


# -----------------------------------------------------------------------------------------------

@app.route('/mycontacts')
@login_required
def myposts():
    title = 'MY POSTS'
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('mycontacts.html', title=title, posts=posts)


@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    context = {
        'post': post,
        'name': post.name,
        'form': DeletePostForm()
    }
    return render_template('post_detail.html', **context)


@app.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    title = f'UPDATE {post.name}'
    if post.author.id != current_user.id:
        flash("You cannot update another user's post. Who do you think you are?", "warning")
        return redirect(url_for('mycontacts'))
    update_form = PostForm()
    if request.method == 'POST' and update_form.validate_on_submit():
        post.name = update_form.name.data
        post.last_name = update_form.last_name.data
        post.phone = update_form.phone.data

        # post.name = post.name
        # post.last_name = post.last_name
        # post.phone = post.phone

        db.session.commit()

        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_update.html', title=title, post=post, form=update_form)


@app.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash("You cannot delete another user's post. Who do you think you are?", "warning")
        return redirect(url_for('mycontacts'))
    form = DeletePostForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.name} has been deleted', 'info')
        return redirect(url_for('index'))
    return redirect(url_for('index'))