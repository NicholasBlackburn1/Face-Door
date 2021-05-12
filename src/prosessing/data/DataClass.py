"""
this class is for handling the User data 
"""

import dataclasses


@dataclasses.dataclass
class UserData():
    user: str
    status: str
    image: str
    downloadUrl: str
    phoneNum: str