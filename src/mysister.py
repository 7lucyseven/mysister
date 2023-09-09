import time
import os
import json
import random
import hashlib
import sys
import pathlib
import copy
import time
import importlib
import logging
import logging.handlers
from logging import getLogger
sys.dont_write_bytecode = True

import get_comment
import sister_ai
import sister_vocevox
import lucy_voice

from distutils.util import strtobool
sys.path.append("../config")
import conf
import dynamic_property


end_time = ''
ctr_time = 30
MAIN_INI_PATH = r"../config/main.ini"
print(MAIN_INI_PATH)
lucy_voice_text = conf.lucy_voice_text
CTR_CHAR = conf.CTR_CHAR
SMALL_TALK = conf.SMALL_TALK
dynamic_timestamp_text= conf.dynamic_timestamp_text
# commentを読み上げるときに最初につける相槌
l_responses = ['ふむふむ。','なになに。','よいしょ。']

LOG_FILE = conf.LOG_FILE
LOG_LEVEL = conf.LOG_LEVEL
# rh = logging.handlers.RotatingFileHandler(
#         LOG_FILE, 
#         encoding='utf-8',
#         maxBytes=100,
#         backupCount=10
#     )
# logger = logging.getLogger()
# # logger = logging.basicConfig(
# #     filename = LOG_FILE,  # ログファイルの名前
# #     level = logging.INFO,      # ログレベル (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# #     format='%(asctime)s - %(levelname)s - %(message)s'
# # )
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# #ファイルへ出力するハンドラーを定義
# fh = logging.FileHandler(filename = LOG_FILE, encoding='utf-8')
# fh.setLevel(logging.INFO)
# fh.setFormatter(formatter)
# #rootロガーにハンドラーを登録する
# logger.addHandler(fh)


# main関数
def main():
    logger = setup_logger(__name__)
    logger.info('main function boot!!')

    os.system('cls')
    logger.info('コンソール画面をクリアしました。')

    print("lucy communication : 1")
    print("comment communication : 2 or other number")
    mode_num = int(input("input mode number: "))
    num = int(input("input comment number: "))
    logger.info('モード情報の入力を受け取りました。')
    logger.info('今回のモードは [' + str(mode_num) + '] です')
    logger.info('今回のコメント読み込み開始地点は [' + str(num) + '] です')

    # 発言のタイムスタンプを取得して初期化
    lucy_timestamp = os.path.getmtime(lucy_voice_text)
    logger.info('ルーシーの発言テキストのタイムスタンプを取得しました。')

    dynamic_timestamp = os.path.getmtime(dynamic_timestamp_text)
    logger.info('「dynamic_property.py」のタイムスタンプを取得しました。')

    # わんコメが集積したcommentをすべて取得
    json = get_comment.init()
    l_data = get_comment.data(json)
    logger.info('すでにあるコメントをすべて取得しました。')

    logger.info('メインのループ処理に入ります。')
    while(1):
        tmp_timestamp = os.path.getmtime(dynamic_timestamp_text)
        if(dynamic_timestamp != tmp_timestamp):
            dynamic_timestamp = copy.copy(tmp_timestamp)
            importlib.reload(dynamic_property)
            mode_num = dynamic_property.mode_num
            logger.info('設定ファイルのタイムスタンプに変更があったため、新しく設定ファイルを読み込みました。')

        if(mode_num == 1):
            lucy_timestamp = lucy_communication(lucy_timestamp)
        elif(mode_num == 2):
            logger.info('モード[2]：コメントとの会話を開始します。')
            if( get_comment.is_new(l_data, num)):
                num = comment_communication(num)
            json = get_comment.init()
            l_data = get_comment.data(json)
        elif(mode_num == 3):
            lucy_timestamp = lucy_communication(lucy_timestamp)
            if( get_comment.is_new(l_data, num)):
                num = comment_communication(num)
            json = get_comment.init()
            l_data = get_comment.data(json)                
        elif(mode_num == 4):
            os.system('cls')
            sister_respons = sister_ai.respons("楽しい話題の雑談を行ってください")
            print("フォルトゥナちゃんからの雑談")
            print(sister_respons)
            save_history("auto", "雑談", sister_respons)
            sister_vocevox.speak('' + ';' + sister_respons)
        else:
            exit()


        time.sleep(0.1)

# ルーシーの発言を読み上げる
def lucy_communication(lucy_timestamp):
    logger = getLogger(__name__)
    if(lucy_voice.is_new(lucy_timestamp, lucy_voice_text)):
        logger.info('ルーシーテキストのタイムスタンプに変更がありました。ルーシーとの会話を開始します。')
        lucy_text = lucy_voice.get_voicetext()
        os.system('cls')
        print('--- るーしー ---')
        print(lucy_text)
        print(' ')
        sister_respons = sister_ai.respons(str(int(time.time()*1000)), 'lucy', lucy_text)
        print('--- フォルトゥナ ---')
        # print('--- お姉ちゃん ---')
        print(sister_respons)
        save_history("lucy", lucy_text, sister_respons)
        sister_vocevox.speak(' ' + ';' + sister_respons)
        lucy_timestamp = os.path.getmtime(lucy_voice_text)

    return lucy_timestamp

# num番号からcommentを最後まで読み上げる
def comment_communication(num):
    logger = getLogger(__name__)
    logger.info('[' + str(num) + '] 番目のコメントから会話を開始します。')
    json = get_comment.init()
    l_data = get_comment.data(json)
    for data in l_data[num:]:
        if(data[2][0] == CTR_CHAR):
            os.system('cls')
            timestamp = data[0]
            name = data[1]
            comment = data[2][1:]
            # print(data)
            print('コメント番号' + str(num) + ' : ', end="")
            print(comment)
            print(' ')
            sister_respons = sister_ai.respons(timestamp, name, comment)
            print('--- フォルトゥナ ---')
            print(sister_respons)
            save_history("user", comment, sister_respons)
            sister_vocevox.speak(random.choice(l_responses) + comment + ';' + sister_respons )
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

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even DEBUG messages
    fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    # create console handler with a INFO log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


if __name__=="__main__":
    main()
