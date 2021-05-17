from itertools import product
from app import app, db, mail
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
from app.forms import  UserInfoForm, LoginForm, DeletePostForm
from app.models import Products, ShoppingCart, User, Post
from app.forms import PostForm
from sqlalchemy.sql import func


@app.route('/')
def index():
    # add_products()
    
    return render_template('index.html')


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





def add_products():
    product1 = Products('Cubs-Cap', '2021 season Cubs Baseball Cap', '18', '1','/static/images/1.jpg')
    product2 = Products('Glove', 'Wilson A2000 Infield', '20', '1','/static/images/2.jpg')
    product3 = Products('BaseBall', 'Rawling MLB Official', '10', '1','/static/images/3.jpg')
    product4 = Products('MBL T-Shirt', 'MLB Official 2021 ', '9', '1','/static/images/4.jpg')
    product5 = Products('Bat', 'Rawling R45 short_Swing Bat', '15', '1','/static/images/5.jpg')
    product6 = Products('Batting Helmet', 'Molded Batting Helmet', '11', '1','/static/images/6.jpg')
    product7 = Products('Cleat', 'Nike,Soccer Cleat', '250', '2','/static/images/7.jpg')
    product8 = Products('Gear Bag', 'Nike Official Gear-Bag', '70', '2','/static/images/8.jpg')
    product9 = Products('Goalkeeper Glove', 'Adidas  Golkeeper Glove', '70', '2','/static/images/9.jpg')
    product10 = Products('Soccer Socks', 'Under Armour Over The Calf Socks', '15', '2','/static/images/10.jpg')
    product11 = Products('Shinguards', 'Adults X League Shinguards', '20', '2','/static/images/11.jpg')
    product12 = Products('Jersey', 'Leo Messi La-Liga Season 2020 Jersey', '50', '2','/static/images/12.jpg')
    product13 = Products('Basketball', 'Neverflat Comp Basketball 29.5', '40', '3','/static/images/13.jpg')
    product14 = Products('Net', 'All-Weather R/W/B Net', '5', '3','/static/images/14.jpg')
    product15 = Products('Back Atcha', 'Spalding Ball Return Training Aid', '15', '3','/static/images/15.jpg')
    product16 = Products('Basketball Shoe', 'Under Armor Unisex Basketball Shoe', '10', '3','/static/images/16.jpg')
    product17 = Products('Nike-A', 'Nike Elite Basketball Crew Socks X-Large', '15', '3','/static/images/17.jpg')
    product18 = Products('Mcdavid', '6500 Compression Arm Sleeve ', '8', '3','/static/images/18.jpg')

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)
    db.session.add(product6)
    db.session.add(product7)
    db.session.add(product8)
    db.session.add(product9)
    db.session.add(product10)
    db.session.add(product11)
    db.session.add(product12)
    db.session.add(product13)
    db.session.add(product14)
    db.session.add(product15)
    db.session.add(product16)
    db.session.add(product17)
    db.session.add(product18)
    db.session.commit()


@app.route('/products/<int:product_cat>' )
@login_required
def products1(product_cat):
    
    produc = Products.query.filter_by(category = product_cat).all()
    
    
    return render_template('products.html', product=produc )





@app.route('/products/<int:product_cat>/<int:product_id>' )
@login_required
def add_to_cart(product_cat,product_id):
    produc = Products.query.filter_by(category = product_cat).all()
    
    for prod in produc:
        if prod.id == product_id:
            prod=ShoppingCart(prod.name,prod.description,prod.price,prod.category,prod.image)
            db.session.add(prod)
            db.session.commit()
            
            



    return render_template('products.html', product=produc )



@app.route('/cart' )
@login_required
def cart():
    produc = ShoppingCart.query.all()
    total=ShoppingCart.gettotal()
      
    
    
    return render_template('cart.html', product=produc, total=total)



@app.route('/cart/<int:product_id>' )
@login_required
def delete_from_cart(product_id):
    produc = ShoppingCart.query.all()
    total=ShoppingCart.gettotal()
    for prod in produc:
        if prod.id == product_id:
            db.session.delete(prod)
            db.session.commit()
            total-=prod.price
            


    return redirect(url_for('cart'))




@app.route('/quantity' )
@login_required
def quantity():
    produc = ShoppingCart.query.all()
    total=ShoppingCart.gettotal()
      
    
    
    return render_template('cart.html', product=produc, total=total)




@app.route('/purchased' )
@login_required
def purchased():
    produc = ShoppingCart.query.all()
    total=ShoppingCart.gettotal()
    if total!=0:
        return render_template('purchased.html', product=produc, total=total)

    else:
        return redirect(url_for('cart'))


@app.route('/done' )
@login_required
def done():
    produc = ShoppingCart.query.all()
    for prod in produc:
            db.session.delete(prod)
            db.session.commit()

    else:
        return redirect(url_for('index'))        
            


    