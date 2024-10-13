import os

class Config:
    # セッション管理
    # 今回は使用しない

    # データベース設定
    # 今回は使用しない

    # メール設定
    # 今回は使用しない

    # その他の設定
    # DEBUG = os.environ.get('DEBUG') in ['True', 'true', '1']
    # LANGUAGES = ['en', 'ja']

class DevelopmentConfig(Config):
    # 開発設定
    # DEBUG = True

class TestingConfig(Config):
    #テスト設定
    # TESTING = True

class ProductionConfig(Config):
    # 本番設定
    # SECRET_KEY = os.environ.get('SECRET_KEY')
