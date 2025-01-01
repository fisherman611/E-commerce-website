import sqlite3
import pandas as pd

# File paths
customers_file = 'database/customers.csv'
products_file = 'database/products.csv'
carts_file = 'database/carts.csv'
orders_file = 'database/orders.csv'

def load_customers():
    """Load customers data from CSV file."""
    customers = pd.read_csv(customers_file)
    customers['id'] = customers['id'].astype(int)
    customers['email'] = customers['email'].fillna('').astype(str)
    customers['username'] = customers['username'].fillna('').astype(str)
    customers['password_hash'] = customers['password_hash'].fillna('').astype(str)
    customers['date_joined'] = pd.to_datetime(customers['date_joined'], errors='coerce').fillna(pd.Timestamp('1970-01-01'))
    return customers

def load_products():
    """Load products data from CSV file."""
    products = pd.read_csv(products_file)
    products['id'] = products['id'].astype(int)
    products['product_name'] = products['product_name'].fillna('').astype(str)
    products['current_price'] = products['current_price'].astype(float)
    products['previous_price'] = products['previous_price'].astype(float)
    products['in_stock'] = products['in_stock'].astype(int)
    products['product_picture'] = products['product_picture'].fillna('').astype(str)
    products['flash_sale'] = products['flash_sale'].astype(bool)
    products['date_added'] = pd.to_datetime(products['date_added'], errors='coerce').fillna(pd.Timestamp('1970-01-01'))
    products['product_description'] = products['product_description'].fillna('').astype(str)
    products['rating'] = products['rating'].astype(float)  # Add this line
    return products

def load_carts():
    """Load carts data from CSV file."""
    carts = pd.read_csv(carts_file)
    carts['id'] = carts['id'].astype(int)
    carts['quantity'] = carts['quantity'].astype(int)
    carts['customer_link'] = carts['customer_link'].astype(int)
    carts['product_link'] = carts['product_link'].astype(int)
    return carts

def load_orders():
    """Load orders data from CSV file."""
    orders = pd.read_csv(orders_file)
    orders['id'] = orders['id'].astype(int)
    orders['quantity'] = orders['quantity'].astype(int)
    orders['price'] = orders['price'].astype(float)
    orders['status'] = orders['status'].fillna('').astype(str)
    orders['payment_id'] = orders['payment_id'].fillna('').astype(str)
    orders['customer_link'] = orders['customer_link'].astype(int)
    orders['product_link'] = orders['product_link'].astype(int)
    return orders

# Connect to SQLite database
conn = sqlite3.connect('instance/ecommerce.sqlite3')
cursor = conn.cursor()

# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS customer")
cursor.execute("DROP TABLE IF EXISTS product")
cursor.execute("DROP TABLE IF EXISTS cart")
cursor.execute('DROP TABLE IF EXISTS "order"')

# Create new tables
cursor.execute("""
    CREATE TABLE customer (
        id INTEGER NOT NULL, 
        email VARCHAR(100), 
        username VARCHAR(100), 
        password_hash VARCHAR(150), 
        date_joined DATETIME, 
        PRIMARY KEY (id), 
        UNIQUE (email)
    )
""")

cursor.execute("""
    CREATE TABLE product (
        id INTEGER NOT NULL, 
        product_name VARCHAR(100) NOT NULL, 
        current_price FLOAT NOT NULL, 
        previous_price FLOAT NOT NULL, 
        in_stock INTEGER NOT NULL, 
        product_picture VARCHAR(1000) NOT NULL, 
        flash_sale BOOLEAN, 
        date_added DATETIME, 
        product_description TEXT NOT NULL,
        rating FLOAT, 
        PRIMARY KEY (id)
    )
""")

cursor.execute("""  
    CREATE TABLE cart (
        id INTEGER NOT NULL, 
        quantity INTEGER NOT NULL, 
        customer_link INTEGER NOT NULL, 
        product_link INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(customer_link) REFERENCES customer (id), 
        FOREIGN KEY(product_link) REFERENCES product (id)
    )
""")

cursor.execute("""
    CREATE TABLE "order" (
        id INTEGER NOT NULL, 
        quantity INTEGER NOT NULL, 
        price FLOAT NOT NULL, 
        status VARCHAR(100) NOT NULL, 
        payment_id VARCHAR(1000) NOT NULL, 
        customer_link INTEGER NOT NULL, 
        product_link INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(customer_link) REFERENCES customer (id), 
        FOREIGN KEY(product_link) REFERENCES product (id)
    )
""")

# Load datas
customers = load_customers()
products = load_products()
carts = load_carts()
orders = load_orders()

# Insert data into customer table
for _, customer in customers.iterrows():
    cursor.execute("""
        INSERT OR REPLACE INTO customer (id, email, username, password_hash, date_joined)
        VALUES (?, ?, ?, ?, ?)
    """, (customer['id'], customer['email'], customer['username'], customer['password_hash'], customer['date_joined'].strftime('%Y-%m-%d %H:%M:%S')))

# Insert data into product table
for _, product in products.iterrows():
    cursor.execute("""
        INSERT OR REPLACE INTO product (id, product_name, current_price, previous_price, in_stock, product_picture, flash_sale, date_added, product_description, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (product['id'], product['product_name'], product['current_price'], product['previous_price'], product['in_stock'], product['product_picture'], product['flash_sale'], product['date_added'].strftime('%Y-%m-%d %H:%M:%S'), product['product_description'], product['rating']))

# Insert data into cart table
for _, cart in carts.iterrows():
    cursor.execute("""
        INSERT OR REPLACE INTO cart (id, quantity, customer_link, product_link)
        VALUES (?, ?, ?, ?)
    """, (cart['id'], cart['quantity'], cart['customer_link'], cart['product_link']))

# Insert data into order table
for _, order in orders.iterrows():
    cursor.execute("""
        INSERT OR REPLACE INTO "order" (id, quantity, price, status, payment_id, customer_link, product_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order['id'], order['quantity'], order['price'], order['status'], order['payment_id'], order['customer_link'], order['product_link']))

# Commit changes and close connection
conn.commit()
conn.close()

print('Data imported successfully')
