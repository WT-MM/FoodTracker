from flask import Flask, render_template, flash, request, redirect, jsonify
from Backend import gemini, newReadData


app =  Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    


if __name__ == '__main__':
    app.run(debug=True)
