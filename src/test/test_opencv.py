

import uuid
useruuidIndex=[]
publicList={}
i=0
while True:
    test= uuid.uuid1()
    publicArray= {
       test:"UWU",
       test:"Nope"
    }
    useruuidIndex.extend(str(test))
    print(test)
    i+=1
    
    print("\n")
    print("\n")
    print("\n")
    print("\n")
    if(i == 10):
        print(publicList.fromkeys((useruuidIndex[0])))
        print("Uwu array list is")
        break