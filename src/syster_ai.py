import openai
import os
import sys
sys.path.append("../config")
import conf

def respons(user_text):
    # 環境変数からAPIキーを取得
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    # promptの作成
    messages=[
        conf.prompt,
        {"role": "user", "content": user_text},
    ] 

    # API実行
    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )

    return res["choices"][0]["message"]["content"]