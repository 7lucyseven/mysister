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

    def __init__(self):
        self.num = 0
        self.observer = None
        self.observer_02 = None

    def on_modified(self, event):
        """lucy_text.txtの監視処理"""
        filepath = event.src_path
        filename = os.path.basename(filepath)
        self.logger.info('%s changed' % filename)
        lucy_communication()

    def on_modified_02(self, event):
        """設定ファイルの監視処理"""
        filepath = event.src_path
        filename = os.path.basename(filepath)
        self.logger.info('%s changed' % filename)

        self.config.read("dynamic_property.ini")
        status = self.config["BASE"]["status"]
        self.logger.info('status is ' + status)

        if(status == "stop"):
            self.logger.info('stop')
            sys.exit()

        self.logger.info('設定ファイルのタイムスタンプに変更があったため、新しく設定ファイルを読み込みました。')

    def run(self):
        """メイン実行処理"""
        self.logger.info('コンソール画面をクリアしました。')
        self.logger.info('今回のコメント読み込み開始地点は [' + str(self.num) + '] です')

        # lucy_text.txtの監視設定
        self._setup_lucy_observer()
        self.logger.info('lucy_text.txtの監視開始')

        # 設定ファイルの監視設定  
        self._setup_config_observer()
        self.logger.info('設定ファイルの監視開始')

        mode_num = int(self.config["BASE"]["mode_num"])
        self.logger.info('設定ファイルの初回読み込み完了')

        # コメントデータの初期取得
        json = get_comment.init()
        l_data = get_comment.data(json)
        self.logger.info('すでにあるコメントをすべて取得しました。')
        
        self.logger.info('メインのループ処理に入ります。')

        try:
            while True:
                if mode_num == 1:
                    continue
                elif mode_num == 2:
                    self._handle_mode2(l_data)
                    json = get_comment.init()
                    l_data = get_comment.data(json)
                elif mode_num == 3:
                    self._handle_mode3(l_data) 
                    json = get_comment.init()
                    l_data = get_comment.data(json)
                elif mode_num == 4:
                    self._handle_mode4()
                else:
                    self.logger.info('exit')
                    exit()
                time.sleep(1)

        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()

    def _setup_lucy_observer(self):
        """lucy_text.txt監視の設定"""
        DIR_WATCH = conf.Config.lucy_voice_dir
        PATTERNS = ['*.txt']
        event_handler = PatternMatchingEventHandler(patterns=PATTERNS)
        event_handler.on_modified = self.on_modified
        self.observer = Observer()
        self.observer.schedule(event_handler, DIR_WATCH, recursive=True)
        self.observer.start()

    def _setup_config_observer(self):
        """設定ファイル監視の設定"""
        DIR_WATCH = './'
        PATTERNS = ['*.ini']
        event_handler_02 = PatternMatchingEventHandler(patterns=PATTERNS)
        event_handler_02.on_modified = self.on_modified_02
        self.observer_02 = Observer()
        self.observer_02.schedule(event_handler_02, DIR_WATCH, recursive=True)
        self.observer_02.start()

    def _handle_mode2(self, l_data):
        """モード2の処理"""
        self.logger.info('モード[2]：コメントとの会話を開始します。')
        if get_comment.is_new(l_data, self.num):
            self.num = comment_communication(self.num)

    def _handle_mode3(self, l_data):
        """モード3の処理"""
        print("while(3):")
        lucy_communication()
        if get_comment.is_new(l_data, self.num):
            self.logger.info('モード[3]：新規コメントがありました。')
            self.num = comment_communication(self.num)

    def _handle_mode4(self):
        """モード4の処理"""
        os.system('cls')
        sister_respons = sister_ai.respons("楽しい話題の雑談を行ってください")
        print("フォルトゥナちゃんからの雑談")
        print(sister_respons)
        sister_vocevox.speak('' + ';' + sister_respons)