# 【データ基盤】スクレイピングからデータ格納までのシステム
データを取得し、データベースに格納するまでのシステム構成は以下のようになっています。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/a4a96c6d-97f1-45e6-a00c-4a8194812da2" width=600>

## Bigquery
このシステムのゴールであるBigqueryから説明していきます。\
※新しいプロジェクトの作成は事前に実施しています。\

以下のようにBigqueryのページに移動し、データセットの作成、テーブルの作成を行います。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/02b734f1-ceb3-443a-a4e6-5b6e8d4c1439" width=600>

今回はスクレイピングしたデータを格納するため、ソースを空のテーブルにします。\
その他、任意のproject_id, dataset_name, table_nameを入力します。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/b300296c-1e23-4e8c-b9a5-e90635bc10e4" width=600>

格納する予定のデータのスキーマを追加していきます。\
任意のフィールド名、データ型、モードを入力します。\
ここではSQLでの取り出しを考慮して、スクレイピングを実行した日付のスキーマを追加しています。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/0f175b9a-6942-439e-8b08-3500030d2b41" width=600>

下に進んで"テーブルを作成"ボタンをクリックして完了です。

## Cloud Functions
スクレイピングを実行するCloud Functionsについて説明していきます。\
Cloud Functionsのページに移動し、"ファンクションを作成"ボタンをクリックします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/8d9d71b7-32fb-4d08-a568-1a7e6e60dea5" width=600>

環境：スペックは第一世代<第二世代です。\
今回は第一世代で十分でした。\
関数名：わかりやすい関数名をつけました。\
リージョン：リージョンにより料金やリージョントラブルの可能性が異なります。\
先人や教科書にならい、us-west1を選択しました。\
トリガー：Cloud Pub/Subに設定\
トピック：後でCloud Schedulerで紐付ける部分です。\
すでにある場合は選択して、ない場合は作成します。\

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/3292138d-e358-4abc-a3ab-23d0b4d469e2" width=600>


