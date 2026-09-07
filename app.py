from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import random
import string
import os

app = Flask(__name__)
CORS(app)

app.secret_key = '123789456'


# =========================================================
# SQLite Database Configuration
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'restaurant.db')


# =========================================================
# Database Connection
# =========================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# Create Database Tables
# =========================================================

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ---------------- MENU TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight TEXT,
            price REAL NOT NULL
        )
    """)

    # ---------------- ORDERS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Order_ID TEXT UNIQUE NOT NULL,
            Customer_ID TEXT,
            Customer_Name TEXT,
            Order_Date TEXT,
            Address TEXT,
            Quantity TEXT,
            Product_Name TEXT,
            Price REAL,
            Delivery TEXT,
            Payment_Status TEXT,
            Payment_Method TEXT,
            Transaction_ID TEXT
        )
    """)

    # ---------------- RESERVATIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Reservation_ID TEXT UNIQUE NOT NULL,
            Name TEXT,
            Email TEXT,
            Phone_No TEXT,
            Reservation_Date TEXT,
            Reservation_Time TEXT,
            Number_of_Guests INTEGER,
            Special_Request TEXT,
            Other_Request TEXT,
            Payment_Method TEXT,
            Transaction_ID TEXT,
            Amount REAL,
            Reservation_Status TEXT
        )
    """)

    # ---------------- REVIEWS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_Name TEXT,
            Feedback TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# Initialize Database
# =========================================================

init_db()


# =========================================================
# Home Page
# =========================================================

@app.route('/')
def home():
    return render_template('homescreen.html')


# =========================================================
# Cart Page
# =========================================================

@app.route('/cart.html')
def cart():
    return render_template('cart.html')


# =========================================================
# Menu Page
# =========================================================

@app.route('/menu.html')
def menu():
    return render_template('menu.html')


# =========================================================
# Review Page
# =========================================================

@app.route('/reviews.html')
def review():
    return render_template('reviews.html')


# =========================================================
# Contact Page
# =========================================================

@app.route('/contact.html')
def contact():
    return render_template('contact.html')


# =========================================================
# Billing Page
# =========================================================

@app.route('/billing.html')
def billing():
    return render_template('billing.html')


# =========================================================
# Generate Random IDs
# =========================================================

def generate_random_orderid(length=8):
    return 'ORDER-' + ''.join(
        random.choices(string.digits, k=length)
    )


def generate_random_customerid(length=8):
    return 'CUST-' + ''.join(
        random.choices(string.digits, k=length)
    )


def generate_random_trans_id(length=8):
    return 'TRANS-' + ''.join(
        random.choices(string.digits, k=length)
    )


def generate_random_res_id(length=8):
    return 'RESERV-' + ''.join(
        random.choices(string.digits, k=length)
    )


# =========================================================
# Order Page
# =========================================================

@app.route('/order.html')
def order():

    orderid = generate_random_orderid()
    customerid = generate_random_customerid()
    trans_id = generate_random_trans_id()

    return render_template(
        'order.html',
        orderid=orderid,
        customerid=customerid,
        trans_id=trans_id
    )


# =========================================================
# Order POST
# =========================================================

@app.route('/order', methods=['GET', 'POST'])
def orders():

    if request.method == 'POST':

        orderid = request.form.get('orderid')
        customerid = request.form.get('customerid')
        customername = request.form.get('customername')
        orderdate = request.form.get('orderdate')
        address = request.form.get('address')
        quantity = request.form.get('quantity')
        productname = request.form.get('productname')
        price = request.form.get('price')
        delivery = request.form.get('delivery')
        payment_sts = request.form.get('payment_sts')
        payment_mtd = request.form.get('payment_mtd')
        trans_id = request.form.get('trans_id')

        # Cash payment does not need transaction ID
        if payment_mtd == 'Cash':
            trans_id = 'Nill'

        conn = None
        cursor = None

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO orders (
                    Order_ID,
                    Customer_ID,
                    Customer_Name,
                    Order_Date,
                    Address,
                    Quantity,
                    Product_Name,
                    Price,
                    Delivery,
                    Payment_Status,
                    Payment_Method,
                    Transaction_ID
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                orderid,
                customerid,
                customername,
                orderdate,
                address,
                quantity,
                productname,
                price,
                delivery,
                payment_sts,
                payment_mtd,
                trans_id
            ))

            conn.commit()

            success = "✅ Order successfully Placed!"
            error = None

        except Exception as e:

            if conn:
                conn.rollback()

            success = None
            error = f"❌ Failed to insert order: {e}"

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        return render_template(
            'order.html',
            success=success,
            error=error,
            orderid=orderid,
            customerid=customerid,
            trans_id=trans_id
        )

    # GET request

    orderid = generate_random_orderid()
    customerid = generate_random_customerid()
    trans_id = generate_random_trans_id()

    return render_template(
        'order.html',
        orderid=orderid,
        customerid=customerid,
        trans_id=trans_id
    )


# =========================================================
# Reservation
# =========================================================

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():

    if request.method == 'POST':

        res_id = request.form.get('res_id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        reservation_date = request.form.get('reservation_date')
        reservation_time = request.form.get('reservation_time')
        guests = request.form.get('guests')

        special_requests = ', '.join(
            request.form.getlist('special_requests')
        )

        other_request = request.form.get('other_request')
        payment = request.form.get('payment')
        trans_id = request.form.get('trans_id')
        amount = request.form.get('amount')
        status = request.form.get('status')

        # Cash payment
        if payment == 'Cash':
            trans_id = 'Nill'

        conn = None
        cursor = None

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO reservations (
                    Reservation_ID,
                    Name,
                    Email,
                    Phone_No,
                    Reservation_Date,
                    Reservation_Time,
                    Number_of_Guests,
                    Special_Request,
                    Other_Request,
                    Payment_Method,
                    Transaction_ID,
                    Amount,
                    Reservation_Status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                res_id,
                name,
                email,
                phone,
                reservation_date,
                reservation_time,
                guests,
                special_requests,
                other_request,
                payment,
                trans_id,
                amount,
                status
            ))

            conn.commit()

            success = "✅ Reservation Successfully Submitted!"
            error = None

        except Exception as e:

            if conn:
                conn.rollback()

            success = None
            error = f"❌ Failed to insert reservation: {e}"

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        return render_template(
            'reservation.html',
            success=success,
            error=error,
            res_id=res_id,
            trans_id=trans_id
        )

    # GET request

    res_id = generate_random_res_id()
    trans_id = generate_random_trans_id()

    return render_template(
        'reservation.html',
        res_id=res_id,
        trans_id=trans_id
    )


# =========================================================
# Reviews
# =========================================================

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'POST':

        c_name = request.form.get('c_name')
        remarks = request.form.get('remarks')

        conn = None
        cursor = None

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO reviews (
                    Customer_Name,
                    Feedback
                )
                VALUES (?, ?)
            """, (
                c_name,
                remarks
            ))

            conn.commit()

            success = "✅ Review Submitted Successfully!"
            error = None

        except Exception as e:

            if conn:
                conn.rollback()

            success = None
            error = f"❌ Failed to insert review: {e}"

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        return render_template(
            'reviews.html',
            success=success,
            error=error
        )

    return render_template('reviews.html')


# =========================================================
# Add Menu API
# =========================================================

@app.route('/add_menu', methods=['POST'])
def add_menu():

    data = request.json

    if not data:
        return jsonify({
            "error": "No menu data received"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        for item in data:

            name = item.get('name')
            weight = item.get('weight')
            price = item.get('price')

            cursor.execute("""
                INSERT INTO menu (
                    name,
                    weight,
                    price
                )
                VALUES (?, ?, ?)
            """, (
                name,
                weight,
                price
            ))

        conn.commit()

        return jsonify({
            "message": "Menu added successfully"
        })

    except Exception as e:

        if conn:
            conn.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# Get Menu List
# =========================================================

@app.route('/get_menu', methods=['GET'])
def get_menu():

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, weight, price
            FROM menu
        """)

        rows = cursor.fetchall()

        menu_list = []

        for row in rows:

            menu_list.append({
                "id": row["id"],
                "name": row["name"],
                "weight": row["weight"],
                "price": row["price"]
            })

        return jsonify(menu_list)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# Fetch Menu - Postman
# =========================================================

@app.route('/fetch_menu', methods=['POST'])
def fetch_menu():

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, weight, price
            FROM menu
        """)

        rows = cursor.fetchall()

        menu_list = []

        for row in rows:

            menu_list.append({
                "id": row["id"],
                "dish_name": row["name"],
                "quantity": row["weight"],
                "price": row["price"]
            })

        return jsonify({
            "success": 1,
            "data": menu_list
        })

    except Exception as e:

        return jsonify({
            "success": 0,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# API Menu
# =========================================================

@app.route('/api/menu', methods=['GET'])
def fetch_api_menu():

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, weight, price
            FROM menu
        """)

        rows = cursor.fetchall()

        menu_list = []

        for row in rows:

            menu_list.append({
                "id": row["id"],
                "name": row["name"],
                "weight": row["weight"],
                "price": float(row["price"])
            })

        return jsonify({
            "success": 1,
            "data": menu_list
        })

    except Exception as e:

        return jsonify({
            "success": 0,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# Run Flask App
# =========================================================

if __name__ == '__main__':
    app.run(debug=True)