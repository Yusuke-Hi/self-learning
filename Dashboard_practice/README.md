# 目的
この学習の目的はPythonによるダッシュボード作成を実践することです。

# データセット
ホテルのお客様の宿泊予約がキャンセルされるか、されないかに関するデータセットを使います。

実際に書いたコードはディレクトリ内の"Code_Dashboard.ipynb"にあります。

## 使用したライブラリ
Pandas, Plotly(go), Dashです。

# ダッシュボード
## 全体像
全体像は以下の画像のようになっております。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/4e5c5118-7f40-452c-b3bb-8d98d2d1f723" width=800>

## 左上
キャンセルされた件数とキャンセルされなかった件数のパーセンテージを円グラフで表示しています。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/000b697a-16c0-41da-9e0a-a959fdde88e1" width=800>

## 左下
ドロップダウンで選択した特徴量の組み合わせの散布図が表示されます。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/7257a385-03f7-4b0e-8286-576e488e8247" width=800>

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/e2260c34-d93a-4dc1-af41-74692e0fa503" width=800>


## 右上
ドロップダウンで選択した特徴量の棒グラフが表示されます。\

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/5b55fded-f5e3-4500-b063-7b318b97c9d5" width=800>

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/8f8f917c-4610-4281-a8e9-018821e0a2f7" width=800>



## 右下
ドロップダウンで選択した特徴量のヒストグラムが表示されます。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/1f48ebe5-59a0-4b7f-b5ce-f89286d4f0e4" width=800>

<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/acc6a008-b092-4249-ab63-a0c01fd2df82" width=800>




# 所感
今回ダッシュボードというものを初めて作成しました。\
Plotlyを使うことによるインタラクティブを作るためにコールバックという機能を用いましたが、初めてのことだったので動作を確認しながら少しづつ組み立てていきました。\
また、レイアウトや配色の調整作業などは地道な作業でしたが、少しづつ完成に近づいていく感覚が楽しかったです。

