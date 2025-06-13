import MySQLdb
import random
import string
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

# Auto Generated ID's
def generate_random_orderid(length=4):
    """ Generate a random Order ID in the format 'ORDER-XXXX' where XXXX is a random 4-digit number."""
    return 'ORDER-' + ''.join(random.choices(string.digits, k=length))
def generate_random_customerid(length=5):
    """ Generate a random Customer ID in the format 'CUST-XXXXX' where XXXXX is a random 5-digit number."""
    return 'CUST-' + ''.join(random.choices(string.digits, k=length))
def generate_random_trans_id(length=4):
    """ Generate a random Transaction ID in the format 'TRANS-XXXX' where XXXX is a random 4-digit number"""
    return 'TRANS-' + ''.join(random.choices(string.digits, k=length))

# Database Connection Order Page
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
        promo_code = request.form.get('promo_code')
        payment_mtd = request.form.get('payment_mtd')
        trans_id = request.form.get('trans_id')

        if not all([orderid, customerid, customername, orderdate, address, quantity, productname, 
                    price, delivery, payment_sts, promo_code, payment_mtd, trans_id]):
            flash("All fields are required!", 'error')
            return redirect(url_for('orders'))

        cursor = db.cursor()
        try:
            sql = """
                INSERT INTO orders (Order_ID, Customer_ID, Customer_Name, Order_Date, Address, Quantity, Product_Name, 
                Price, Delivery, Payment_Status, Promo_Code, Payment_Method, Transaction_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s)"""
            values = (orderid, customerid, customername, orderdate, address, quantity, productname, 
                      price, delivery, payment_sts, promo_code, payment_mtd, trans_id)
            cursor.execute(sql, values)
            db.commit()
            return render_template('order.html', success=True, orderid=orderid, customerid=customerid)

        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)
            return render_template('order.html', error=error, orderid=orderid, customerid=customerid)

        finally:
            cursor.close()

    # For GET request, generate new IDs
    orderid = generate_random_orderid()
    customerid = generate_random_customerid()
    trans_id = generate_random_trans_id()
    return render_template('order.html', orderid=orderid, customerid=customerid, trans_id=trans_id)

# Database Connection Reservation Page
@app.route('/reservation.html', methods=['GET', 'POST'])
def reservation_db():
    if request.method == 'POST':
        name = request.form('name')
        email = request.form('email')
        phone = request.form('phone')
        reservation_date = request.form('reservation_date')
        reservation_time = request.form('reservation_time')
        guests = request.form('guests')
        special_requests = request.form.get('special_requests')
        other_requests = request.form.get('other_requests')
        payment = request.form('payment')
        trans_id = request.form('trans_id')
        amount = request.form('amount')
        status = request.form('status')

        print("Received Data:", request.form)

        if not all([name, email, phone, reservation_date, reservation_time, guests, 
                    special_requests, other_requests, payment, trans_id, amount, status]):
            error = "All fields are required!"
            flash(error, 'error')
            return redirect(url_for('reservation'))
        
        cursor = db.cursor()
        try:
            # Insert into database
            sql = """
                INSERT INTO reservations (Reservation_ID, Name, Email, Phone_No, Reservation_Date, Reservation_Time, Number_of_Guests, 
                            Special_Request, Other_Request, Payment_Method, Transaction_ID, Amount, Reservation_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s)
                """
            values = (name, email, phone, reservation_date, reservation_time, guests, 
                    special_requests, other_requests, payment, trans_id, amount, status)

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/reservation.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)  # Log the error
            return render_template('/reservation.html', error=error)

        finally:
            cursor.close()
    return render_template('reservation.html')

# Database Connection Review Page
# @app.route('/reviews.html', methods=['GET', 'POST'])
# def reviews_db():
#     if request.method == 'POST':
#         c_name = request.form('c_name')
#         remarks = request.form('remarks')

#         print("Received Data:", request.form)

#         if not all([c_name, remarks]):
#             error = "All fields are required!"
#             flash(error, 'error')
#             return redirect(url_for('reservation'))
        
#         cursor = db.cursor()
#         try:
#             # Insert into database
#             sql = """
#                 INSERT INTO reviews (Customer_Name, Feedback)
#                 VALUES (%s, %s)
#                 """
#             values = (c_name, remarks)

#             cursor.execute(sql, values)
#             db.commit()
            
#             return render_template('/reservation.html', success=True)
        
#         except MySQLdb.Error as e:
#             error = f"Database error: {str(e)}"
#             print(error)  # Log the error
#             return render_template('/reservation.html', error=error)

#         finally:
#             cursor.close()
#     return render_template('reservation.html')

if __name__ == '__main__':
    app.run(debug=True)