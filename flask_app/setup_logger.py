import logging
import logging.handlers
from logging import getLogger
import sys
from distutils.util import strtobool
import importlib
sys.path.append("../config")
import conf
importlib.reload(conf)

def setup_logger(name):
    # ロガーを取得
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ファイルハンドラーを作成 (DEBUGレベル)
    config = conf.Config()
    fh = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
    fh.setLevel(getattr(logging, config.LOG_LEVEL))
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    # コンソールハンドラーを作成 (INFOレベル) 
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    # ハンドラーをロガーに追加
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger