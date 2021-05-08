
import logging
import pathlib
from tokenize import Double
from requests import Session
import sqlalchemy as db
import sqlalchemy.dialects.sqlite
from configparser import ConfigParser
from sqlalchemy.orm import sessionmaker

# Gets the Face Data from the Face data
PATH = str(pathlib.Path().absolute())+"/src/prosessing/"+"Config.ini"


def getFaces():
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(PATH)

    # Get the password
    database = config_object["DATABASE"]

    engine = db.create_engine('postgresql://'+ str(database['user'])+":"+str(database['pass'])+"@"+str(database['ip'])+":"+str(database['port'])+"/"+str(database['databasename']))
    connection = engine.connect()
    metadata = db.MetaData()
    faces = db.Table(database['table'], metadata,
                     autoload=True, autoload_with=engine)
    logging.warn("got table...")
    query = db.select([faces])
    logging.warn("got querying....")
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    logging.warn("got result returning")
    return(result_set)

# Returns the LifeTime Table result set
def getLifetime():
  
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(PATH)

    # Get the password
    database = config_object["DATABASE"]

    engine = db.create_engine('postgresql://'+ str(database['user'])+":"+str(database['pass'])+"@"+str(database['ip'])+":"+str(database['port'])+"/"+str(database['databasename']))
    connection = engine.connect()
    metadata = db.MetaData()
    faces = db.Table(database['Lifetable'], metadata,
                     autoload=True, autoload_with=engine)
    logging.warn("got table...")
    query = db.select([faces])
    logging.warn("got querying....")
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    logging.warn("got result returning")
    return(result_set)

'''
Return the amout of Entrys in the  dataBase 
'''
def getAmountOfEntrys():
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(PATH)

    # Get the password
    database = config_object["DATABASE"]

    engine = db.create_engine('postgresql://'+ str(database['user'])+":"+str(database['pass'])+"@"+str(database['ip'])+":"+str(database['port'])+"/"+str(database['databasename']))
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = db.MetaData()
    faces = db.Table(database['table'], metadata,
                     autoload=True, autoload_with=engine)
    print("The Amount of Entrys that are in the Table are" + str(session.query(faces).count()))
    print("the type is"+str(type(session.query(faces).count())))
    databasecount = int(float(session.query(faces).count()))
    return databasecount

# this is the seen Amout life time database
def getAmountOfLifeEntrys():
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(PATH)

    # Get the password
    database = config_object["DATABASE"]

    engine = db.create_engine('postgresql://'+ str(database['user'])+":"+str(database['pass'])+"@"+str(database['ip'])+":"+str(database['port'])+"/"+str(database['databasename']))
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = db.MetaData()
    faces = db.Table(database['lifetable'], metadata,
                     autoload=True, autoload_with=engine)
    print("The Amount of Entrys that are in the Table are" + str(session.query(faces).count()))
    return session



# this is for handling Setting The face count data
def setLifetimeFaceCount(session,faceCount):
    data = session.query.filter_by().first()
    data.seenFaces = faceCount
    session.add(data)
    session.commit()
    logging.info("Seaved Life time Face count")


# this is for handling Setting The face count data
def setLifetimePlateCount(session,plateCount):
    data = session.query.filter_by().first()
    data.seenPlates = plateCount
    session.add(data)
    session.commit()
    logging.info("Seaved Life time Plate count")


def getKey(result_set, i):
    print(result_set[i])
    return result_set[i]


def getID(result_set, i):
    id, useruuid, user, groub, image, imageurl = result_set[i]
    return id

    # gets Database entry name


def getName(result_set, i):
    id, useruuid, user, group, image, imageurl = result_set[i]
    return user


def getStatus(result_set, i):
    id, useruuid, user, group, image, imageurl = result_set[i]
    return group


def getImageName(result_set, i):
    id, useruuid,user, group, image, imageurl = result_set[i]
    return image

def getImageUrI(result_set, i):
    id, useruuid, user, group, image, imageurl = result_set[i]
    return imageurl

def getUserUUID(result_set, i):
    id, useruuid,user, group, image, imageurl = result_set[i]
    return useruuid



def getLifefaces(result_set, i):
    id,seenFaces,seenPlates = result_set[i]
    return seenFaces


def getLifePlates(result_set, i):
    id,seenFaces,seenPlates = result_set[i]
    return seenPlates
