import openai
import os
import sys
import importlib
from flask_app import sister_memory
sys.path.append("../config")
import conf
import time

def respons(timestamp, userID, user_text):
    # 環境変数からAPIキーを取得
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    # promptの作成
    importlib.reload(conf)
    messages=[
        conf.Config.prompt_dict[conf.Config.prompt_mode]
    ] 
    
    l_user_text      = []
    l_assistant_text = []
    if(sister_memory.is_true("user", userID)):
        # 過去のユーザーの発言を取得する
        l_user_text = sister_memory.load_talk("user", userID)
        # print(l_user_text)

    if(sister_memory.is_true("assistant", 'Fortuna')):
        # AIの発言を取得する
        l_assistant_text = sister_memory.load_talk("assistant", 'Fortuna')

    # print(l_user_text + l_assistant_text)
    sorted_array = sorted(l_user_text + l_assistant_text, key=lambda x: x[1])

    for i in sorted_array:
        # print(i)
        messages.append({"role": i[0], "content": i[2]})
    
    messages.append({"role": "user", "content": user_text})

    # API実行
    try:
        res = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
    except Exception as e:
        # print(e)
        # print(messages)

        while True:
            del messages[1]
            if(20 > len(messages)):
                break

        res = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )

    sister_memory.save_talk("assistant", str(int(time.time()*1000)), 'Fortuna', res["choices"][0]["message"]["content"])
    sister_memory.save_talk("user", str(timestamp), userID, user_text)

    return res["choices"][0]["message"]["content"]