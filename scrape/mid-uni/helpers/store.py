import json

class Store:
    def __init__(self):
        pass

    def storeJson(self, data, filename):
        # save to json file in this directory
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)