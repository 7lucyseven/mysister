import sys
import os
sys.dont_write_bytecode = True
import mysister
from setup_logger import setup_logger
import threading
import queue
from multiprocessing import Process, Queue

class main:
    logger = setup_logger(__name__)



def run(queue00):
    main.logger.info('mysister run!!')
    queue00.put(os.getpid())
    main.logger.info('mysister run!!')
    mysister.run()

# main関数
def boot(thread1, queue01):
    # ログ出力処理
    # スレッドを作る
    

    # スレッドの処理を開始
    main.logger.info('thread1 start!!')

    queue00 = Queue()
    
    #thread1 = threading.Thread(target=run, args=(queue01,queue01,),daemon = True)
    p1 = Process(target=run, args=(queue00, ))
    #p2 = Process(target=wrapper, args=("test",))
    print("queue01.get()")
    #print(queue01.get())
    p1.start()
    #p1.start()
    #print("queue01.get()")
    #print(queue01.get())
    

    return int(queue00.get())
    

    #print("start")
