from flask import Flask, render_template, flash, request, redirect, jsonify
from Backend import gemini


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
        print(foods)
        return jsonify({'message': 'File uploaded successfully'})
    


if __name__ == '__main__':
    app.run(debug=True)
