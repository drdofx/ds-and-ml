import json

class Store:
    def __init__(self):
        pass

    def storeJson(self, data, filename):
        try:
            # save to json file in this directory
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)

            return True
        except Exception as e:
            return False
        
    def checkFileExists(self, filename):
        try:
            # open file
            with open(filename, 'r'):
                return True
        except Exception as e:
            return False