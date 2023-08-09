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
