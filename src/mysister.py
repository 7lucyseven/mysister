import time
import os
import json
import random
import hashlib
import sys
sys.dont_write_bytecode = True

import get_comment
import syster_ai
import sister_vocevox
import lucy_voice

# 文字起こしを行ったルーシーの発言
lucy_voice_text = 'C:\\Users\\Creator\\Desktop\\mysister\\lucy_voice\\lucy_text.txt'
# commentを読み上げるときに最初につける相槌
l_responses = ['ふむふむ。','なになに。','よいしょ。']
# 読み上げるcommentの制御文字
CTR_CHAR = '#'

end_time = ''
ctr_time = 30

# main関数
def main():
    os.system('cls')
    # 発言のハッシュ値を取得して初期化
    lucy_hash = ''
    with open(lucy_voice_text, 'rb') as f:
        filedata = f.read()
        lucy_hash = hashlib.md5(filedata).hexdigest()

    # わんコメが集積したcommentをすべて取得
    json = get_comment.init()
    l_data = get_comment.data(json)
    
    # comment読み上げスタートする番号
    num = 172

    end_time = time.time()
    
    # 読み上げ処理を開始
    while(1):
        if( get_comment.is_new(l_data, num) ):
            #print('--- communication Start---')
            num = comment_communication(num)
            lucy_hash = lucy_communication(lucy_hash)
            #print('--- communication End---')
            end_time = time.time()
        else:
            time.sleep(1)
        t = time.time() - end_time
        if(t > ctr_time):
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
def lucy_communication(lucy_hash):
    if(lucy_voice.is_new(lucy_hash)):
        lucy_text = lucy_voice.get_voicetext()
        os.system('cls')
        print('るーしー')
        print(lucy_text)
        sister_respons = syster_ai.respons(lucy_text)
        print(sister_respons)
        save_history("lucy", lucy_text, sister_respons)
        sister_vocevox.speak(random.choice(l_responses) + lucy_text + ';' + sister_respons)
        with open(lucy_voice_text, 'rb') as f:
            filedata = f.read()
            lucy_hash = hashlib.md5(filedata).hexdigest()
    return lucy_hash

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
