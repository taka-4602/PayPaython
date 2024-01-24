import PayPaython

#ログイン
paypay=PayPaython.PayPay(phone="08012345678",password="Test-1234")#ログイン済みclient_uuid="str"をセットするとOTPをパスできます #token="str"トークンをセットするとログインをパスします
otp=input(f"SMSに届いた番号:{paypay.pre}-")
print(paypay.login(otp))#uuid確認用に["client_uuid"]にわざとuuidくっつけてます
#SMSの認証番号を再送
print(paypay.resend_otp(paypay.refid))#refidの使い道ができた
otp=input(f"SMSに届いた番号:{paypay.pre}-")#もっかい入力
print(paypay.login(otp))
#送金リンク確認
print(paypay.check_link("osuvUuLmQH8WA4kW"))#ぺいぺい送金リンクの https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW <-ここね
#送金リンク受け取り
print(paypay.receive("osuvUuLmQH8WA4kW"))#パスワードはpassword=int #事前にcheck_linkして返ってきたdictを引数infoに入れるとそのdictを使うようになります
#送金リンクを辞退
print(paypay.reject("osuvUuLmQH8WA4kW"))#これもinfoにdictつっこめる
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
print(paypay.send_money(kingaku=1,external_id="048f4fef00bdbad00"))#このidはてきとーです
#送金してもらうためのURLを作成する(PayPayアプリのQRコードとおなじ)
print(paypay.create_p2pcode())
#支払いのワンタイムコードを作成する
print(paypay.create_payment_otcfh())
