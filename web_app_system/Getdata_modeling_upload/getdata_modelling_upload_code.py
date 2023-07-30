import pandas as pd
from google.cloud import bigquery
import db_dtypes
from google.cloud import storage
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import pickle

def get_data(): #データを取得する関数
    client = bigquery.Client(project="carpriceprediction-391821") 
    
    # 実行query データ取得日が最新のデータをBigqueryから取得
    query = '''
    SELECT 
    price, maker, car, grade, year, mileage
    FROM `carpriceprediction-391821.FromBigMoter.main_table_rev2`
    WHERE scraping_date = (
      SELECT MAX(scraping_date)
      FROM `FromBigMoter.main_table_rev2` as hoge
    );
    '''

    result = client.query(query)

    # データフレームにする
    df = result.to_dataframe()
    df.columns=["price", "maker", "car", "grade", "year", "mileage"]
    X_orig = df.drop(["price", "maker"], axis=1)
    y_orig = df["price"]

    #OneHotEncoder
    encoder = OneHotEncoder(sparse_output=False, drop="first")
    #fit_transform
    X_onehot= encoder.fit_transform(X_orig.drop("mileage", axis=1))
    #データフレーム化
    df_X_onehot = pd.DataFrame(X_onehot, columns=encoder.get_feature_names_out()).astype("int")
    #mileageと結合
    train_encoded = pd.concat([X_orig["mileage"].reset_index(drop=True), df_X_onehot], axis=1)
    return encoder, train_encoded, y_orig, df

def construct_model(X, y): #モデルを構築する関数
    #モデル構築
    model = RandomForestRegressor(n_estimators=100, #Cloud Schedulerの実行時間の制限と今後のデータ数変化の可能性、pickle読み込みなどを考慮
                                max_depth=None, #カテゴリ変数の数が多いため、max_depthは無制限に設定
                                min_samples_split=2,
                                min_samples_leaf=1,
                                max_features="sqrt"
                                )#下3つのハイパーパラメータは交差検証により決定
    model.fit(X, y)
    return model

def upload(model, encoder, df):
    #データuploadのタイムアウト時間
    timeout_seconds = 2000
    # pickleでシリアライズ
    model_data = pickle.dumps(model)
    encoder_data = pickle.dumps(encoder)
    # バケット名指定
    bucket_name = 'bucket_name'
    # ストレージクライアントでproject名指定
    storage_client = storage.Client(project="project_name")
    # バケットインスタンス
    bucket = storage_client.bucket(bucket_name)
    
    # Google Cloud Storageへのmodel保存
    destination_blob_name_model = 'model.pkl'  # モデルを保存するファイル名
    blob = bucket.blob(destination_blob_name_model)
    blob.upload_from_string(model_data, timeout=timeout_seconds)
    
    # Google Cloud Storageへのencoder保存
    destination_blob_name_encoder = 'encoder.pkl'  # エンコーダーを保存するファイル名
    blob = bucket.blob(destination_blob_name_encoder)
    blob.upload_from_string(encoder_data, timeout=timeout_seconds)

    # DataFrameをCSVファイルとして保存してGoogle Cloud Storageへアップロード
    destination_blob_name_csv = 'data.csv'  # データフレームを保存するファイル名
    blob = bucket.blob(destination_blob_name_csv)
    blob.upload_from_string(data=df.to_csv(index=False), content_type='text/csv; charset=utf-8', timeout=timeout_seconds)

def main(context):
    encoder, train_encoded, y_orig, df = get_data()
    model = construct_model(train_encoded, y_orig)
    upload(model, encoder, df)
    
    # HTTPレスポンス
    return 'Model training and upload completed.'