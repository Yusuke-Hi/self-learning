# 目的
この学習の目的はPythonによるダッシュボード作成を実践することです。

# データセット
ホテルのお客様の宿泊予約がキャンセルされるか、されないかに関するデータセットを使います。

Hotel Reservations Dataset\
URL: https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset

実際に書いたコードはディレクトリ内の"Code_Dashboard.ipynb"にあります。
## 使用したライブラリ
Pandas, Plotly(go), Dashです。

# ダッシュボード
## 全体像
全体像は以下の画像のようになっております。\
目的変数と説明変数の関係性を視覚的に確認するためのダッシュボードです。\
散布図、棒グラフ、Distgramに関しては目的変数であるキャンセルしたかどうかで色分けを行っています。
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/203d84aa-5c41-4c8c-83e3-9b4f33a5f608" width=800>


## 左上
キャンセルされた件数とキャンセルされなかった件数のパーセンテージを円グラフで表示しています。
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/000b697a-16c0-41da-9e0a-a959fdde88e1" width=600>

## 左下
ドロップダウンで選択した説明変数の組み合わせの散布図が表示されます。\
X軸、Y軸の説明変数を選択し、"apply"ボタンをクリックすると散布図が作成、表示されます。
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/7257a385-03f7-4b0e-8286-576e488e8247" width=600>

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/e2260c34-d93a-4dc1-af41-74692e0fa503" width=600>


## 右上
ドロップダウンで選択した説明変数の棒グラフが表示されます。
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/5b55fded-f5e3-4500-b063-7b318b97c9d5" width=600>
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/8f8f917c-4610-4281-a8e9-018821e0a2f7" width=600>



## 右下
ドロップダウンで選択した説明変数のDistgramが表示されます。
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/cfe9fdb9-7418-4c26-af87-4258198a142d" width=600>
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/4f14e826-73cb-410d-a609-06e4da382a95" width=600>




# 所感
今回ダッシュボードというものを初めて作成しました。\
Plotlyでインタラクティブなグラフを作るためにコールバックという機能を用いましたが、初めてのことだったので動作を確認しながら少しづつ組み立てていきました。\
また、レイアウトや配色の調整作業などは地道な作業でしたが、少しづつ完成に近づいていく感覚が楽しかったです。
