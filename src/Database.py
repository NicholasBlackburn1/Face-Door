
import pathlib
from requests import Session
import sqlalchemy as db
import sqlalchemy.dialects.sqlite
from configparser import ConfigParser
from sqlalchemy.orm import sessionmaker
# Gets the Face Data from the Face data


def getFaces():
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(str(pathlib.Path().absolute())+"/src/"+"Config.ini")

    # Get the password
    database = config_object["DATABASE"]

    engine = db.create_engine(
        f'postgresql://'+database['user']+":"+database['pass']+'@'+database['ip']+":"+database['port']+'/'+database['databaseName'])
    connection = engine.connect()
    metadata = db.MetaData()
    faces = db.Table(database['table'], metadata,
                     autoload=True, autoload_with=engine)
    print(faces)
    query = db.select([faces])
    print(query)
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    print(result_set)
    return(result_set)

'''
Return the amout of Entrys in the  dataBase 
'''
def getAmountOfEntrys(logging):
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(str(pathlib.Path().absolute())+"/src/"+"Config.ini")

    # Get the password
    database = config_object["DATABASE"]

    engine = db.create_engine(
        f'postgresql://'+database['user']+":"+database['pass']+'@'+database['ip']+":"+database['port']+'/'+database['databaseName'])
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = db.MetaData()
    faces = db.Table(database['table'], metadata,
                     autoload=True, autoload_with=engine)
    logging.info("The Amount of Entrys that are in the Table are" + str(session.query(faces).count()))
    return session.query(faces).count()


def getKey(result_set, i):
    print(result_set[i])
    return result_set[i]


def getID(result_set, i):
    id, user, groub, image, imageurl, seen = result_set[i]
    return id

    # gets Database entry name


def getName(result_set, i):
    id, user, group, image, imageurl, seen = result_set[i]
    return user


def getStatus(result_set, i):
    id, user, group, image, imageurl, seen = result_set[i]
    return group


def getImageName(result_set, i):
    id, user, group, image, imageurl, seen = result_set[i]
    return image

    id, user, group, image, imageurl, seen = result_set[i]
    return image


def getImageUrI(result_set, i):
    id, user, group, image, imageurl, seen = result_set[i]
    return imageurl
