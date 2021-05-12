from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import UserInfoForm
from app.models import User, Post

@app.route('/')
def index():
    context = {
       'title': 'HOME',
       'posts': Post.query.all(),
       'user': {
            'id': 2,
            'username': 'Brian'
        }  
    }
    return render_template('index.html', **context)


@app.route('/phone_register', methods=['GET', 'POST'])
def register():
    title = 'REGISTER'
    form = UserInfoForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        phone = form.phone.data
        # print(username, email, password)
        # Check if username/email already exists
        existing_user = User.query.filter((User.name == name) | (User.last_name == last_name)).all()
        if existing_user:
            flash('That username or email already exists. Please try again', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(name, last_name, phone)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you {name} {last_name} for registering!', 'success')
        return redirect(url_for('index'))


    return render_template('phone_register.html', title=title, form=form)
