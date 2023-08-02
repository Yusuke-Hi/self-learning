from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
from google.cloud import storage
from io import BytesIO

# Google Cloud Storageクライアントのセットアップ
storage_client = storage.Client(project="project_name")
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

#model, encoder, dfを更新するエンドポイント
@app.route("/reflection")
def reflect():
    global model, encoder, df
    #model, encoder, dfをGoogle Cloud Storageから直接読み込む
    model = load_pickle_from_cloudstorage("model.pkl")
    encoder = load_pickle_from_cloudstorage("encoder.pkl")
    df = load_csv_from_cloudstorage("data.csv")

# メインページのルート
@app.route("/")
def index():
    #model, encoder, dfの初期化
    try:
        df
    except:
        reflect()
    return render_template("index.html", maker_list=np.sort(df["maker"].unique()))

# 車名のオプションを取得するエンドポイント
@app.route("/get_cars", methods=["GET"])
def get_cars():
    selected_option = request.args.get("selected_option")
    options = np.sort(df[df["maker"] == selected_option]["car"].unique()).tolist()
    return jsonify({"options": options})

# グレードのオプションを取得するエンドポイント
@app.route("/get_grades", methods=["GET"])
def get_grades():
    selected_option = request.args.get("selected_option")
    options = np.sort(df[df["car"] == selected_option]["grade"].unique()).tolist()
    return jsonify({"options": options})

# 年式のオプションを取得するエンドポイント
@app.route("/get_years", methods=["GET"])
def get_years():
    selected_option = request.args.get("selected_option")
    options = np.sort(df[df["grade"] == selected_option]["year"].unique()).tolist()
    return jsonify({"options": options})

# 予測を実行するエンドポイント
@app.route("/prediction", methods=["GET", "POST"])
def predict():
    try:
        if request.form["maker"] and request.form["car"] and request.form["grade"] \
            and request.form["year"] and request.form.get("mileage").isdecimal():
            #車のデータをブラウザ入力から取得
            car = request.form.get("car")
            grade = request.form.get("grade")
            year = int(request.form.get("year"))
            mileage=request.form.get("mileage")

                # 特徴量作成
            mileage_feature = pd.DataFrame({"mileage":[mileage]}) #走行距離
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
        
        else:
            #データ未入力、走行距離が数字出ない場合にエラーページを表示
            return render_template("error.html")
    
    except Exception as e:
        # 例外が発生した場合にエラーメッセージをログに表示
        print("エラーが発生しました:", e)
        return render_template("error.html", message="An error occurred.")
