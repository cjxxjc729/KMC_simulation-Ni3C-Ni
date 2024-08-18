
import random
import numpy as np

import json
import glob

def build_event_dic():

    pattern = "event.*.json"

    fs_json=glob.glob(pattern)

    event_dic ={}
    for f_json in fs_json:

        with open(f_json, 'r', encoding='utf-8') as file:
            data = json.load(file)

        event_dic = {**event_dic, **data}

    return event_dic



if __name__=="__main__":

    event_dic = build_event_dic()
    
