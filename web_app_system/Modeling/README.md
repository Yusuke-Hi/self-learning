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

\
Pythonを選択し、起点となる関数名をエントリポイントに入力します。\
コードをmain.pyに、ライブラリとバージョンをrequirements.txtに入力し、デプロイします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/6d5a0bc7-8e59-4aa9-8063-8961dd548fab" width=400>

## Cloud Scheduler
Cloud Functionsにリクエストを送信するCloud Schedulerの設定について解説します。\
下図のようにCloud Schedulerのページに移動し、"ジョブを作成"ボタンをクリックします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/918f2f03-b3dd-49ff-8c89-d8ba283cc46d" width=400>

\
名前、リージョン、説明、頻度、タイムゾーンを設定します。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/1076dd1f-dd15-4eb4-85cc-e92bcdadacf8" width=400>

\
「実行内容を構成する」ではターゲットタイプをHTTPにしています。\
また、URLではCloud Functionsでデプロイした際に作成されるURLを使用します。\
作成ボタンをクリックします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/6daa3122-4eeb-40c2-9daf-947e63aa8f83" width=400>

# Pythonコード
同ディレクトリ内にあるPythonコードを再掲します。\
このコードをCloud Functionsのmain.pyに実装しました。\
エントリポイントに指定したmain関数内で、データ取得、機械学習モデリング、データアップロードそれぞれの関数を順次実行しています。\
※HTTPリクエスト時のmain関数では引数を1つとし、HTTPレスポンスとしてテキストをreturnする必要があります。

データ取得：\
・google-cloud-bigqueryを用いてSQLを実行してデータを取得\
・取得したデータをデータフレーム化\
・ダミー変数化\
機械学習モデリング：RandomForestRegressorでモデリング
データアップロード：\
モデルとエンコーダーはpickleファイルとしてCloud Storageに上書き保存\
データフレームはcsvファイルとしてCloud Storageに上書き保存\
※Cloud Storage上に事前に作成したバケットを使用

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

# 所感
スクレイピングと重なる部分がいくつかあったため、システム構築をスムーズにできました。\
GCPに少しずつなれてきたということでしょうか。\
それでもPython上でのSQL実行やHTTPリクエスト、Cloud Storageへのアップロードなど、多くことを経験することができました。
