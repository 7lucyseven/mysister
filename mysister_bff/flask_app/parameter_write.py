from flask_app import sound_device
import sys
sys.dont_write_bytecode = True
from flask_app.setup_logger import setup_logger
sys.path.append("../config")
import configparser
import platform
import os
if platform.system() != 'Windows':
    import fcntl
else:
    import msvcrt
    import portalocker

class parameter_write:
    def __init__(self):
        self.config = configparser.ConfigParser(comment_prefixes='#', allow_no_value=True)
        self.config.read("./flask_app/dynamic_property.ini", encoding="utf-8")
        self.logger = setup_logger(__name__)
        self.logger.info("parameter write init")

    def service(self, request):
        try:
            self.config = configparser.ConfigParser(comment_prefixes='#', allow_no_value=True)
            # ファイルオープンする
            with open("./flask_app/dynamic_property.ini", "r+", encoding="utf-8") as f:
                if platform.system() != 'Windows':
                    # ロック
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    # 読み込み
                    f.seek(0, os.SEEK_SET)
                    self.config.read_file(f)
                    # 読み込んだ設定値の修正
                    parameter = request.form.to_dict()
                    print(self.config.sections())
                    self.config["BASE"]["mode_num"] = parameter["mode"]
                    self.config["BASE"]["device"]   = parameter["device"]
                    self.config["BASE"]["status"]   = "start"
                    try:
                        f.seek(0, os.SEEK_SET)
                        self.config.write(f)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                else:
                    portalocker.lock(f, portalocker.LOCK_EX)
                    try:
                        self.config.write(f)
                    finally:
                        portalocker.unlock(f)
            # ロックする
            # 読みこむ
            # 修正する
            # 書き込む
            # ロック解除





        except (IOError, OSError) as e:
            self.logger.error(f"設定ファイルの書き込みに失敗しました: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"予期せぬエラーが発生しました: {str(e)}")
            raise


