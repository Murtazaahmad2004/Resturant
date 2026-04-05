from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import mysql.connector
import random
import string

import requests

app = Flask(__name__)
CORS(app)

app.secret_key = '123789456'

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'NHA@2004',
    'database': 'resturant'
}

# Home Page
@app.route('/')
def home():
    return render_template('homescreen.html')

# cart Page
@app.route('/cart.html')
def cart():
    return render_template('cart.html')

# Menu Page
@app.route('/menu.html')
def menu():
    return render_template('menu.html')

# Review Page
@app.route('/reviews.html')
def review():
    return render_template('reviews.html')

# Contact Page
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# Billing Page
@app.route('/billing.html')
def billing():
    return render_template('billing.html')
# Order Page
def generate_random_orderid(length=8):
    return 'ORDER-' + ''.join(random.choices(string.digits, k=length))

def generate_random_customerid(length=8):
    return 'CUST-' + ''.join(random.choices(string.digits, k=length))

def generate_random_trans_id(length=8):
    return 'TRANS-' + ''.join(random.choices(string.digits, k=length))

def generate_random_res_id(length=8):
    return 'RESERV-' + ''.join(random.choices(string.digits, k=length))

# Route for GET (display form with auto-generated IDs)
@app.route('/order.html')
def order():
    orderid = generate_random_orderid()
    customerid = generate_random_customerid()
    trans_id = generate_random_trans_id()
    return render_template('order.html', orderid=orderid, customerid=customerid, trans_id=trans_id)

# Route for POST (form submission)
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

        if payment_mtd == 'Cash':
            trans_id = 'Nill'
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO orders (
                    Order_ID, Customer_ID, Customer_Name, Order_Date, Address, Quantity, 
                    Product_Name, Price, Delivery, Payment_Status, Payment_Method, Transaction_ID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                orderid, customerid, customername, orderdate, address, quantity, productname, 
                price, delivery, payment_sts, payment_mtd, trans_id
            ))
            conn.commit()
            success = "✅ Order successfully Placed!"
        except Exception as e:
            error = f"❌ Failed to insert items: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render_template(
            'order.html', 
            success=success if 'success' in locals() else None,
            error=error if 'error' in locals() else None,
            orderid=orderid, 
            customerid=customerid, 
            trans_id=trans_id
        )

    # If GET request, re-generate new IDs
    orderid = generate_random_orderid()
    customerid = generate_random_customerid()
    trans_id = generate_random_trans_id()
    return render_template('order.html', orderid=orderid, customerid=customerid, trans_id=trans_id)

# Reservation page
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
        special_requests = ', '.join(request.form.getlist('special_requests'))
        other_request = request.form.get('other_request')
        payment = request.form.get('payment')
        trans_id = request.form.get('trans_id')
        amount = request.form.get('amount')
        status = request.form.get('status')

        if payment == 'Cash':
            trans_id = 'Nill'

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO reservations (
                    Reservation_ID, Name, Email, Phone_No, Reservation_Date,
                    Reservation_Time, Number_of_Guests, Special_Request,
                    Other_Request, Payment_Method, Transaction_ID,
                    Amount, Reservation_Status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                res_id, name, email, phone, reservation_date,
                reservation_time, guests, special_requests,
                other_request, payment, trans_id,
                amount, status
            ))

            conn.commit()
            success = "✅ Reservation Successfully Submitted!"

        except Exception as e:
            error = f"❌ Failed to insert reservation: {e}"

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render_template(
            'reservation.html',
            success=success if 'success' in locals() else None,
            error=error if 'error' in locals() else None,
            res_id=res_id,
            trans_id=trans_id
        )

    # GET request
    res_id = generate_random_res_id()
    trans_id = generate_random_trans_id()
    return render_template('reservation.html', res_id=res_id, trans_id=trans_id)

# Review page
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':

        c_name = request.form.get('c_name')
        remarks = request.form.get('remarks')

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO reviews (
                    Customer_Name, Feedback
                ) VALUES (%s, %s)
            """, (c_name, remarks))

            conn.commit()
            success = "✅ Review Submitted Successfully!"

        except Exception as e:
            error = f"❌ Failed to insert review: {e}"

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render_template(
            'reviews.html',
            success=success if 'success' in locals() else None,
            error=error if 'error' in locals() else None
        )

    return render_template('reviews.html')

# Add Menu API POST request
@app.route('/add_menu', methods=['POST'])
def add_menu():
    data = request.json

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        for item in data:
            name = item['name']
            weight = item['weight']
            price = item['price']

            query = "INSERT INTO menu (name, weight, price) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, weight, price))

        conn.commit()

        return jsonify({"message": "Menu added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Get Menu List From API
@app.route('/get_menu', methods=['GET'])
def get_menu():
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM menu")
        result = cursor.fetchall()

        menu = []
        for row in result:
            menu.append({
                "id": row[0],
                "name": row[1],
                "weight": row[2],
                "price": row[3]
            })

        return jsonify(menu)

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# code for fetch data from postman
@app.route('/fetch_menu', methods=['POST'])
def fetch_menu():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, weight, price FROM menu")
        rows = cursor.fetchall()

        menu_list = []
        for row in rows:
            menu_list.append({
                "id": row[0],
                "dish_name": row[1],
                "quantity": row[2],
                "price": row[3]
            })

        return jsonify({
            "success": 1,
            "data": menu_list
        })

    except Exception as e:
        return jsonify({
            "success": 0,
            "message": str(e)
        })

@app.route('/api/menu', methods=['GET'])
def fetch_api_menu():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, weight, price FROM menu")
        rows = cursor.fetchall()
        menu_list = []
        for row in rows:
            menu_list.append({
                "id": row[0],
                "name": row[1],
                "weight": row[2],
                "price": float(row[3])
            })
        return jsonify({"success": 1, "data": menu_list})
    except Exception as e:
        return jsonify({"success": 0, "message": str(e)})
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)