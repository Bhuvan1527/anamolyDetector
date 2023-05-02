from pymongo import MongoClient
class DBConnection:
    def __init__(self) -> None:
        self.connetionString = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0"
        self.database = MongoClient(self.connetionString)['practice']
        self.collection = self.database['users']
        self.collection2 = self.database['results']

    def insert(self, email, usrname, passw):
        self.collection.insert_one({"email":email, "username":usrname,"password":passw})
        print("Successful")
        return
    
    def isThere(self, email, usrname) -> int :
        if self.collection.count_documents({"email":email}, limit=1) == 1:
            return 1
        elif self.collection.count_documents({"name":usrname}, limit=1) == 1:
            return 2
        else :
            return 0
    
    def Authenticate(self, usr, passw) -> bool:
        if self.collection.count_documents({"username":usr, "password":passw}) == 1:
            return True
        else:
            return False
        
    def getResultItems(self, usr)    -> dict:
        # for x in self.collection2.find({"username":usr}):
        #     print(f"The username is {x['_id']}, and anomaly is {x['Anomalies_Detected']}")
        # print(self.collection2.find())
        return self.collection2.find({"username":usr})
    
    def insertResults(self, doc):
        self.collection2.insert_one(doc)
    
    def getResultItemOnId(self, usr, id)    -> dict:
        # for x in self.collection2.find({"username":usr}):
        #     print(f"The username is {x['_id']}, and anomaly is {x['Anomalies_Detected']}")
        # print(self.collection2.find())
        return self.collection2.find({"username":usr, "_id":id})
