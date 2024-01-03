import time
import os
import sys
import copy
import time
import importlib
sys.dont_write_bytecode = True

import get_comment
import sister_ai
import sister_vocevox
sys.path.append("../config")
import conf
import dynamic_property
from setup_logger import setup_logger
from lucy_communication import lucy_communication
from comment_communication import comment_communication

import watchdog
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler

# 監視通知のメイン処理
def on_modified(event):
    filepath = event.src_path
    filename = os.path.basename(filepath)
    print('%s changed' % filename)

    # 
    lucy_communication()

# 監視通知のメイン処理
def on_modified_02(event):
    filepath = event.src_path
    filename = os.path.basename(filepath)
    print('%s changed' % filename)

    # 
    importlib.reload(dynamic_property)
    logger = setup_logger(__name__)
    logger.info('設定ファイルのタイムスタンプに変更があったため、新しく設定ファイルを読み込みました。')
    print("test")

def run(mode_num):
    #os.system('cls')
    logger = setup_logger(__name__)
    logger.info('コンソール画面をクリアしました。')
    #num = int(input("input comment number: "))
    num = 0
    logger.info('今回のコメント読み込み開始地点は [' + str(num) + '] です')

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
    DIR_WATCH = '../config'
    PATTERNS = ['*.py']

    event_handler_02 = PatternMatchingEventHandler(PATTERNS)
    event_handler_02.on_modified = on_modified_02

    observer_02 = Observer()
    observer_02.schedule(event_handler_02, DIR_WATCH, recursive=True)
    observer_02.start()
    print("監視2開始")

    importlib.reload(dynamic_property)
    mode_num = dynamic_property.mode_num
    logger.info('設定ファイルのタイムスタンプに変更があったため、新しく設定ファイルを読み込みました。')

    # わんコメが集積したcommentをすべて取得
    json = get_comment.init()
    l_data = get_comment.data(json)
    logger.info('すでにあるコメントをすべて取得しました。')

    
    logger.info('メインのループ処理に入ります。')

    try:
        while(1):
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
    except KeyboardInterrupt:
        observer.stop()

    observer.join()