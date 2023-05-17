# 目的
このデータ分析の目的はBigQueryでSQLを使って前処理を行い、データ分析を実施することです。\
BigQueryでデータを扱えることが機械学習エンジニア/データサイエンティストのデファクトスタンダードになりつつあると知り、実践することにしました。

# データセット
データセットはKaggleの"Life Expectancy(WHO)"を使用します。URLは下記のとおりです。\
https://www.kaggle.com/datasets/kumarajarshi/life-expectancy-who?select=Life+Expectancy+Data.csv

このデータセットは世界保健機関(WHO)が2000年から2015年にかけて世界193ヵ国の平均寿命と健康要因を調査したものです。\
各変数の説明は以下の表のとおりです。

|変数|説明|データ型|
|-----|----|-----|
|Country|国名|文字型|
|Year|西暦年|整数型|
|Status|途上国か先進国か|文字型|
|Life expectancy|平均寿命|浮動小数点型|
|Adult Mortality|15~60歳の1000人当たりの死者数|浮動小数点|
|infant deaths|乳幼児の1000人当たりの死者数|整数型|
|Alcohol|1人当たりのアルコール摂取量(純アルコール)|浮動小数点型|
|percentage expenditure|1人当たり国内総生産に占める医療費の割合(%)|浮動小数点型|
|Hepatitis B|1歳児のB型肝炎（HepB）予防接種率（%）|浮動小数点型|
|Measles|1000人あたりの麻疹の報告症例数|整数型|
|BMI|人口全体の平均BMI|浮動小数点型|
|under-five deaths|人口1000人当たりの5歳未満死亡者数|整数型|
|Polio|1歳児のポリオ（Pol3）予防接種率（%）|浮動小数点型|
|Total expenditure|総政府支出に占める医療への一般政府支出の割合 (%)|浮動小数点型|
|Diphtheria|1歳児におけるジフテリア破傷風トキソイドおよび百日咳（DTP3）予防接種率（%）|浮動小数点型|
|HIV/AIDS|出生 1,000 人当たりの死亡数 HIV/AIDS (0 ～ 4 歳)|浮動小数点型|
|GDP|一人当たり国内総生産（米ドル）|浮動小数点型|
|PopulationSchooling years|国の人口|浮動小数点型|
|thinness 1-19 years|10歳から19歳までの小児および青少年の痩せの有病率 (%)|浮動小数点型|
|thinness 5-9 years|5～9歳の子供の痩せの有病率(%)浮動小数点型|浮動小数点型|
|Income composition of resources|資源の所得構成に関する人間開発指数 (0 から 1 の範囲の指数)|浮動小数点型|
|Schooling|就学年数(年)|浮動小数点型|

## このデータセットを選んだ理由
・欠損値を含んでいるため、前処理の練習になると思った\
・現実のデータを対象にデータ分析を実践したかった\
・データそのものに興味があった\
・実データから有益な知見が得られるかもしれないと期待した

# BigQueryで下準備
## 準備
### プロジェクトの作成
"Life Expectancy"という名前でプロジェクトを作成します。\
<img src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/919d61b7-cd8b-410f-9ee2-1262b58a8842" width=500>

### データセットの作成
"Life_Ecpectancy"という名前でデータセットを作成します。（スペースは使えない）\
<img src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/e32f5e65-e7b2-44f1-9b33-6f883c7e66e6" width=500>

### テーブルの作成
csvファイルをBigQueryにアップロードしてSQLテーブルを作成します。\
<img src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/ace7d5e8-d5f3-4171-b531-18e10e60945d" width=500>

列名、データ型、説明を入力\
<img src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/2bed2022-acdb-4448-a26c-4d1ae6b66148" width=500>

# データ分析のゴールと計画
## ゴール：平均寿命予測モデルの作成
まずゴールはから設定しようと思います。\
今回のデータ分析のゴールは平均寿命予測モデルの作成とします。
## 計画
現在地：BigQueryにデータがある → ゴール：平均寿命予測モデルの作成\
現在地からゴールまでの計画を立てたいと思います。
## 1.BigQueryで前処理
今回の実践の目的であるBigQueryでのデータ前処理を行います。\
・データクレンジング\
欠損値や誤値があれば対応します。\
・データの絞り込み\
使用するデータには2000年から2015年までの16年分のデータがあります。\
今回は2011年から2015年までの5年分に絞ってからPythonでデータ分析を行います。\

## 2.Pythonによるデータ分析
・可視化\
・特徴量生成\
・訓練データ、検証データの分離\
・モデルチューニングモデル作成\
・検証

## BigQueryで前処理
### データ概要
テーブルのストレージ情報から行数は2938であることが確認でき、このデータセットは上記の列数22と合わせて\
2938行22列のテーブルデータであることがわかります。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/e1aa2f5c-9ae0-4d67-bf76-9874d5546a72" width = 500>

プレビュータブからテーブルデータを確認することができます。\
今回の目的変数は画像の中列あたりにある"Life_Expectancy"です。\
<image src = "https://github.com/Yusuke-Hi/self-learning/assets/131725916/a7623d88-eea3-413c-9ad9-8e5d133ac730" width = 500>





