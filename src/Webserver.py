    """
This python class is for hosting image alearts to our push notification system in a simple web url
"""
    
from flask import Flask
from flask.helpers import send_file
app = Flask(__name__)



@app.route('/')
def root(Location, name):
    return send_file(Location+name+".jpg")



@app.route('/parents')
def parentImage(Location,fileprefix,name):
    return send_file(Location+fileprefix+name+".jpg")


@app.route('/unknown')
def unknownUser(Location,fileprefix,name):
    return send_file(Location+fileprefix+name+".jpg")
    

def StartServer():
    app.run(debug=True, host='0.0.0.0:80')