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

class MainFlask:
    l_device = sound_device.get_device_list()
    thread1 = None
    config = configparser.ConfigParser()
    config.read("./flask_app/dynamic_property.ini")
    queue01 = queue.Queue()
    pid = -1

app = Blueprint('main', __name__)

@app.route("/")
def index():
    """起動時に実行される最初の処理"""
    return render_template("index.html")

@app.route("/parameter", methods=["POST"])
def parameter_post():
    logger = setup_logger(__name__)
    
    try:
        writer = parameter_write.parameter_write()
        writer.service(request)
        MainFlask.queue01.put(1)
        MainFlask.pid = main.boot(MainFlask.thread1, MainFlask.queue01)
        return render_template("parameter.html", l_device=MainFlask.l_device)
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/parameter", methods=["GET"]) 
def parameter_get():
    """初期画面からStartボタンで遷移するパラメータ設定画面"""
    return render_template("parameter.html", l_device=MainFlask.l_device)

@app.route("/stop", methods=["GET"])
def stop():
    try:
        if MainFlask.pid > 0:
            process = psutil.Process(MainFlask.pid)
            process.kill()
            
            MainFlask.queue01.put(0)
            MainFlask.config["BASE"]["status"] = "stop"
            
            with open("dynamic_property.ini", "w") as file:
                MainFlask.config.write(file)
                
        return render_template("parameter.html", l_device=MainFlask.l_device)
    except Exception as e:
        logger.error(f"停止処理でエラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500
