from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import InputRequired, Email, NumberRange
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Define the SQLite database
DATABASE = 'user_data.db'

# Create a database connection function
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Create the user table if it doesn't exist
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Create a Flask form for user input
class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=0)])
    dob = DateField('Date of Birth', validators=[InputRequired()])

# Route for the main page with the form
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        age = form.age.data
        dob = form.dob.data

        db = get_db()
        db.execute('INSERT INTO users (name, email, age, dob) VALUES (?, ?, ?, ?)',
                   [name, email, age, dob])
        db.commit()
        return redirect(url_for('users'))
    return render_template('index.html', form=form)

# Route for displaying users from the database
@app.route('/users')
def users():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
