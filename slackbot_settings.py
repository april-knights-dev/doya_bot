# coding: utf-8
import os

# botアカウントのトークンを指定
API_TOKEN = os.environ["API_TOKEN"]

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "もしかして僕を呼んだのだ？\n頑張ったことも添えてくれると僕が代わりにdoya部屋に送るのだ！"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ["plugins"]
