
import pathlib
import sqlalchemy as db 
import sqlalchemy.dialects.sqlite
class Database(object):
    
    # Gets the Face Data from the Face data 
    def getFaces():
      
        engine = db.create_engine(f'postgresql://test:pass@0.0.0.0:5432/face')
        connection = engine.connect()
        metadata = db.MetaData()
        faces = db.Table('Face', metadata, autoload=True, autoload_with=engine)
        print(faces)
        query = db.select([faces])
        print(query)
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        print(result_set)
        return(result_set)
    
    # get Keys from Database and sort them to Data 
    def getKey(result_set, i):
        print(result_set[i])
        return result_set[i]
    
    
    def getID(result_set,i):
        id,user,groub,image = result_set[i]
        return id
    
        # gets Database entry name
    def getName(result_set,i):
        id, user,group,image = result_set[i]
        return user

    def getStatus(result_set,i):
        id, user,group,image = result_set[i]
        return group

    def getImage(result_set,i):
        id, user,group,image = result_set[i]
        return image


    