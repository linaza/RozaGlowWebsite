from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
import products

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')
PASS_REGEX = re.compile(r'.*[A-Z].*[0-9]')

app = Flask(__name__)
app.secret_key = "ThisIsSecretadfasdfasdf!"

mysql = MySQLConnector(app,'login_reg')

@app.route('/')
def success():
        return render_template('login.html')

@app.route("/sign_out")
def sign_out():
    session.pop("user_id", None)

    return redirect('/login_page')

@app.route('/login_page')
def login_page():
    print(session)
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    print(session)
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register_user():
        query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        # We'll then create a dictionary of data from the POST data received.
        data = {
                'username': request.form['username'],
                'password': request.form['password'],
            }
        # Run query, with dictionary values injected into the query.
        mysql.query_db(query, data)
        return redirect('/')
#didn't get the hacker version done with the birthday stuff

###################################################################################
@app.route('/add',methods=['POST','GET'])
def addtocart():
    count = 0
    query = "INSERT INTO products (username, product) VALUES (:username, :product)"
    #print("test")
    bar = request.form['test']#clicked button id
    data = {
        'username': session['username'],
        'product': bar,
    }
    mysql.query_db(query, data)
    #here we should store product info in the products table for the same user 
    #return render_template('index.html')
    input_username = session['username']
    user_query = "SELECT product FROM products WHERE username = :username"
    query_data = {'username': input_username}
    stored_user = mysql.query_db(user_query, query_data)
    return_data = []
    save_products = products.products
    
    for row in stored_user:
        for product in save_products:
            if row['product'] == product["id"]:
                count = count + int(product["price"])
                return_data.append({
                    "id" : product["id"],
                    "name" : product["name"],
                    "price" : product["price"],
                    "description" : product["discreption"],
                    "img" : product["picUrl"]
                })
    print(return_data)
    print(count)
   # return redirect('/cart' ,l = stored_user ,count )
    return render_template('cart.html',l = return_data , sum = count ,username = input_username)
###################################################################################
@app.route('/remove',methods=['POST','GET'])
def removeFromCart():
    prod = request.form['test']#item to delete
    input_username = session['username']# username 
    user_query ="DELETE FROM products WHERE  username = :username AND  product = 5"
    query_data = {'username': input_username}
    stored_user = mysql.query_db(user_query, query_data)
    return redirect('/goToCart')


###################################################################################
@app.route('/goToCart', methods=['POST', 'GET'])
def goToCart():
    count = 0
    #query = "INSERT INTO products (username, product) VALUES (:username, :product)"
    #print("test")
   
    #here we should store product info in the products table for the same user 
    #return render_template('index.html')
    input_username = session['username']
    user_query = "SELECT product FROM products WHERE username = :username"
    query_data = {'username': input_username}
    stored_user = mysql.query_db(user_query, query_data)
    return_data = []
    save_products = products.products
    
    for row in stored_user:
        for product in save_products:
            if row['product'] == product["id"]:
                count = count + int(product["price"])
                return_data.append({
                    "id" : product["id"],
                    "name" : product["name"],
                    "price" : product["price"],
                    "description" : product["discreption"],
                    "img" : product["picUrl"]
                })
    return render_template('cart.html',l = return_data , sum = count ,username = input_username)

###################################################################################
@app.route('/home', methods=['POST', 'GET'])
def home():
     return render_template('index.html', products = products.products)
###################################################################################

@app.route('/login', methods=['POST', 'GET'])
def login():

    input_username = request.form['username']
    input_password = request.form['password']
    user_query = "SELECT * FROM users WHERE username = :username"
    query_data = {'username': input_username}
    stored_user = mysql.query_db(user_query, query_data)

    if not stored_user:
        flash("User does not exist!")
        return redirect('/login_page')

    else:
        if request.form['password'] == stored_user[0]['password']:
            session['user_id'] = stored_user[0]['id']
            session['username'] = stored_user[0]['username']
            return render_template('index.html', products = products.products)
        else:
            flash("Wrong password, try again!")
            return redirect('/login_page')
         
       
#you should read cart list and view it in one page as table with img , price ,...
# def Mycart():
#     i
#     if '_flashes' in session:
# # changed this line to be render so I could put in value = on the html page to save what the person typed when it didn't validate
#         return redirect('/')
app.run(debug=True)