import MySQLdb
from flask import Flask, flash, render_template, request, jsonify
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = '123789456'

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurant_management'

db = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    passwd=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

# Home Page
@app.route('/')
def home():
    return render_template('homescreen.html')

# Admin Page
@app.route('/admin.html')
def adminscreen():
    return render_template('admin.html')

# cart Page
@app.route('/cart.html')
def cart():
    return render_template('cart.html')

# Menu Page
@app.route('/menu.html')
def menu():
    return render_template('menu.html')

# Reservation Page
@app.route('/reservation.html')
def reservation():
    return render_template('reservation.html')

# Review Page
@app.route('/reviews.html')
def review():
    return render_template('reviews.html')

# Contact Page
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# Order Page
@app.route('/order.html')
def order():
    return render_template('order.html')

# Database Connection
if __name__ == '__main__':
    app.run(debug=True)