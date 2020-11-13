"""
This python class is for hosting image alearts to our push notification system in a simple web url
"""
    
from flask import Flask
import flask
from flask.helpers import send_file
app = Flask(__name__)



@app.route('/')
def root():
    return send_file('index.html')


    


app.run(debug=True, host='127.0.0.1')