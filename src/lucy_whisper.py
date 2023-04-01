import glob
import os
import openai
import time

import hashlib
import sys
sys.path.append("../config")
import conf

hash_md5_tmp = ''
openai.api_key = os.environ['OPENAI_API_KEY']

while(1):
    files = glob.glob('C:\\Users\\Creator\\Documents\\サウンド レコーディング\\*m4a')
    voice_file_path = max(files, key=os.path.getctime)

    if('自動保存' in voice_file_path):
        time.sleep(3)
        continue

    with open(voice_file_path, 'rb') as file:
        fileData = file.read()
        hash_md5 = hashlib.md5(fileData).hexdigest()

    if(hash_md5 != hash_md5_tmp):
        hash_md5_tmp = hash_md5

        voice_file= open(voice_file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", voice_file)
        print(transcript["text"])

        lucy_text = conf.lucy_voice_text
        with open(lucy_text, mode = 'w', encoding='UTF-8') as f:
            f.write(transcript["text"])

    time.sleep(3)

