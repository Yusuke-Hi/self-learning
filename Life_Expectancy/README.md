# 目的
この学習の目的はBigQueryでSQLを使ってデータを抽出し、データ分析を実施することです。\
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
|Life_Expectancy_column|平均寿命|浮動小数点型|
|Adult_Mortality|15~60歳の1000人当たりの死者数|浮動小数点|
|Infant_Deaths|乳幼児の1000人当たりの死者数|整数型|
|Alcohol|1人当たりのアルコール摂取量(純アルコール)|浮動小数点型|
|Percentage_Expenditure|1人当たり国内総生産に占める医療費の割合(%)|浮動小数点型|
|Hepatitis_B|1歳児のB型肝炎（HepB）予防接種率（%）|浮動小数点型|
|Measles|1000人あたりの麻疹の報告症例数|整数型|
|BMI|人口全体の平均BMI|浮動小数点型|
|Under_Five_Deaths|人口1000人当たりの5歳未満死亡者数|整数型|
|Polio|1歳児のポリオ（Pol3）予防接種率（%）|浮動小数点型|
|Total_Expenditure|総政府支出に占める医療への一般政府支出の割合 (%)|浮動小数点型|
|Diphtheria|1歳児におけるジフテリア破傷風トキソイドおよび百日咳（DTP3）予防接種率（%）|浮動小数点型|
|HIV_AIDS|出生 1,000 人当たりの死亡数 HIV/AIDS (0 ～ 4 歳)|浮動小数点型|
|GDP|一人当たり国内総生産（米ドル）|浮動小数点型|
|Population|国の人口|浮動小数点型|
|Thinness_1-19_Years|10歳から19歳までの小児および青少年の痩せの有病率 (%)|浮動小数点型|
|Thinness_5-9_Years|5～9歳の子供の痩せの有病率(%)浮動小数点型|浮動小数点型|
|Income_Composition_Of_Resources|資源の所得構成に関する人間開発指数 (0 から 1 の範囲の指数)|浮動小数点型|
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
まずはゴールから設定しようと思います。\
今回のデータ分析のゴールは平均寿命予測モデルの作成とします。
## 計画
現在地：BigQueryにデータがある → ゴール：平均寿命予測モデルの作成\
現在地からゴールまでの計画を立てたいと思います。
## 1.BigQueryでデータを扱う
実践の目的であるBigQueryでのデータの抽出を行います。\
2000年から2015年までの16年分のデータがあります。\
今回は2010年から2014年までの5年分に絞ってからPythonでデータ分析を行います。\
2010年~2013年分のデータをモデル作成のための訓練、検証データとします。\
2014年分のデータを作成するモデルの最終評価に使用します。

## 2.Pythonによるデータ分析
・データ前処理\
・可視化\
・特徴量生成\
・訓練データ、検証データの分離\
・モデルチューニングモデル作成\
・検証\
・モデルの最終評価
## BigQueryでデータを扱う
### データの概要
テーブルのストレージ情報から行数は2938であることが確認でき、このデータセットは上記の列数22と合わせて\
2938行22列のテーブルデータであることがわかります。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/e1aa2f5c-9ae0-4d67-bf76-9874d5546a72" width = 500>

プレビュータブからテーブルデータを確認することができます。\
今回の目的変数は画像の中列あたりにある"Life_Expectancy"です。\
<image src = "https://github.com/Yusuke-Hi/self-learning/assets/131725916/a7623d88-eea3-413c-9ad9-8e5d133ac730" width = 500>

 ### データの抽出
 2010年から2014年までのデータを抽出するためにwhere句でデータを絞り込んでいます。\
 また、国名昇順、年度降順にするためにorder by句を使用しました。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/842f79e9-b454-43e6-afce-dab6e808ecd0" width=500>\
 抽出したデータを保存します。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/e501beca-ad10-4ccc-8d1e-c49a8a40fe9a" width = 500>
