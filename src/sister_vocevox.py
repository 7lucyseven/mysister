import requests
import argparse
import json
import pyaudio
import sys
sys.path.append("../config")
import conf

def speak(sister_respons):

    # サーバのホスト名を指定
    HOSTNAME='192.168.0.15'

    #「;」で文章を区切り１行ずつ音声合成させる
    texts = sister_respons.split(';')
    
    # 読み上げキャラのID
    speaker = 14

    # 音声合成処理のループ
    for i, text in enumerate(texts):
        # 感情パラメータ個所をスキップ
        if(i == 1 and conf.prompt_mode == "prompt_heavy"):
            continue

        # 文字列が空の場合は処理しない
        if(text == ''):
            continue
        
        # 
        if(len(text) > 200):
            text = text[0:200]

        # audio_query (音声合成用のクエリを作成するAPI)
        res1 = requests.post('http://' + HOSTNAME + ':50021/audio_query',
                            params={'text': text, 'speaker': speaker})
        # synthesis (音声合成するAPI)
        res2 = requests.post('http://' + HOSTNAME + ':50021/synthesis',
                            params={'speaker': speaker},
                            data=json.dumps(res1.json()))
        
        data = res2.content
        
        # PyAudioのインスタンスを生成
        p = pyaudio.PyAudio()
        
        # 指定のデバイスインデックスを検索
        for i in range(4,10):
            if('Yamaha SYNCROOM Driver' in p.get_device_info_by_index(i)['name']):
                output_device_index = i
                break

        # ストリームを開く
        stream = p.open(format=pyaudio.paInt16,  # 16ビット整数で表されるWAVデータ
                    channels=1,  # モノラル
                    rate=24000,  # サンプリングレート
                    output=True,
                    output_device_index = output_device_index)
        
        # WAV データを直接再生する
        stream.write(data[46:])
        
        # ストリームを閉じる
        stream.stop_stream()
        stream.close()

        # PyAudio のインスタンスを終了する
        p.terminate()
        
        