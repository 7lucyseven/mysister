import time
import os
import sys
import copy

import importlib
sys.dont_write_bytecode = True

from flask_app import get_comment
from flask_app import sister_ai
from flask_app import sister_vocevox
sys.path.append("../config")
import conf
from flask_app.setup_logger import setup_logger
from flask_app.lucy_communication import lucy_communication 
from flask_app.comment_communication import comment_communication

from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler

import configparser

class mysister:
    logger = setup_logger(__name__)
    config = configparser.ConfigParser()
    config.read("dynamic_property.ini")


# 監視通知のメイン処理
def on_modified(event):
    filepath = event.src_path
    filename = os.path.basename(filepath)
    print('%s changed' % filename)
    lucy_communication()

# 監視通知のメイン処理
def on_modified_02(event):
    filepath = event.src_path
    filename = os.path.basename(filepath)
    print('%s changed' % filename)

    mysister.config.read("dynamic_property.ini")
    status = mysister.config["BASE"]["status"]
    print('status' + status)

    if(status == "stop"):
        mysister.logger.info('stop')
        sys.exit()

    mysister.logger.info('設定ファイルのタイムスタンプに変更があったため、新しく設定ファイルを読み込みました。')

def run():
    num = 0
    mysister.logger.info('コンソール画面をクリアしました。')
    mysister.logger.info('今回のコメント読み込み開始地点は [' + str(num) + '] です')

    # lucy_text.txtを監視するための処理
    DIR_WATCH = conf.lucy_voice_dir
    PATTERNS = ['*.txt']

    event_handler = PatternMatchingEventHandler(PATTERNS)
    event_handler.on_modified = on_modified

    observer = Observer()
    observer.schedule(event_handler, DIR_WATCH, recursive=True)
    observer.start()
    print("監視1開始")

    # configディレクトリの拡張しpyの設定ファイルを監視するための処理
    #DIR_WATCH = '../config'
    DIR_WATCH = './'
    PATTERNS = ['*.ini']

    event_handler_02 = PatternMatchingEventHandler(PATTERNS)
    event_handler_02.on_modified = on_modified_02

    observer_02 = Observer()
    observer_02.schedule(event_handler_02, DIR_WATCH, recursive=True)
    observer_02.start()
    print("監視2開始")

    mode_num = int(mysister.config["BASE"]["mode_num"])
    mysister.logger.info('設定ファイルのタイムスタンプに変更があったため、新しく設定ファイルを読み込みました。')

    # わんコメが集積したcommentをすべて取得
    json = get_comment.init()
    l_data = get_comment.data(json)
    mysister.logger.info('すでにあるコメントをすべて取得しました。')
    
    mysister.logger.info('メインのループ処理に入ります。')

    try:
        while(1):
            if(mode_num == 1):
                continue

            elif(mode_num == 2):
                #print("while(2):")
                mysister.logger.info('モード[2]：コメントとの会話を開始します。')
                if( get_comment.is_new(l_data, num)):
                    num = comment_communication(num)
                json = get_comment.init()
                l_data = get_comment.data(json)
            elif(mode_num == 3):
                print("while(3):")
                lucy_communication()
                if( get_comment.is_new(l_data, num)):
                    mysister.logger.info('モード[3]：新規コメントがありました。')
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
                mysister.logger.info('exit')
                exit()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()