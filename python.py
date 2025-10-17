from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import mysql.connector
import random
import string

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

# Order Page
def generate_random_orderid(length=4):
    return 'ORDER-' + ''.join(random.choices(string.digits, k=length))

def generate_random_customerid(length=5):
    return 'CUST-' + ''.join(random.choices(string.digits, k=length))

def generate_random_trans_id(length=4):
    return 'TRANS-' + ''.join(random.choices(string.digits, k=length))

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
        else:
            trans_id = request.form.get('trans_id')

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
            error=error, 
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
# def generate_random_res_id(length=4):
#     return 'RESER-' + ''.join(random.choices(string.digits, k=length))

# def generate_random_trans_id(length=4):
#     return 'TRANS-' + ''.join(random.choices(string.digits, k=length))

# @app.route('/reservation.html')
# def reservation_page():
#     res_id = generate_random_res_id()
#     trans_id = generate_random_trans_id()
#     return render_template('reservation.html', res_id=res_id, trans_id=trans_id)

# @app.route('/reservation', methods=['GET', 'POST'])
# def reservation():
#     if request.method == 'POST':
#         res_id = request.form.get('res_id')
#         name = request.form.get('name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         reservation_date = request.form.get('reservation_date')
#         reservation_time = request.form.get('reservation_time')
#         guests = request.form.get('guests')
#         special_requests = ', '.join(request.form.getlist('special_requests'))  # handle multiple checkboxes
#         other_request = request.form.get('other_request')
#         payment = request.form.get('payment')
#         trans_id = request.form.get('trans_id')
#         amount = request.form.get('amount')
#         status = request.form.get('status')

#         if payment == 'cash':
#             trans_id = 'Nill'
#         else:
#             trans_id = request.form.get('trans_id')

#         # Check for empty fields
#         if not all([res_id, name, email, phone, reservation_date, reservation_time, guests,
#                     payment, amount, status]):
#             error = "⚠️ All fields are required"
#             return render_template('reservation.html', error=error, res_id=res_id, trans_id=trans_id)

#         cursor = db.cursor()
#         try:
#             cursor.execute("""
#                 INSERT INTO reservations (
#                     Reservation_ID, Name, Email, Phone_No, Reservation_Date, Reservation_Time,
#                     Number_of_Guests, Special_Request, Other_Request, Payment_Method,
#                     Transaction_ID, Amount, Reservation_Status
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (
#                 res_id, name, email, phone, reservation_date, reservation_time, guests,
#                 special_requests, other_request, payment, trans_id, amount, status
#             ))
#             db.commit()
#             success = "✅ Reservation submitted successfully!"
#             return render_template('reservation.html', success=success,
#                                    res_id=generate_random_res_id(), trans_id=generate_random_trans_id())
#         except Exception as e:
#             print("Error inserting into database:", e)
#             error = f"Failed to insert reservation: {str(e)}"
#             return render_template('reservation.html', error=error, res_id=res_id, trans_id=trans_id)
#         finally:
#             cursor.close()

#     res_id = generate_random_res_id()
#     trans_id = generate_random_trans_id()
#     return render_template('reservation.html', res_id=res_id, trans_id=trans_id)

# # Review page
# @app.route('/reviews', methods=['GET', 'POST'])
# def reviews():
#     if request.method == 'POST':
#         c_name = request.form.get('c_name')
#         remarks = request.form.get('remarks')

#         # Check for empty fields
#         if not all([c_name, remarks]):
#             error = "⚠️ All fields are required"
#             return render_template('reviews.html', error=error)

#         cursor = db.cursor()
#         try:
#             cursor.execute("""
#                 INSERT INTO reviews (
#                     Customer_Name, Feedback
#                 ) VALUES (%s, %s)
#             """, (
#                 c_name, remarks
#             ))
#             db.commit()
#             success = "✅ Review submitted successfully!"
#             return render_template('reviews.html', success=success)
#         except Exception as e:
#             print("Error inserting into database:", e)
#             error = f"Failed to insert review: {str(e)}"
#             return render_template('reviews.html', error=error)
#         finally:
#             cursor.close()

#     return render_template('reviews.html')

if __name__ == '__main__':
    app.run(host="192.168.100.3", port=5000, debug=True)