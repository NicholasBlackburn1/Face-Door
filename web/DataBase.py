""" 
Creates, handles and removes data from the database for saving messages and total ammount of seen people
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# admin table stores all the user entered admins in 
admins = Table(
    "admins",
    Base.metadata,
    Column("admin_id", Integer, ForeignKey("admin.admin_id")),
    Column("first_name", String, ForeignKey("admin.first_name")),
    Column("last_name", String, ForeignKey("admin.last_name")),
)
# users table stores all users that dont have admin acess but that are still allowed in
users = Table(
    "users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.admin_id")),
    Column("first_name", String, ForeignKey("user.first_name")),
    Column("last_name", String, ForeignKey("user.last_name")),
)




# For referance admins are owners 
#TODO: Change all owner referancees to admin & add image storage
class admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    
    
    
# For referance admins are owners 
#TODO: Change all parents referancees to users
class user(Base):
    __tablename__ = "admin"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    
        

