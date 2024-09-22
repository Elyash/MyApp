from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import RegistrationForm, LoginForm, GiftForm
from models import User, Gift, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload_gift', methods=['GET', 'POST'])
@login_required
def upload_gift():
    form = GiftForm()
    if form.validate_on_submit():
        gift = Gift(name=form.name.data, image_url=form.image_url.data, buy_link=form.buy_link.data, cost=form.cost.data, user_id=current_user.id)
        db.session.add(gift)
        db.session.commit()
        flash('Your gift has been uploaded!', 'success')
        print('added a new gift')
        return redirect(url_for('dashboard'))
    return render_template('upload_gift.html', form=form)

@app.route('/view_gifts')
@login_required
def view_gifts():
    gifts = Gift.query.all()
    return render_template('view_gifts.html', gifts=gifts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)
