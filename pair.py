import json
from json import JSONEncoder

class pair:
    #Constructor:
    def __init__(self,symbol,type,target):
        #Declaring variables
        self.synbol = symbol
        self.type = type
        self.target = target
        
    #Getters
    def getSynbol(self):
        return self.synbol
    def getType(self):
        return self.type
    def getTarget(self):
        return self.target

class CEncoder(json.JSONEncoder):
    def default(self, o):
            return o.__dict__