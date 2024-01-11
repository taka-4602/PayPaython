# PayPaython
PythonからPayPay APIを操作するシンプルで使いやすいAPIラッパー
## 始める前に確認すること
### ログインを3回失敗するとアカウントが一時ロックされる
PayPayのサポートに連絡することで早く解除してもらえるみたいです(めんどくさいけど)
### セッションを作りすぎない
セッションを大量に作るとアカウント凍結の可能性があるみたいです
## すでにPayPayを操作できるDiscordのBotをデプロイしてます！
↓Bot招待リンク↓  
https://discord.com/api/oauth2/authorize?client_id=1189119988678803496&permissions=8&scope=bot
## 注意：PayPaython 1.x.x系と2.x.x系は別物です
APIラッパー側の機能を減らしてユーザー側の自由度を上げたものが2.x.x系です  
printも消してエラー判定のコードも消しています  
もし自由度よりもターミナルでちまちまやりたい方は1.x.x系をおすすめします  
- ```pip install paypaython==1.1.0```
## Let's Go!
- ```pip install requests``` (PayPayのAPIにリクエストするんだから必須)
- ```pip install paypaython``` (これ)

この2つをインストールしたらリポジトリにあるlets go.pyからすぐに使い始めることができます！
### lets_go_2.1.0.py
```python
import PayPaython

#ログイン
paypay=PayPaython.PayPay(phone="08012345678",password="Test-1234")
otp=input("SMSの番号: ")
print(paypay.login(otp))#uuid確認用に["client_uuid"]にわざとuuidくっつけてます
#送金リンク確認
print(paypay.check_link("osuvUuLmQH8WA4kW"))
#送金リンク受け取り
print(paypay.receive("osuvUuLmQH8WA4kW"))#ぺいぺい送金リンクの https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW <-ここね #パスワードはpassword=int
#送金リンクを辞退
print(paypay.reject("osuvUuLmQH8WA4kW"))
#送金リンクを作成
print(paypay.create_link(kingaku=1,password=1111))#パスワードはpassword=int
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
print(paypay.send_money(kingaku=1,externalid="048f4fef00bdbad00"))#このidはてきとーです
#送金してもらうためのURLを作成する(PayPayアプリのQRコードとおなじ)
print(paypay.create_p2pcode())
#支払いのワンタイムコードを作成する
print(paypay.create_payment_otcfh())
```
いちおう#コメントで大まかな使い方は記載してます  
大まか...ですがほんとうにこれだけです、とってもシンプル  
send_moneyで使うexternal_idはuser_infoにくっついてきます
### すでにログイン済みのclient_uuidでログイン
```python
paypay=PayPaython.PayPay("08012345678","Test-1234")
```
上のログイン部分にはあとclient_uuidとプロキシを引数に使えます  
```python
paypay=PayPaython.PayPay(phone="08012345678",password="Test-1234",client_uuid="d2d786a9-6a9f-49e1-9139-ba2f5f7f9f1d",proxy="example.com")
```
###### 引数全体としてはこんなカンジ
ログイン済みのuuidを使うとSMSに届く認証番号を入力しなくてもログインできます！  
そんなのないよって方はとりあえず電話番号とパスワードだけでログインしてください、ログインに成功するとターミナルにuuidが表示されます
### アクセストークンについて
2時間ほどで失効します  
失効したら再ログインしてトークンを再発行する必要があります  
実はこのログイン方法以外にトークンログインすることもできます  
そっちの方は特に公開するつもりはないです(ただクッキーにトークンつけるだけ...)  
トークンはクッキーにくっついてるのでセッション開始時に有効なトークンをくっつけてあげてください  
これも無効ならS0001かS9999が返ってきます(てきとーなものを入れるとサーバーエラーになる)  
トークンログインについては1回Twitterでぼそっとつぶやいたのでそれを参考にしといてください  
#### [Twitter](https://twitter.com/TakeTakaAway/status/1744998645488070877)  
![1](images/0.png)  
###### これだけ
## コンタクト
↓Discordサーバー↓  
https://discord.gg/X5SNVYtRPR  
↑にてPayPayで寄付してくれると超嬉しいです！！
## このAPIラッパーをPayPay詐欺とかいうクソしょーもないことに使わないでください。
