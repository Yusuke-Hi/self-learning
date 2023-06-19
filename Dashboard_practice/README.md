# 目的
この学習の目的はPythonによるダッシュボード作成を実践することです。

# データセット
今回使用するデータは"Steam"における月ごとのゲームの売上数に関するものです。

※SteamはPCゲームやゲームソフトウェアの販売やゲームプラットフォームの提供などを行っている会社です。\
"Popularity of games on Steam"\
URL: https://www.kaggle.com/datasets/michau96/popularity-of-games-on-steam/code

実際に書いたコードはディレクトリ内の"steam_dashboard.ipynb"にあります。

## 使用したライブラリ
Pandas, NumPy, Plotly(go), Dash(dcc, html, Input, Output)

# ダッシュボード
## 全期間の販売数ランキング
全ゲームの総販売数の10位までの総売上数を表示しています。\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/a8550e04-d1ed-4a1d-983c-205455beaa30" width=800>

## 販売数の推移
上に示した10タイトルをドロップダウンで選択し、発売から2021年2月までの販売数の推移を描画します。
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/2cdff5b0-be41-458f-b584-d7e515ec75fd" width=800>\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/f6e9bec9-fdaa-4bd8-9afc-92fc4635218d" width=800>\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/4bd530bf-3bf5-4d95-8d05-1e6c2bfc5ea4" width=800>\
<image src="https://github.com/Yusuke-Hi/self-learning/assets/131725916/ef3a7709-06ba-4ee6-a9d9-18ef3e6d4730" width=800>

# 所感
今回ダッシュボードというものを初めて作成しました。\
初めて使用したライブラリが多く、エラーが出たときにどこがおかしいか確認するのに苦労しましたが、
調べながら少しずつ作っていく楽しさがありました。

