# PayPaython ![2](images/1.png)
PythonからPayPay APIを操作するシンプルで使いやすいAPIラッパー   
### >> ```pip install paypaython``` <<
## WebAPIは推奨されなくなりました
WebAPIは簡単に使えて便利でしたが、仕様変更が重なって推奨されなくなりました  
モバイルAPI用は↓からどうぞ  
https://github.com/taka-4602/PayPaython-mobile  
WebAPIもまだふつうに使えるのでWebAPIでOKな人はそのままどうぞ～
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
## すでにPayPayを操作できるDiscordのBotをデプロイしてます！
↓Bot招待リンク↓  
https://discord.com/api/oauth2/authorize?client_id=1189119988678803496&permissions=8&scope=bot
## Let's Go!
### lets_go_2.x.x.py
```python
import PayPaython

#ログイン
paypay=PayPaython.PayPay(phone="08012345678",password="Test-1234")#ログイン済みclient_uuid="str"をセットするとOTPをパスできます #token="str"トークンをセットするとログインをパスします #proxy=dictでプロキシを設定できます
otp=input(f"SMSに届いた番号:{paypay.pre}-")
print(paypay.login(otp))#uuid確認用に["client_uuid"]にわざとuuidくっつけてます
#SMSの認証番号を再送
print(paypay.resend_otp(paypay.refid))#refidの使い道ができた
otp=input(f"SMSに届いた番号:{paypay.pre}-")#もっかい入力
print(paypay.login(otp))
#送金リンク確認
print(paypay.check_link("osuvUuLmQH8WA4kW"))#ぺいぺい送金リンクの https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW <-ここね
#or
print(PayPaython.Pay2().check_link("osuvUuLmQH8WA4kW"))#ログインなしでcheck_linkを使えるPay2クラスです #これもproxy=dictでプロキシを設定できる
#送金リンク受け取り
print(paypay.receive("osuvUuLmQH8WA4kW"))#パスワードはpassword=str #事前にcheck_linkして返ってきたdictを引数infoに入れるとそのdictを使うようになります
#送金リンクを辞退
print(paypay.reject("osuvUuLmQH8WA4kW"))#これもinfoにdictつっこめる
#送金リンクを作成
print(paypay.create_link(kingaku=1,password="1111"))#パスワードはpassword=str
#残高確認
print(paypay.balance())
#ユーザー情報
print(paypay.user_info())
#ユーザーの表示情報
print(paypay.display_info())
#ユーザーの支払い方法
print(paypay.payment_method())
#取引履歴
print(paypay.history())
#指定したexternalidのユーザーに直接送金
print(paypay.send_money(kingaku=1,external_id="048f4fef00bdbad00"))#このidはてきとーです
#送金してもらうためのURLを作成する(PayPayアプリのQRコードとおなじ)
print(paypay.create_p2pcode())
#支払いのワンタイムコードを作成する(ホーム画面にあるあのバーコードとおなじ)
print(paypay.create_payment_otcfh())
```
いちおう#コメントで大まかな使い方は記載してます  
send_moneyで使うexternal_idはuser_infoにくっついてきます
### すでにログイン済みのclient_uuid or トークンでログイン
```python
paypay=PayPaython.PayPay("08012345678","Test-1234")
```
上のログイン部分にはあとclient_uuidとトークンとプロキシを引数に使えます  
```python
paypay=PayPaython.PayPay(phone="08012345678",password="Test-1234",client_uuid="d2d786a9-6a9f-49e1-9139-ba2f5f7f9f1d",token="とてもながい==",proxy={"http":"http://example.com"})
```
###### 引数全体としてはこんなカンジ
ログイン済みのuuidを使うとSMSに届く認証番号を入力しなくてもログインできます  
そんなのないよって方はとりあえず電話番号とパスワードだけでログインしてください、ログインに成功するとuuidが確認できます
### uuidの確認
 ```python
print(paypay.uuid)
```
### アクセストークンについて
トークンを入力するとログインをスキップします  
WebAPIでは2時間で失効します  
失効ならS0001かS9999が返ってきます (てきとーなものを入れるとサーバーエラーになる)  
失効したら再ログインしてトークンを再発行する必要があります  
~~トークンログインについては1回Twitterでぼそっとつぶやいたのでそれを参考にしといてください~~  
-> PayPaython 2.2.0からトークンログイン機能がつきました  
#### [Twitter](https://twitter.com/TakeTakaAway/status/1744998645488070877)  
![1](images/0.png)  
###### これだけ  
トークンは返り値のdictにも含まれていますが、変数にもあります  
```python
print(paypay.token)
```
### もう少し知る
```paypay.pre```
- ワンタイムパスワードの接頭語  
  TA-4602の"TA"の部分
  

```PayPaython.Pay2```
- check_linkはログインしていなくても使えるので、ログインなしでcheck_linkだけ使えるPay2クラスです  
  ```PayPatrhon.Pay2().check_link("osuvUuLmQH8WA4kW")```  
  Pay2()には引数にプロキシをぶちこめます  
  ```Pay2(proxy=dict)```
## コンタクト  
Discord サーバー / https://discord.gg/aSyaAK7Ktm  
Discord ユーザー名 / .taka.  
#### 追記
どうやらAme-xさんによってJavaScript版がリリースされたようです  
https://github.com/EdamAme-x/paypay.x.js  
JavaScript勢はそっちを参考にするのもアリです
