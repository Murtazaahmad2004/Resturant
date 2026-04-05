CREATE DATABASE resturant;
USE resturant;

CREATE TABLE orders (
    Order_ID VARCHAR(20) PRIMARY KEY,
    Customer_ID VARCHAR(20),
    Customer_Name VARCHAR(100),
    Order_Date DATE,
    Address TEXT,
    Quantity INT,
    Product_Name VARCHAR(100),
    Price DECIMAL(10,2),
    Delivery VARCHAR(50),
    Payment_Status VARCHAR(50),
    Payment_Method VARCHAR(50),
    Transaction_ID VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
    Reservation_ID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone_No VARCHAR(20),
    Reservation_Date DATE,
    Reservation_Time TIME,
    Number_of_Guests INT,
    Special_Request TEXT,
    Other_Request TEXT,
    Payment_Method VARCHAR(50),
    Transaction_ID VARCHAR(20),
    Amount DECIMAL(10,2),
    Reservation_Status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    weight VARCHAR(20),
    price INT
);

CREATE TABLE reviews (
    Review_ID INT AUTO_INCREMENT PRIMARY KEY,
    Customer_Name VARCHAR(100),
    Feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);