import os
import sys
sys.path.append("../config")
import conf



# 引数は2つ。AI or user と 会話text。
def save_talk(role , timestamp, userID, talk_text):

    file_path = './tmp/' + role + '_' +userID + '.txt'
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write('\n' + timestamp + ';' + talk_text.replace('\n', ''))


def load_talk(role, userID):

    file_path = '../tmp/' + role + '_' +userID + '.txt'
    l_talk_text = []
    with open(file_path, 'r', encoding='utf-8') as f:
        l_f = f.readlines()
        # print(l_f)
        for i in l_f[1:]:
            talk_text = i.split(';')
            talk_text.insert(0, role)
            l_talk_text.append(talk_text)
    # print(l_talk_text)

    return l_talk_text

def is_true(role, userID):
    file_path = '../tmp/' + role + '_' +userID + '.txt'
    is_file = os.path.isfile(file_path)
    return is_file