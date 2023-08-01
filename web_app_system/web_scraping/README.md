# 【データ基盤】スクレイピングからデータ格納までのシステム
データを取得し、データベースに格納するまでのシステム構成は以下のようになっています。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/a4a96c6d-97f1-45e6-a00c-4a8194812da2" width=600>

## Bigquery
このシステムのゴールであるBigqueryの設定から解説します。\
※新しいプロジェクトの作成は事前に実施しています。

以下のようにBigqueryのページに移動し、データセットの作成、テーブルの作成を行います。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/02b734f1-ceb3-443a-a4e6-5b6e8d4c1439" width=600>

\
今回はスクレイピングしたデータを格納するため、ソースを空のテーブルにします。\
その他、任意のproject_id, dataset_name, table_nameを入力します。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/b300296c-1e23-4e8c-b9a5-e90635bc10e4" width=600>

\
格納する予定のデータのスキーマを追加していきます。\
任意のフィールド名、データ型、モードを入力します。\
ここではSQLでの取り出しを考慮して、スクレイピングを実行した日付のスキーマを追加しています。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/0f175b9a-6942-439e-8b08-3500030d2b41" width=600>

\
下に進んで"テーブルを作成"ボタンをクリックして完了です。

## Cloud Functions
スクレイピングを実行するCloud Functionsの設定について解説します。\
Cloud Functionsのページに移動し、"ファンクションを作成"ボタンをクリックします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/8d9d71b7-32fb-4d08-a568-1a7e6e60dea5" width=600>

\
環境：スペックは第一世代<第二世代です。\
今回は第一世代で十分でした。\
関数名：わかりやすい関数名をつけました。\
リージョン：リージョンにより料金やリージョントラブルの可能性が異なります。\
先人や教科書にならい、us-west1を選択しました。\
トリガー：Cloud Pub/Subに設定\
トピック：後でCloud Schedulerで紐付ける部分です。\
すでにある場合は選択して、ない場合は作成します。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/3292138d-e358-4abc-a3ab-23d0b4d469e2" width=600>

\
Runtime, build, connections and security settingsをクリックして、スペックを設定します。\
スクレイピングの実行時間を考慮して、割当メモリとタイムアウトを最大に設定しました。\
実行内容によってはタイムアウトエラーになるので気をつけてください。\
その他はデフォルト設定です。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/67b2c2db-502b-4b5d-b9d6-b39fabeff6fd" width=400>

\
コードの設定に移ります。\
ランタイムでPythonを選択します。\
コード内で起点となる関数名をエントリポイントに設定します。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/a6dd30a3-cd19-4c4c-a1c3-4e137d4c6da5" width=600>

\
main.pyに実行するコードを入力します。\
また、requirements.txtに使用するライブラリを入力します。\
"デプロイ"ボタンを押してデプロイします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/0322fd14-5872-4f82-8ed7-abc2c33fa15b" width=600>

## Cloud Scheduler
スクレイピングのトリガーを送信するCloud Schedulerの設定について解説します。\
Cloud Schedulerのページに移動して、"ジョブを作成"ボタンをクリックします。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/b7fc42c1-f92c-4f3a-a279-54c15efc5518" width=600>

\
ジョブの名前：わかりやすい名前をつけました。\
リージョン：us-west1(オレゴン)を選択しました。\
説明：見返した時にわかるように簡潔な文章にしました。\
頻度：週に1回、金曜日の12:00に設定しました。\
タイムゾーン：日本標準時に設定しました。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/289c2722-1564-4b5d-8fec-09c200f68344" width=400>

\
ターゲット タイプでPub/Subを選択します。\
次にCloud Functionsで設定したトピックを選択して、実行するFunctionを指定します。\
メッセージは不要なので、{}としています。\
"作成"ボタンをクリックして完了です。

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/7f498a26-da7c-4fce-a1cd-54c0989bbdbb" width=400>

\
これで、スクレイピングを定期実行する環境と格納先からなるデータ基盤を構築できました。

# スクレイピングコード
同ディレクトリ内に保存しているコードを再掲します。\
全体の構成としてはスクレイピングの実行、データフレームの作成、データクリーニング、データ挿入からなり、それぞれ関数になっています。\
最後のmain関数がエントリポイントとなっており、上記4つの内容を順に実行しています。\
※Pub/Subのエントリポイントとなる関数は引数を2つ設定する必要があります。

スクレイピング：requests, BeautifulSoupを使用しています。\
データフレームの作成：スクレイピングで取得したデータに日付を追加しています。\
データクリーニング：記号や漢字の削除、必要な部分だけを抽出しています。\
データの挿入：google-cloud-bigqueryを用いて、事前に作成したBigqueryのテーブルにデータを挿入しています。

    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import datetime

    from google.cloud import bigquery as gbq # BigQueryのテーブルにデータを挿入する

    def scraping():
        #1p目のurlと2p以降のベースurl
        first_url = "https://www.bigmotor.co.jp/bigmotor2/search/search2.php?manufacturer2=all&manufacturer=&cars=&grade=&type2=&yearb=&yeare=&mileageb=&mileagee=&priceb=&pricee=&state=&shop=&drive=&mission=&car_inspection=&cars=&keywords=&imported="
        base_url = "https://www.bigmotor.co.jp/bigmotor2/search/search2.php?manufacturer2=all&manufacturer=&cars=&grade=&type2=&yearb=&yeare=&mileageb=&mileagee=&priceb=&pricee=&state=&shop=&drive=&mission=&car_inspection=&keywords=&imported=&page="
    
        #pageを指定
        start_page = 1
        last_page = 60
    
        #取得するデータのリスト
        grade_list = []
        name_list = []
        price_list = []
        year_list = []
        mileage_list = []
    
        #複数ページのデータ取得
        for p_num in range(start_page,last_page+1):
            #ページのurlを指定/作成
            if p_num==1:
                url = first_url
            else:
                url = base_url + str(p_num)
        
            #htmlレスポンスを取得
            response = requests.get(url)
            #htmlをタグ単位に解析
            soup = BeautifulSoup(response.content, 'html.parser')
        
            # 本体価格を取得
            price_elements = soup.select('.price strong span')
            #"準備中"がある場合はbreak
            check_p = [p.text for p in price_elements]
            if "準備中" in check_p:
                print("Execute break")
                break
            else:
                for pe in price_elements:
                    price_list.append(pe.text)
            
            # グレードを取得
            car_grade_elements = soup.find_all("span", attrs={"class":"ch-1-sub"})
            for cge in car_grade_elements:
                grade_list.append(cge.text)
            
            # 車種を取得
            car_name_elements = soup.find_all("h3", attrs={"class":"ch-1"})
            for cne in car_name_elements:
                name_list.append(cne.text)
            
            # 年式を取得
            year_elements = soup.select('table.table-spec tr:nth-of-type(1) td')
            for ye in year_elements:
                year_list.append(ye.text)
                
            # 走行距離を取得
            mileage_elements = soup.select('table.table-spec tr:nth-of-type(2) td')
            for me in mileage_elements:
                mileage_list.append(me.text)
            
        #価格の数値を一意に定める
        p_li = [int(p)+1 for i, p in enumerate(price_list) if i%4==0]

        #name_listからmaker_listを作成
        maker_list = [name[name.find("【")+1: name.find("】")] for name in name_list]
    
        #車名からグレードを除去
        name_list = [s.replace(grade_list[i], "") for i, s in enumerate(name_list)]
    
        return p_li, maker_list, name_list, grade_list, year_list, mileage_list
    
    #データフレーム化
    def create_dataframe(p_li, maker_list, name_list, grade_list, year_list, mileage_list):    
        df = pd.DataFrame({
            "price":p_li,
            "maker":maker_list,
            "car":name_list,
            "grade":grade_list,
            "year":year_list,
            "mileage":mileage_list})
        #取得日を追加
        df["scraping_date"] = datetime.datetime.today().date()
        return df
    
    #データクリーニング
    def clean_df(df):
        df_cleaned = df.copy()
        # "】"以降を取得
        df_cleaned["car"] = df_cleaned["car"].map(lambda x:x[x.find("】")+1:])
        #西暦だけ取得
        df_cleaned["year"] = df_cleaned["year"].str[:4]
        # "km"より前を取得
        df_cleaned["mileage"] = df_cleaned["mileage"].str[:-2]
        # "万"が含まれる場合は10000をかけて整数に、含まれない場合は","を削除して整数にする
        df_cleaned["mileage"] = df_cleaned["mileage"].apply(lambda x: int(float(x[:-1])*10000) if "万" in x\
                                      else int(x.replace(",", "")))
        return df_cleaned

    # BigQueryのテーブルにデータをインサートする関数
    def bigquery_insert(df_cleaned):
        client = gbq.Client(project="project_name")
        table = client.get_table("project_id.database_name.table_name")
        client.insert_rows(table, df_cleaned.to_dict('records'))

    # Cloud Functionで実行する関数
    def main(request, context):
        p_li, maker_list, name_list, grade_list, year_list, mileage_list = scraping()#スクレイピング実行
        df = create_dataframe(p_li, maker_list, name_list, grade_list, year_list, mileage_list)#データフレーム作成
        df_cleaned = clean_df(df).dropna()#データクリーニング(前処理)
        bigquery_insert(df_cleaned)#bigqueryにデータを挿入

# 所感
まずはローカルでwebスクレイピングコードを作成することから初めましたが、本格的にスクレイピングをしたのは初めてだったため、試行錯誤の繰り返しでした。/
Cloud FunctionsやCloud Schedulerに関しては全く触ったことがなかったため、エラーとの戦いでした。\
ようやくBigqueryにデータを挿入できたときは思わず声をあげてガッツポーズしてしまいました。\
このパートではスクレイピング、Cloud Functions、Cloud Scheduler、pythonによるBigqueryの操作を一貫して学ぶことができました。
