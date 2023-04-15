import pathlib
import os
import sys
sys.path.append("../config")
import conf

def is_new(lucy_timestamp, lucy_voice_text):
    new_timestamp = os.path.getmtime(lucy_voice_text)
    if(lucy_timestamp == new_timestamp):
        return False
    else:
        return True

def get_voicetext():
    lucy_text = conf.lucy_voice_text
    with open(lucy_text, 'r', encoding='UTF-8') as f:
        datalist = f.readlines()
        return datalist[0]
    