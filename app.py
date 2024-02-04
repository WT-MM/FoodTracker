from flask import Flask, render_template, flash, request, redirect, jsonify
from Backend import gemini, newReadData, emailscript
import os
import json



app =  Flask(__name__)

user = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png')

@app.route('/dashboard')
def dashboard():
    with open("userData.json", "r") as file:
        data = json.load(file)
        #user_data = data[user]
    #return render_template('home.html', foodData=user_data)
    return render_template('home.html', foodData=[])#foodData=[{'name': "cow", 'date':"12-23-23"}])

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save('uploads/' + file.filename)
        foods = gemini.name_foods('uploads/' + file.filename)
        print(foods)
        retData = {}
        #for food in foods:
        #    retData[food] = newReadData.get_min_fridge_expiration_time_in_days(food)
        
        #foods = {"Apple" : "12-23-23"}
        for food in foods:
            asyncio.run(emailscript.send_email("EcoBean Expiration Alert", food['name'], user, food['date']))
        return jsonify({'message': 'File uploaded successfully', 'foodData': foods})
    

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
    return render_template('username2.html')

@app.route('/get-recipe', methods=['POST'])
def get_recipe():
    if request.method == 'POST':
        foods = request.form['foods']
        print(foods)
        recipes = gemini.get_recipe(foods)
        print(recipes)
        return jsonify({'message': 'Recipes found', 'recipes': recipes})

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
