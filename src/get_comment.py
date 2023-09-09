import json
import logging

def init():
    while(1):
        try:
            json_open = open('C:/Users/Creator/AppData/Roaming/live-comment-viewer/comment.json', 'r', encoding="utf-8")
            json_load = json.load(json_open)
            break
        except Exception as e:
            # print(e)
            continue

    return json_load

def data(json_load):
    l_data = []
    for i in json_load['comments']:
        l_tmp = []
        l_tmp.append(i['data']['timestamp'])
        l_tmp.append(i['data']['name'])
        l_tmp.append(i['data']['comment'])
        l_data.append(l_tmp)

    return l_data 

def is_new(l_data, num):
    if(len(l_data) == num):
        return False
    else:
        return True