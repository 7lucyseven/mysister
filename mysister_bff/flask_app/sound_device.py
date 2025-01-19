import pyaudio

def get_device_list():
    # PyAudioのインスタンスを生成
    p = pyaudio.PyAudio()    

    # maxOutputChannelsが2以上の指定のデバイスインデックスを検索
    l_device = []
    for i in range(p.get_device_count()):
        num_of_input_ch = p.get_device_info_by_index(i)['maxOutputChannels']
        if(num_of_input_ch >= 2):
            # Todo デバッグログを記載したい
            # デバッグログ
            l_device.append(p.get_device_info_by_index(i)['name'])
    
    return l_device