from flask import Flask, render_template, request, jsonify, Blueprint
from flask_app import sound_device
from flask_app import main
from flask_app import parameter_write
from flask_app.setup_logger import setup_logger
import sys
sys.path.append("../")
sys.dont_write_bytecode = True
import mysister
import threading
import configparser
import queue
from multiprocessing import Process
import psutil

app = Blueprint('main', __name__)
logger = setup_logger(__name__)

class MainFlask:
    def __init__(self):
        logger.info('MainFlaskの初期化処理')
        self.l_device = sound_device.get_device_list()
        self.thread1 = None
        self.config = self.load_config()
        self.queue01 = queue.Queue()
        self.pid = -1

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('./flask_app/dynamic_property.ini')
        return config

main_flask = MainFlask()

@app.route("/")
def index():
    """起動時に実行される最初の処理"""
    return render_template("index.html")

@app.route("/start", methods=["GET"])
def start_get():
    logger.info('Start処理開始')
    try:
        main_flask.queue01.put(1)
        main_flask.pid = main.boot(main_flask.thread1, main_flask.queue01)
        return render_template("index.html")
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/parameter", methods=["POST"])
def parameter_post():
    try:
        writer = parameter_write.parameter_write()
        writer.service(request)
        return render_template("parameter.html", l_device=main_flask.l_device)
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/parameter", methods=["GET"]) 
def parameter_get():
    """初期画面からStartボタンで遷移するパラメータ設定画面"""
    return render_template("parameter.html", l_device=main_flask.l_device)

@app.route("/stop", methods=["GET"])
def stop():
    logger.info('Stop処理開始')
    try:
        if main_flask.pid > 0:
            process = psutil.Process(main_flask.pid)
            process.kill()
            logger.info('プロセスkill完了')
            
            main_flask.queue01.put(0)
            main_flask.config["BASE"]["status"] = "stop"
            
            with open("./flask_app/dynamic_property.ini", "w") as file:
                main_flask.config.write(file)
                
        return render_template("index.html")
    except Exception as e:
        logger.error(f"停止処理でエラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500
