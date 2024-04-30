from flask import Flask, render_template, request, flash, url_for, redirect
from sqlalchemy import create_engine, Column, String, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Increase the length of the secret key

engine = create_engine(os.getenv("DATABASE_URI"))
Session = sessionmaker(bind=engine)
FastFund_db = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    phone_number = Column(String(20), primary_key=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    balance = Column(Numeric(15, 2), default=0.00)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # if the user exists
    user = FastFund_db.query(User).filter_by(phone_number=username).first()

    if user and user.check_password(password):
        # Redirect the user
        return redirect(url_for('user_dashboard', full_name=user.full_name))
    else:
        # if failed, render the login page with an error
        flash("Invalid username or password. Please try again.", "error")
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']

        # Check if the user already exists
        existing_user = FastFund_db.query(User).filter_by(phone_number=phone_number).first()
        if existing_user:
            flash("User already exists. Please try again.", "error")
            return render_template('register.html')

        # If it doesn't
        new_user = User(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password_hash=generate_password_hash(password)
        )
        FastFund_db.add(new_user)
        try:
            FastFund_db.commit()
        except Exception as e:
            flash("An error occurred while registering. Please try again later.", "error")
            return redirect(url_for('register'))

        flash("Registration successful!", "success")
        return redirect(url_for('user_dashboard', full_name=full_name))  # Redirect to the user dashboard

    return render_template('register.html')

@app.route('/user_dashboard')
def user_dashboard():
    full_name = request.args.get('full_name')
    return render_template('user_dashboard.html', full_name=full_name)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.debug = True
    app.run(port=5000)
