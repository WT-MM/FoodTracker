from flask import Flask, render_template, flash, request, redirect, jsonify


app =  Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save('uploads/' + file.filename)
        return jsonify({'message': 'File uploaded successfully'})
    


if __name__ == '__main__':
    app.run(debug=True)
