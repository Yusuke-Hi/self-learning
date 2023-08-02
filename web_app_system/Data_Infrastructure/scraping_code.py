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