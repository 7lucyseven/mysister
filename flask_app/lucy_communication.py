from setup_logger import setup_logger
import get_comment
import sister_vocevox
import sister_ai
import random
import lucy_voice
import sys
from distutils.util import strtobool
sys.path.append("../config")
import conf
import os
import time

# ルーシーの発言を読み上げる
def lucy_communication():
    logger = setup_logger(__name__)

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
    sister_vocevox.speak(' ' + ';' + sister_respons)

