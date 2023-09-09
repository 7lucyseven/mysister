import sys
sys.dont_write_bytecode = True
import mysister
from setup_logger import setup_logger

# main関数
def main():
    # ログ出力処理
    logger = setup_logger(__name__)
    logger.info('main function boot!!')

    # メイン処理実行
    logger.info('mysister.run()')
    mysister.run()

if __name__=="__main__":
    main()
