import sys
import os
sys.dont_write_bytecode = True
from flask_app import mysister
from flask_app.setup_logger import setup_logger
import threading
import queue
from multiprocessing import Process, Queue

class main:
    logger = setup_logger(__name__)

def run(queue00):
    """mysisterプロセスを実行する関数"""
    main.logger.info('mysister run!!')
    queue00.put(os.getpid())
    main.logger.info('mysister run!!')
    mysister.run()

def boot(thread1, queue01):
    """メインプロセスを起動する関数"""
    # ログ出力
    main.logger.info('thread1 start!!')

    # プロセス間通信用のキュー作成
    queue00 = Queue()
    
    # mysisterプロセスの作成と開始
    p1 = Process(target=run, args=(queue00,))
    p1.start()

    # プロセスIDを取得して返却
    return int(queue00.get())
