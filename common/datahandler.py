import json

from common.trackerdata import TrackerData

TRACKER_DATA_PATH = "data/trackdata.json"

# TODO: FileNotFoundException
def load_tracker_data() -> TrackerData:
    with open(TRACKER_DATA_PATH, 'r') as f:
        return TrackerData.from_json(json.load(f))
    
def write_tracker_data(td: TrackerData):
    with open(TRACKER_DATA_PATH, 'w') as f:
        json.dump(td.to_json(), f, indent=4)