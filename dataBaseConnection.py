from pymongo import MongoClient
class DBConnection:
    def __init__(self) -> None:
        self.connetionString = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0"
        self.database = MongoClient(self.connetionString)['practice']
        self.collection = self.database['users']

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