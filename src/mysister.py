import time
import os
import json
import random
import hashlib
import sys
import pathlib
sys.dont_write_bytecode = True

import get_comment
import syster_ai
import sister_vocevox
import lucy_voice

from distutils.util import strtobool
sys.path.append("../config")
import conf

end_time = ''
ctr_time = 30
MAIN_INI_PATH = r"../config/main.ini"
print(MAIN_INI_PATH)
lucy_voice_text = conf.lucy_voice_text
CTR_CHAR = conf.CTR_CHAR
SMALL_TALK = conf.SMALL_TALK
# commentを読み上げるときに最初につける相槌
l_responses = ['ふむふむ。','なになに。','よいしょ。']

# main関数
def main():
    os.system('cls')
    num = int(input("input comment number: "))
    # 発言のタイムスタンプを取得して初期化
    lucy_timestamp = os.path.getmtime(lucy_voice_text)

    # わんコメが集積したcommentをすべて取得
    json = get_comment.init()
    l_data = get_comment.data(json)
    
    end_time = time.time()
    
    # 読み上げ処理を開始
    while(1):
        if( get_comment.is_new(l_data, num)):
            #print('--- communication Start---')
            num = comment_communication(num)
            lucy_timestamp = lucy_communication(lucy_timestamp)
            #print('--- communication End---')
            end_time = time.time()
        else:
            time.sleep(1)
        t = time.time() - end_time
        if(t > ctr_time and SMALL_TALK):
            os.system('cls')
            sister_respons = syster_ai.respons("楽しい話題の雑談を行ってください")
            print("フォルトゥナちゃんからの雑談")
            print(sister_respons)
            save_history("auto", "雑談", sister_respons)
            sister_vocevox.speak('' + ';' + sister_respons)

            end_time = time.time()
        json = get_comment.init()
        l_data = get_comment.data(json)


# ルーシーの発言を読み上げる
def lucy_communication(lucy_timestamp):
    if(lucy_voice.is_new(lucy_timestamp, lucy_voice_text)):
        lucy_text = lucy_voice.get_voicetext()
        os.system('cls')
        print('るーしー')
        print(lucy_text)
        sister_respons = syster_ai.respons(lucy_text)
        print(sister_respons)
        save_history("lucy", lucy_text, sister_respons)
        sister_vocevox.speak(' ' + ';' + sister_respons)
        lucy_timestamp = os.path.getmtime(lucy_voice_text)

    return lucy_timestamp

# num番号からcommentを最後まで読み上げる
def comment_communication(num):
    json = get_comment.init()
    l_data = get_comment.data(json)
    for data in l_data[num:]:
        if(data[2][0] == CTR_CHAR):
            os.system('cls')
            comment = data[2][1:]
            print('コメント番号' + str(num) + ' : ', end="")
            print(comment)
            print('')
            sister_respons = syster_ai.respons(comment)
            print(sister_respons)
            save_history("user", comment, sister_respons)
            sister_vocevox.speak(random.choice(l_responses) + comment + ';' + sister_respons )
            print('-----------------------------------------------')
            num = num + 1
        else:
            #print(num)
            #print('Skip')
            num = num + 1
    return num

def save_history(user, comment, sister_respons):
    dict_tmp = {
        "user": user,
        "comment": comment,
        "sister_respons": sister_respons,
    }

    path = './history.json'

    # # jsonファイルを読み込み
    # with open(path, 'r', encoding='utf-8') as f:
    #     read_data = json.load(f)

    # # jsonに追記
    # save_data = [read_data, dict_tmp]

    # jsonを保存
    with open(path, mode="ab+") as f:
        f.seek(-1,2)
        f.truncate()
        f.write(', '.encode())
        f.write(json.dumps(dict_tmp, ensure_ascii=False).encode()[1:-1])
        f.write(']'.encode())


        #json.dump(save_data, json_history, indent=4)

if __name__=="__main__":
    main()
