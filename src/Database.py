
import pathlib
import sqlalchemy as db 
import sqlalchemy.dialects.sqlite
from configparser import ConfigParser
class Database(object):
    
    # Gets the Face Data from the Face data 
    def getFaces():
         #Read config.ini file
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute())+"/"+"Config.ini")

        #Get the password   
        database = config_object["DATABASE"]
      
        engine = db.create_engine(f'postgresql://'+database['user']+":"+database['pass']+'@'+database['ip']+":"+database['port']+'/'+database['databaseName'])
        connection = engine.connect()
        metadata = db.MetaData()
        faces = db.Table(database['table'], metadata, autoload=True, autoload_with=engine)
        print(faces)
        query = db.select([faces])
        print(query)
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        print(result_set)
        return(result_set)
    
    # get Keys from Database and sort them to Data 
    def getKey(self,result_set, i):
        print(result_set[i])
        return result_set[i]
    
    
    def getID(self,result_set,i):
        id,user,groub,image,imageurl,seen = result_set[i]
        return id
    
        # gets Database entry name
    def getName(self,result_set,i):
        id, user,group,image,imageurl,seen = result_set[i]
        return user

    def getStatus(self,result_set,i):
        id, user,group,image,imageurl,seen = result_set[i]
        return group

    def getImageName(self,result_set,i):
        id, user,group,image,imageurl,seen = result_set[i]
        return image
