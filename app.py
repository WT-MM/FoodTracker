from flask import Flask, render_template, flash, request, redirect, jsonify
from Backend import gemini, newReadData
import json


app =  Flask(__name__)

user = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    with open("userData.json", "r") as file:
        data = json.load(file)
        user_data = data[user]
    return render_template('home.html', foodData=user_data)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save('uploads/' + file.filename)
        foods = gemini.name_foods('uploads/' + file.filename)
        retData = {}
        for food in foods:
            retData[food] = newReadData.get_min_fridge_expiration_time_in_days(food)
        
        return jsonify({'message': 'File uploaded successfully', 'foodData': retData})
    

@app.route('/sign-in', methods=['POST'])
def login():
    global user
    if request.method == 'POST':
        # Get the account information from the request
        username = request.form['username']
        password = request.form['password']

        user = username

        # Read the account information from the JSON file
        with open('accounts.json', 'r') as file:
            accounts = file.readlines()

        # Check if the account information is correct
        for account in accounts:
            account = json.loads(account)
            if account['username'] == username and account['password'] == password:
                return jsonify({'message': 'Login successful', 'continue': True})

        return jsonify({'message': 'Login failed', 'continue': False})

@app.route('/create-account', methods=['GET'])
def create_account_page():
    return render_template('create-account.html')

@app.route('/create-account', methods=['POST'])
def create_account():
    global user
    if request.method == 'POST':
        # Get the account information from the request
        username = request.form['username']
        password = request.form['password']
        

        # Create a dictionary with the account information
        account = {
            'username': username,
            'password': password
        }

        user = username

         # Write the account information to a JSON file
        with open('accounts.json', 'a') as file:
            json.dump(account, file)
            file.write('\n')

        return jsonify({'message': 'Account created successfully', "success": True})



if __name__ == '__main__':
    app.run(debug=True)
