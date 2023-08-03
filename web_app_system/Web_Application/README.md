# 【Webアプリ】Webアプリのデプロイから機械学習モデルの更新までのシステム
GoogleAppEngineを使って作成したWebアプリをデプロイするところから、機械学習モデルを更新するところまでのアーキテクチャは以下のようになっています。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/9223ed8e-062a-4ff7-bfbf-7760ab0a9783" width=400>

## デプロイ
デプロイはCloud ShellでCUIで操作します。\
プロジェクトに移動し、ウィンドウ右上のスクリーンのようなマークをクリックします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/93879ce4-87f0-4d78-b819-36ebacb7ae70" width=800>

\
ホームディレクトリにはREADMEファイルが初期配置されており、webアプリのディレクトリをアップロードしました。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/ac9af43f-7810-4794-bfd7-9f0a0bec148c" width=600>

ディレクトリ構造は以下のようになっています。\
main.py, static, templatesは一般的なものですが、app.yaml, cron.yaml, requirementes.txtなどを用意する必要があります。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/cda4d5f5-ebe2-466e-bb28-d46b216e4a8c" width=200>

app.yaml

      #GAEの設定ファイル。
      #インスタンスクラスやスケーリングの条件などを記載する
      #runtimeは必須パラメータ
      #entrypointはcronジョブを起動するために必要
      runtime: python38
      entrypoint: gunicorn -b :$PORT main:app


app.yamlがあるディレクトリで以下のコマンドを実行することで、Webアプリをデプロイできます。
    
    gcloud app deploy

デプロイしたあとは以下のコマンドでウェブアプリにアクセスして、動作を確認できます。

    gcloud app browse

動作がおかしい場合やそもそも起動しない場合は以下のコマンドでログを確認できます。

    gcloud app logs tail -s default

cron.yaml

      cron:
      - description: "Weekly task"  # cronジョブの説明
       url: /reflection  # Flaskアプリで処理したいエンドポイントのURL
       schedule: every friday 13:30 # 週に1回実行、毎週金曜日の13:30
       timezone: Asia/Tokyo  # タイムゾーンを設定（日本のタイムゾーンを使用）
       
同様にcron.yamlがあるディレクトリで以下のコマンドを実行することで、cronジョブをデプロイできます。

    gcloud app deploy cron.yaml
    
正常にデプロイが成功していればCloud SchedulerのApp Engineのcronジョブのタブにジョブが作成されます。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/859ecc0f-1d11-43c4-96c2-5b75d4b24ce3" width=800>

cronジョブが正常に動作するか確認したい場合は右側の縦3点をクリックして、ジョブを矯正実行することができます。
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/67e552c2-3af0-4df2-add8-b12113be590b" width=800>






















