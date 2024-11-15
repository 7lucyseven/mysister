import logging
import conf

def setup_logger(name):
    '''ロガーを取得'''
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    '''設定を取得'''
    config = conf.Config()

    '''ファイルハンドラーを作成 (DEBUGレベル)'''
    fh = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
    fh.setLevel(getattr(logging, config.LOG_LEVEL, logging.DEBUG))
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    '''コンソールハンドラーを作成 (INFOレベル)'''
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    '''ハンドラーをロガーに追加'''
    logger.addHandler(fh)
    logger.addHandler(ch)

    '''初期メッセージをログに記録'''
    logger.debug("Logger has been set up successfully.")

    return logger