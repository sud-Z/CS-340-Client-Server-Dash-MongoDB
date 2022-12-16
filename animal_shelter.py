from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # init to connect with no auth
        # self.client = MongoClient('mongodb://localhost:48067')
        # init to connect with auth
        self.client = MongoClient('mongodb://%s:%s@localhost:48067/?authMechanism=DEFAULT&authSource=admin' % (username, password))
        
        # self.database = self.client['project']
        self.database = self.client['AAC']

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert(data)  # data should be dictionary
            return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Create method to implement the R in CRUD.
    def read_all(self, data):
        if data is not None:
            cursor = self.database.animals.find(data, {"_id" : False})
            
            # return a cursor with a pointer to a list of documents
        
            return cursor
        else:
            raise Exception("Nothing to find, because data parameter is empty")
    
    
    def read_one(self, data):
        if data is not None:
            # return single document as python dictionary
            return self.database.animals.find_one(data)
        else:
            raise Exception("Nothing to find, because data parameter is empty")
            
# Create method to implement the U in CRUD
    def update_many(self, data, dataUpdate):
        if data is not None and dataUpdate is not None:
            # Get result from mongo and return
            result = self.database.animals.update_many(data, dataUpdate)
            result = result.raw_result
            if result['nModified'] == 0:
                return "Update not Successful"
            else:
                return result
        else:
            raise Exception("Nothing to update, because data parameter is empty")
            
# Create method to implement the D in CRUD
    def delete_many(self, data):
        if data is not None:
            result = self.database.animals.delete_many(data)
            result = result.raw_result
            if result['n'] == 0:
                return "Delete not Successful"
            else:
                return result
        else:
            raise Exception("Nothing to delete, because data parameter is empty")
            