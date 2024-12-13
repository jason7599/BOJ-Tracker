# deals with reading and writing data 

import os
import json

from common.appdata import AppData

APPDATA_PATH = "data/appdata.json"

def get_appdata():
    if os.path.exists(APPDATA_PATH):
        with open(APPDATA_PATH, 'r') as f:
            return AppData.from_json(json.load(f))
    return AppData.empty()
    
def write_appdata(td: AppData):
    with open(APPDATA_PATH, 'w') as f:
        json.dump(td.to_json(), f, indent=4)
