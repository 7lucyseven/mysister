from flask_app import create_app

# Flaskアプリケーションのインスタンスを作成
app = create_app()

if __name__ == "__main__":
    # 開発用サーバーを起動
    # host: ローカルホストで実行
    # port: 8080ポートを使用
    # debug: デバッグモードを有効化
    app.run(host='localhost', port=8080, debug=True)
