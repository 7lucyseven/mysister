from flask_app.setup_logger import setup_logger
from flask_app import get_comment
from flask_app import sister_vocevox
from flask_app import sister_ai
import random
import sys
from distutils.util import strtobool
sys.path.append("../config")
import conf
import os

# num番号からcommentを最後まで読み上げる
def comment_communication(num):
    logger = setup_logger(__name__)
    logger.info('[' + str(num) + '] 番目のコメントから会話を開始します。')
    json = get_comment.init()
    l_data = get_comment.data(json)
    logger.info('コメントファイルを読み込みました。')
    for data in l_data[num:]:
        if(data[2][0] == conf.CTR_CHAR):
            logger.info('コメントの先頭に [' + conf.CTR_CHAR + '] を確認しました。')
            #os.system('cls')    
            timestamp = data[0]
            name = data[1]
            comment = data[2][1:]
            # print(data)
            print('コメント番号' + str(num) + ' : ', end="")
            print(comment)
            logger.debug('コメント出力')
            print(' ')
            sister_respons = sister_ai.respons(timestamp, name, comment)
            print('--- フォルトゥナ ---')
            print(sister_respons)
            sister_vocevox.speak(random.choice(conf.l_responses) + comment + ';' + sister_respons )
            num = num + 1
        else:
            num = num + 1
    return num