import json
import logging
import requests

def init():
    while(1):
        try:
            #json_open = open('C:/Users/Creator/AppData/Roaming/live-comment-viewer/comment.json', 'r', encoding="utf-8")
            #json_load = json.load(json_open)
            json_load = requests.get('http://localhost:11180/api/comments')
            break
        except Exception as e:
            # print(e)
            continue

    return json_load.json()

def data(json_load):
    #comments = [entry['data']['comment'] for entry in json_load]
    #print('##TEST')
    #print(comments)
    #print('##TEST')
    l_data = []
    #for i in json_load['comments']:
    for i in json_load:
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