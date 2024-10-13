from flask import Flask, render_template, request, jsonify
import sound_device
import main
import sys
sys.dont_write_bytecode = True
#import mysister
from setup_logger import setup_logger
import threading
import parameter_write
import configparser
import queue
from multiprocessing import Process
import psutil

app = Flask(__name__)

class main_flask:
    l_device = sound_device.get_device_list()
    thread1 = None
    config = configparser.ConfigParser()
    config.read("dynamic_property.ini")
    queue01 = queue.Queue()
    pid = -1

#def run(dict_parameter):
#    mysister.run(dict_parameter["mode"])

@app.route("/")
def index():
    """
    起動時の走る最初の処理
    """
    html = render_template("index.html")
    return html

@app.route("/parameter" ,methods=["POST"])
def parameter_post():
    

    logger = setup_logger(__name__)
    #logger.info(dict_parameter)

    result = parameter_write.service(request)
    main_flask.queue01.put(1)
    print(main_flask.queue01)
    main_flask.pid = main.boot(main_flask.thread1, main_flask.queue01)
    

    html = render_template("parameter.html", l_device = main_flask.l_device)
    return html

@app.route("/parameter",methods=["GET"])
def parameter_get():
    """
    初期画面からStartを押下して飛ぶパラメータ設定画面
    """

    html = render_template("parameter.html", l_device = main_flask.l_device)
    return html

@app.route("/stop",methods=["GET"])
def stop():

    ppid = main_flask.pid
    print(ppid)

    
    p = psutil.Process(ppid)
    p.kill()


    main_flask.queue01.put(0)
    main_flask.config["BASE"]["status"]   = "stop"

    with open("dynamic_property.ini", "w") as file:
        main_flask.config.write(file)

    html = render_template("parameter.html", l_device = main_flask.l_device)
    return html

if __name__ == "__main__":
    app.run(debug=True)