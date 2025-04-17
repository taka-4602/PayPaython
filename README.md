# PayPaython ![2](images/1.png)
PythonからPayPay APIを操作するシンプルで使いやすいAPIラッパー   
## インストール
```py
pip install paypaython
```
必須：requests
## WebAPIは推奨されなくなりました
WebAPIは簡単に使えて便利でしたが、仕様変更が重なって推奨されなくなりました (リンク作成と送金ができなくなった)  
モバイルAPI用は↓からどうぞ  
https://github.com/taka-4602/PayPaython-mobile  
WebAPIもまだふつうに使えるので上記の機能が必要ない方はWebAPIでOKです、そのままどうぞ～
## [ ! ] PayPayからのレスポンス集 -> *[PayPayResponce.md](https://github.com/taka-4602/PayPaython/blob/main/PAYPAYRESPONCE.md)*
PayPay APIを使った時に返されるレスポンスをまとめたドキュメントです  
返ってきたレスポンスにどんな意味があるか知りたい場合、このドキュメントが役に立つかもしれません  
## 始める前に確認すること
### ログインを3回失敗するとアカウントが一時ロックされる
PayPayのサポートに連絡することで早く解除してもらえるみたいです (めんどくさいけど)
### セッションを作りすぎない
セッションを大量に作るとアカウント凍結の可能性があるみたいです (僕は未確認)
### 日本からしかアクセスできない
ふつうにブロックされます  
海外のバーチャルマシンとかを使う場合はプロキシを使いましょう
## Let's Go!
#### example.py
```py
from PayPaython import PayPay

paypay=PayPay(phone="08012345678",password="Test-1234")#ログイン済みclient_uuid="str"をセットするとOTPをスキップできます #access_token="str"トークンをセットするとログインをスキップします #proxy=dictでプロキシを設定できます
otp=input(f"SMSに届いた番号:{paypay.otp_prefix}-")#otp_prefixはSMSにくるワンタイムパスワードの接頭、TA-4602のTAの部分
paypay.resend_otp(paypay.otp_reference_id)#ワンタイムパスワードを再送
otp=input(f"SMSに届いた番号:{paypay.otp_prefix}-")#再送したらもっかい入力
paypay.login(otp)#ワンタイムパスワードを使ってログイン
print(paypay.access_token)#アクセストークン、リフレッシュはなぜか404が出る
print(paypay.client_uuid)#クライアントUUID、トークンの有効期限が切れた後にこれを設定して再度ログインするとOTPをスキップできる

link_info=paypay.link_check("https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW")#送金リンク確認、URLかID = "osuvUuLmQH8WA4kW" この部分 でリクエストできる
#or
link_info=PayPay().link_check("https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW")#link_checkはログインなしでも使うことができる
print(link_info)#リンクの合計金額
print(link_info.money_light)#金額のマネーライト分
print(link_info.money)#金額のマネー分
print(link_info.has_password)#パスワードがあるなら True
print(link_info.chat_room_id)#チャットルームID リンク受け取ったらメッセージ送れるあれのID
print(link_info.status)#PENDING COMPLEATED REJECTED FAILED
print(link_info.order_id)

paypay.link_receive("ここもURL / IDどっちでもOK")#送金リンク受け取り、パスワードはpassword=str
paypay.link_receive("ここもURL / IDどっちでもOK",link_info=link_info)#link_info=dict、これを設定するとリンクチェックをスキップする
paypay.link_reject("ここもURL / IDどっちでもOK")#送金リンクを辞退、これもlink_infoにdictをつっこめる

get_balance=paypay.get_balance()#残高確認
print(get_balance.all_balance)#すべての残高
print(get_balance.useable_balance)#すべての使用可能な残高
print(get_balance.money_light)#もってるマネーライト
print(get_balance.money)#もってるマネー
print(get_balance.points)#もってるポイント

get_profile=paypay.get_profile()#ユーザー情報を確認
print(get_profile.name)#ユーザー名
print(get_profile.external_user_id)#識別のためのユーザーID、自分で決められるやつとは違う
print(get_profile.icon)#アイコンのURL

print(paypay.get_history())#取引履歴を確認

create_p2pcode=paypay.create_p2pcode()#送金してもらうためのURLを作成する(PayPayアプリのQRコードとおなじ)
print(create_p2pcode.p2pcode)#↑で作ったURL

print(paypay.create_paymentcode())#レジでスキャンする用のバーコードを生成、画像はアプリ内で処理されるからコードだけ生成してもよっぽど機材を持ってる人じゃない限り無意味、死に機能

paypay.create_link(amount=1,password="1111")#送金リンクを作成、パスワードはpassword=str...この機能は2024/3月下旬に使えなくなった (エンドポイントから削除された)
paypay.send_money(amount=1,external_id="048f4fef00bdbad00")#指定したexternalidのユーザーに直接送金...この機能も2024/3月下旬に使えなくなった (エンドポイントから削除された)
```
#コメントで書いてあることが全部  
よく使う返り値は変数に入れているので、レスポンス全体を確認する必要はなくなった  
うまくいかなかった場合はエラーをraiseするようになったのでユーザー側がdictを気にするのはget_historyくらい  
### すでにログイン済みのClient_UUID or トークンでログイン
```py
paypay=PayPaython.PayPay("08012345678","Test-1234")
```
上のログイン部分にはあとClient_UUIDとトークンとプロキシを引数に使えます  
```py
paypay=PayPaython.PayPay(phone="08012345678",password="Test-1234",client_uuid="d2d786a9-6a9f-49e1-9139-ba2f5f7f9f1d",token="とてもながい==",proxy={"http":"http://example.com"})
```
ログイン済みのUUIDを使うとSMSに届く認証番号を入力しなくてもログインできます  
そんなのないよって方はとりあえず電話番号とパスワードだけでログインしてください、ログインに成功するとUUIDが確認できます
```py
print(paypay.client_uuid)
```
### アクセストークン
トークンを入力するとログインをスキップします  
WebAPIは2時間で失効します  
失効ならS0001かS9999が返ってきます (てきとーなものを入れるとサーバーエラーになる)  
失効したら再ログインしてトークンを再発行する必要があります  
トークンは返り値のdictにも含まれていますが、変数にもあります  
```py
print(paypay.access_token)
```
### 古いバージョン
PayPaythonバージョン3はモバイルAPI版と統一するためにNamedTupleを使用するよう変更しただけです  
中身の本質的な動作はまったく変わっていません  
古いバージョンのドキュメントはここから -> [README_old.md](https://github.com/taka-4602/PayPaython/blob/main/README_old.md)
## 余談
PayPaython_mobileをアップデートしたついでにWebAPI版もアップデートしました (フォーマットを統一したかった)
噂でWebAPIは凍結しやすいって聞いたことが何回かあるけど、僕は未確認だからそれについてはあんまり言及しません (トークンを使わずセッションを作りすぎるとなるのかもしれない)  
**WebAPI版PayPaythonはDiscontinuedです！** 僕はもうWebAPIを使ってないのでサポートできるか怪しいからです！
## コンタクト  
Discord サーバー / https://discord.gg/YdrTY2JPR2  
Discord ユーザー名 / .taka.  
#### 追記
どうやらAme-xさんによってJavaScript版がリリースされたようです  
https://github.com/EdamAme-x/paypay.x.js  
JavaScript勢はそっちを参考にするのもアリです
