from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory
from forms import RegistrationForm, LoginForm
from models import db, User, Consultation, Message
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__, template_folder='.', static_folder='')

# Configure the PostgreSQL database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.rorllosppiqkybjszkgu:oQe0CzXvjDV4B6HI@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvcmxsb3NwcGlxa3lianN6a2d1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMDI4NTgxNSwiZXhwIjoyMDM1ODYxODE1fQ.dSzJc_rGiKjPXzYlbGmiM18iB8VZneEd4vfN_2b9-YE'

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=False)  # Set is_admin to False
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('register2.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login2.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/")
@login_required
def home():
    return render_template('index2.html', username=current_user.username if current_user.is_authenticated else None)

# Route to serve styles2.css
@app.route('/styles2.css')
def styles():
    return send_from_directory(app.root_path, 'styles2.css')

# Route to serve images from the images folder
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(os.path.join(app.root_path, 'images'), filename)

if __name__ == "__main__":
    app.run(debug=True)
