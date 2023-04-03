from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/zippee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="utkarsh123456789"
DB_HOST="localhost"
DB_NAME="zippee"
DB_USER="postgres"
DB_PASS="admin"
conn=psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@app.route('/api/data')
def get_data():
    data = {'message': 'Hello, World!'}
    return jsonify(data)


@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("DATA Dict", request.get_data())
    data=request.get_data()
    if request.method == 'POST':       
        username = request.form.get('fullName')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not password:
            flash('Please enter a valid username and password.')
            return redirect(url_for('register'))
        cursor.execute("SELECT  FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        if user_data:
            flash('Username already taken')
        else:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            conn.commit()
            flash('Registration successful')
        return redirect(url_for('login'))

    return "Registration complete"

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))

    return "render_template('login.html')"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
