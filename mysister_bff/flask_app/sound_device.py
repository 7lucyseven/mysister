import pyaudio

def get_device_list():
    # PyAudioのインスタンスを生成
    p = pyaudio.PyAudio()    

    # 指定のデバイスインデックスを検索
    l_device = []
    for i in range(p.get_device_count()):
        num_of_input_ch = p.get_device_info_by_index(i)['maxInputChannels']
        if(num_of_input_ch == 0):
            l_device.append(p.get_device_info_by_index(i)['name'])
    
    return l_device