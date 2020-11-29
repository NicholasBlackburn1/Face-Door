
import pathlib
import sqlalchemy as db 
class Database(object):
    
    # Gets the Face Data from the Face data 
    def getFaces():
        print('sqlite://'+str(pathlib.Path().absolute())+'/web/db.sqlite3')
        engine = db.create_engine(f'sqllite:///'+str(pathlib.Path().absolute())+'/web/db.sqlite3')
        connection = engine.connect()
        metadata = db.MetaData()
        faces = db.Table('Face', metadata, autoload=True, autoload_with=engine)
        query = db.select([faces])
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        return(result_set)