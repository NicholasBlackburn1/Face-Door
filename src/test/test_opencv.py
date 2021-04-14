

import uuid
import prosessing.Database as db
import prosessing.dataclass as data


user_Array=[]
 #Encodes all the Nessiscary User info into Json String so it can be easly moved arroun
i = 0

while True:
    # example Json string  [{"uuid":"Tesla", "name":2, "status":"New York",image:none, url:}]
    print(str("Data index ")+str(i))

                # this is Where the Data gets Wrapped into am DataList with uuid First key
    local_data = {
                    uuid.uuid1(db.getUserUUID(db.getFaces(),i)):data.UserData(db.getName(db.getFaces(),i),db.getStatus(db.getFaces(),i),db.getImageName(db.getFaces(),i),db.getImageUrl(db.getFaces(),i))
                }

    user_Array.extend(local_data)
    print(user_Array[db.getUserUUID(db.getFaces(),i)])
                
    i += 1

    # Checks to see if i == the database amount hehe
    if(i == db.getAmountOfEntrys()):
        print(db.getAmountOfEntrys())
        break
