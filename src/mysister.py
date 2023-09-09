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
from setup_logger import setup_logger
from lucy_communication import lucy_communication
from comment_communication import comment_communication

end_time = ''
ctr_time = 30
MAIN_INI_PATH = r"../config/main.ini"
print(MAIN_INI_PATH)
lucy_voice_text = conf.lucy_voice_text
CTR_CHAR = conf.CTR_CHAR
SMALL_TALK = conf.SMALL_TALK
dynamic_timestamp_text= conf.dynamic_timestamp_text

LOG_FILE = conf.LOG_FILE
LOG_LEVEL = conf.LOG_LEVEL

def run():
    os.system('cls')
    logger = setup_logger(__name__)
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
                logger.info('モード[3]：新規コメントがありました。')
                num = comment_communication(num)
            json = get_comment.init()
            l_data = get_comment.data(json)                
        elif(mode_num == 4):
            os.system('cls')
            sister_respons = sister_ai.respons("楽しい話題の雑談を行ってください")
            print("フォルトゥナちゃんからの雑談")
            print(sister_respons)
            sister_vocevox.speak('' + ';' + sister_respons)
        else:
            exit()


        time.sleep(1)