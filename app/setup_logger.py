import logging
import logging.handlers
from logging import getLogger
import sys
from distutils.util import strtobool
sys.path.append("../config")
import conf

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # DEBUGメッセージのFileHandlerを作成する
    fh = logging.FileHandler(conf.LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    # INFOのLOGLEVELでConsolemHandlerを作成する
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    # loggerにハンドラーをaddする
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger