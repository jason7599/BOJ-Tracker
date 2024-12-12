# deals with reading and writing data 

import os
import json

from common.trackerdata import TrackerData

TRACKER_DATA_PATH = "data/trackdata.json"

def get_tracker_data():
    if os.path.exists(TRACKER_DATA_PATH):
        with open(TRACKER_DATA_PATH, 'r') as f:
            return TrackerData.from_json(json.load(f))
    return TrackerData.empty()
    
def write_tracker_data(td: TrackerData):
    with open(TRACKER_DATA_PATH, 'w') as f:
        json.dump(td.to_json(), f, indent=4)
