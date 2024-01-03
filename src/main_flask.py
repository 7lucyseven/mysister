from flask import Flask, render_template, request, jsonify
import sound_device
import main
import sys
sys.dont_write_bytecode = True
import mysister
from setup_logger import setup_logger
import threading

app = Flask(__name__)

def run(dict_parameter):
    mysister.run(dict_parameter["mode"])

@app.route("/")
def index():
    html = render_template("index.html")
    return html

@app.route("/parameter" ,methods=["POST"])
def parameter_post():
    dict_parameter = request.form.to_dict()

    logger = setup_logger(__name__)
    logger.info(dict_parameter)


    # スレッドを作る
    thread1 = threading.Thread(target=run, args=(dict_parameter,))

    # スレッドの処理を開始
    thread1.start()
    print("start")

    l_device = sound_device.get_device_list()
    html = render_template("parameter.html", l_device = l_device)
    return html

@app.route("/parameter",methods=["GET"])
def parameter_get():

    l_device = sound_device.get_device_list()
    html = render_template("parameter.html", l_device = l_device)
    return html


if __name__ == "__main__":
    app.run(debug=True)