#TODO change /OCR to run pipeline_cropAndFinal (add missing stuff from pipeline_OCR) as necessary

from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/OCR')
def buttons():
    return render_template("buttons.html")
    subprocess.run(["python3 pipeline_cropAndFinal.py"])




@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)