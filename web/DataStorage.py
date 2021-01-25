""" 
This file handles the storage of all the Data for displaying on the web interface
"""
from tinydb import TinyDB, Query

db = TinyDB('facial_users.json')

class users(object):
    
    #sets up tiny db if non existint 
    def createUser(priv,name):
        db.insert({'privlage': str(priv,'utf-8'), 'user':str(name,'utf-8')})

    # gets all the users privlage in the database  
    def queryPriv():
        data =  Query()
        return db.search(data.privlage)

    # gets all the users
    def queryUser():
        data = Query()
        return db.search(data.user)

    # removes user a user selected user from the db
    def removeUser(name):
        data =  Query()
        db.remove(data.user == name)
        
