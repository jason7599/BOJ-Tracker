# shared global vars..
import os
import json

from common.trackerdata import TrackerData

TRACKER_DATA_PATH = "data/trackdata.json"

class DataStore:
    _tracker_data: TrackerData = None

    @classmethod
    def tracker_data(cls):
        return cls._tracker_data

    @classmethod
    def initialize(cls):
        cls._init_tracker_data()
    
    @classmethod
    def finalize(cls):
        cls._write_tracker_data()
    
    @classmethod
    def _init_tracker_data(cls):
        if os.path.exists(TRACKER_DATA_PATH):
            with open(TRACKER_DATA_PATH, 'r') as f:
                cls._tracker_data = TrackerData.from_json(json.load(f))
        else: 
            cls._tracker_data = TrackerData.empty()
        
    @classmethod
    def _write_tracker_data(cls):
        with open(TRACKER_DATA_PATH, 'w') as f:
            json.dump(cls._tracker_data.to_json(), f, indent=4)
