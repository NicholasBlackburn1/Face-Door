
import pathlib
import sqlalchemy as db 
import sqlalchemy.dialects.sqlite
class Database(object):
    
    # Gets the Face Data from the Face data 
    def getFaces():
        print('sqlite://'+str(pathlib.Path().absolute())+'/web/db.sqlite3')
        engine = db.create_engine(f'sqlite:///'+str(pathlib.Path().absolute())+'/web/db.sqlite3')
        connection = engine.connect()
        metadata = db.MetaData()
        faces = db.Table('Face', metadata, autoload=True, autoload_with=engine)
        query = db.select([faces])
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        return(result_set)
    
    # get Keys from Database and sort them to Data 
    def getKey(result_set, i):
        print(result_set[i])
        return result_set[i]
    