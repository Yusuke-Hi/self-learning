# 【機械学習モデリング】Bigqueryからのデータ取り出しと機械学習モデルの格納までのシステム
SQLでテーブルからデータを取り出し、機械学習モデルを構築、モデルの格納までのアーキテクチャは以下のようになっています。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/2abaff84-d867-4911-807c-a7ebff82ad87" width=400>


## Cloud Storage
構築した機械学習モデル、エンコーダー、データフレームを格納するCloud Storageの設定について解説します。\
※事前に新規プロジェクトを作成して、そこで操作を行っています。\
以下のようにCloud Storageのバケットページに移動し"作成"ボタンをクリックします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/1dbafd82-fa3b-4a8b-a3f0-3d1a8ebe0bcb" width=600>

\
バケットに名前をつけて、作成します。\
このバケット名はコードの中で使用します。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/1becbb87-dbfc-46f1-95a4-4460ee4d2539" width=600>

## Cloud Functions
Pythonコードを実行するCloud Functionsの設定について解説します。\
Cloud Functionsのページに移動して、"ファンクションを作成するボタンを"

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/dcf0aebe-5eef-4695-a137-1c4327d23eaf" width=600>

\
環境は第二世代を選択しました。\
Pub/Subでは540秒でタイムアウトしますが、"第二世代でHTTPリクエスト"を選択することで、3600秒まで時間を伸ばすことができます。\
モデリングの実行時間が540秒以上であるため、今回は第二世代に設定しました。\
その他は一般的な設定にしました。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/3f52091d-b5f7-419d-8638-79741fb0ed77" width=400>

\
Runtime, build, connections and security settingsではメモリとCPUを適当なものに設定し、\
上記で述べたようにタイムアウトを3600秒と最大にしています。\
次へをクリックして、コードの設定に移ります。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/b6d87745-734c-4858-83da-2569a0abf9f8" width=400>

Pythonを選択し、起点となる関数名をエントリポイントに入力します。\
コードをmain.pyに、ライブラリとバージョンをrequirements.txtに入力し、デプロイします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/6d5a0bc7-8e59-4aa9-8063-8961dd548fab" width=400>





