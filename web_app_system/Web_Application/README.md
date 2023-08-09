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
main.py, static, templatesは一般的なものですが、app.yaml, cron.yaml, requirementes.txtなどを用意する必要があります。\
app.yamlでWebアプリをデプロイし、cron.yamlでモデルの更新をスケジュールします。

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

\
cronジョブが正常に動作するか確認したい場合は右側の縦3点をクリックして、ジョブを強制実行することができます。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/67e552c2-3af0-4df2-add8-b12113be590b" width=800>

## 機械学習モデルの更新
まずはFlaskを使ってWebアプリを実装しているPythonコードを再掲します。

      from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
      import pickle
      import pandas as pd
      import numpy as np
      from google.cloud import storage
      from io import BytesIO

      # Google Cloud Storageクライアントのセットアップ
      storage_client = storage.Client(project="ploject_id")
      bucket_name = 'bucket_name'

      # Google Cloud Storageからpickleファイルを直接読み込む関数
      def load_pickle_from_cloudstorage(file_path):
          bucket = storage_client.get_bucket(bucket_name)
          blob = bucket.blob(file_path)
          data = blob.download_as_bytes()
          with BytesIO(data) as f:
              pickledata = pickle.load(f)
          return pickledata

      # Google Cloud Storageからcsvファイルを直接読み込む関数
      def load_csv_from_cloudstorage(file_path):
          bucket = storage_client.get_bucket(bucket_name)
          blob = bucket.blob(file_path)
          data = blob.download_as_bytes()
          dataframe = pd.read_csv(BytesIO(data)) 
          return dataframe

      # Flaskアプリのセットアップ
      app = Flask(__name__)
      app.secret_key = 'pass'
      
      @app.route("/reflection")
      def reflect():
          with app.app_context():
              global model, encoder, df
              model = load_pickle_from_cloudstorage("model.pkl")
              encoder = load_pickle_from_cloudstorage("encoder.pkl")
              df = load_csv_from_cloudstorage("data.csv")
          return "Model, encoder, and df have been updated!"

      # メインページのルート
      @app.route("/")
      def index():
          try:
              df
          except:
              reflect()
          global please_select
          please_select = "選択してください"
          return render_template("index.html",
                                 maker_list=np.sort(df["maker"].unique()),
                                 maker_base=please_select,
                                 car_base=please_select,
                                 grade_base=please_select,
                                 year_base=please_select,
                                 df=df)

      # 車のオプションを取得するエンドポイント
      @app.route("/get_cars", methods=["GET"])
      def get_cars():
          selected_option = request.args.get("selected_option")
          session["selected_maker"] = selected_option  # 選択されたメーカーをセッションに保存
          options = np.sort(df[df["maker"] == selected_option]["car"].unique()).tolist()
          options.insert(0, please_select)
          return jsonify({"options": options})

      # 車種のオプションを取得するエンドポイント
      @app.route("/get_grades", methods=["GET"])
      def get_grades():
          selected_option = request.args.get("selected_option")
          session["selected_car"] = selected_option  # 選択された車種をセッションに保存
          options = np.sort(df[df["car"] == selected_option]["grade"].unique()).tolist()
          options.insert(0, please_select)
          return jsonify({"options": options})


      # 車の年式のオプションを取得するエンドポイント
      @app.route("/get_years", methods=["GET"])
      def get_years():
          selected_option = request.args.get("selected_option")
          session["selected_grade"] = selected_option  # 選択されたグレードをセッションに保存
          options = np.sort(df[df["grade"] == selected_option]["year"].unique()).tolist()
          options.insert(0, please_select)
          return jsonify({"options": options})

      # 予測を実行するエンドポイント
      @app.route("/prediction", methods=["GET", "POST"])
      def predict():
          try:
              if (request.form["maker"]!=please_select) and request.form["car"]!=please_select\
                    and request.form["grade"]!=please_select and request.form["year"]!=please_select\
                        and request.form.get("mileage").isdecimal():
                  #セッション
                  session["selected_mileage"] = request.form.get("mileage")
                  #車のデータを入力から取得
                  car = request.form.get("car")
                  grade = request.form.get("grade")
                  year = int(request.form.get("year"))
                  mileage=request.form.get("mileage")

                  # 特徴量作成
                  mileage_feature = pd.DataFrame({"mileage":[mileage]}) # 走行距離
                  # カテゴリ変数
                  category_features = pd.DataFrame({
                      "car":[car], 
                      "grade":[grade],
                      "year":[year]
                  })
                  # onehotencoding
                  category_onehot = pd.DataFrame(encoder.transform(category_features),
                                                 columns=encoder.get_feature_names_out()).astype("int")
                  # 特徴量結合
                  features = pd.concat([mileage_feature, category_onehot], axis=1)

                  # 予測
                  price = model.predict(features)
                  return render_template("result.html", price=int(price))
        
              else:#flashで誤入力情報を表示
                  if (not request.form["maker"]) or request.form["maker"] == please_select:
                      flash("メーカーを選択してください。", "error")
                  if (not request.form["car"]) or request.form["car"] == please_select:
                      flash("車種を選択してください。", "error")
                  if (not request.form["grade"]) or request.form["grade"] == please_select:
                      flash("グレードを選択してください。", "error")
                  if (not request.form["year"]) or request.form["year"] == please_select:
                      flash("年式を選択してください。", "error")
                  if not request.form.get("mileage").isdecimal():
                      flash("走行距離を整数値で入力してください。", "error")
                      session["selected_mileage"] = ""
                  else:
                      session["selected_mileage"] = request.form.get("mileage")

                  return redirect(url_for("index"))
    
          except Exception as e:
              # 例外が発生した場合にエラーメッセージをログに表示
              print("エラーが発生しました:", e)

機械学習モデル(エンコーダーとデータフレームも)の更新(初期化も)はreflect()関数で実行しています。\
cron.yamlに指定しているエンドポイント(/reflection)をreflect()関数に設定することで、\
cronジョブが定期実行された際にreflect()関数が実行されます。\

reflect()関数内では事前にCloud Storageに格納しているmodel, encoderをpickleファイルとして、\
dfをcsvファイルとして読み込み、代入しています。\
それぞれ別の関数を使用していますが、説明は割愛します。

# 所感
Webアプリの作成、デプロイ、cronジョブの実行など初めてのことばかりでしたが、なんとか自分がやりたかったことができました。\
そしてCloud Shellでコマンドを打つことに抵抗感がまったくない自分に気づきました。Ubuntuを個人で使い始めてターミナルに慣れてきたのかもしれません。GUIよりもとっつきやすかったです。\
また、何かを作ることを楽しんでいる自分を見つけることができ嬉しく思います。

