# 目的
このデータ分析の目的はBigQueryでSQLを使って前処理を行い、機械学習を実施することです。\
BigQueryでデータを扱えることが機械学習エンジニア/データサイエンティストのデファクトスタンダードになりつつあると知り、実践することにしました。

# データセット
データセットはKaggleの"Human Resources Data Set"を使用します。URLは下記のとおりです。
https://www.kaggle.com/datasets/rhuebner/human-resources-data-set
このデータセットはHuman Resourceに関するプロフェッショナルを育てるために作成されたデータです。
各変数の設は以下の表のとおりです。

|特徴量|内容|データ型|
|-----|----|-------|
|Employee Name|労働者の名前|text|
|EmpID|労働者のID|text|
|MarriedID|1:既婚者, 0:未婚者|binary|
|MaritalStatusID|


## このデータセットを選んだ理由
・欠損値を含んでいるため、前処理の練習になる\
・単純に興味がある分野、考察が楽しそう

# BigQueryでの操作
### プロジェクトの作成

###

