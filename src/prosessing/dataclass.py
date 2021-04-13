"""
This class is for the custom data Classes for Handling user data 
usu
TODO: make data Store persistat
"""

from dataclasses import dataclass
import uuid


# This Data class is for Handling UserData and allowing Programsers to use all the User data  UwU
@dataclass
class UserData:
    UserId : uuid.UUID
    Name : str
    Status: str
    Image : str
    Url : str