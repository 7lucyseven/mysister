from flask import Flask, render_template, request, jsonify
import pyaudio

app = Flask(__name__)


@app.route("/")
def index():
    html = render_template("index.html")
    return html

@app.route("/result",methods=["POST"])
def result():
    test = request.form.to_dict()
    print(test)
    html = render_template("index.html")
    return test

@app.route("/parameter")
def test():
    
    # PyAudioのインスタンスを生成
    p = pyaudio.PyAudio()    

    # 指定のデバイスインデックスを検索
    l_device = []
    for i in range(p.get_device_count()):
        num_of_input_ch = p.get_device_info_by_index(i)['maxInputChannels']
        if(num_of_input_ch == 0):
            l_device.append(p.get_device_info_by_index(i)['name'])


    html = render_template("parameter.html", l_device = l_device)
    return html


if __name__ == "__main__":
    app.run(debug=True)