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
PayPay().link_check("https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW")#link_checkはログインなしでも使うことができる
print(paypay.link_amount)#リンクの合計金額
print(paypay.link_money_light)#金額のマネーライト分
print(paypay.link_money)#金額のマネー分
print(paypay.link_has_password)#パスワードがあるなら True
print(paypay.link_chat_room_id)#チャットルームID リンク受け取ったらメッセージ送れるあれのID
print(paypay.link_status)#PENDING COMPLEATED REJECTED FAILED
print(paypay.link_order_id)
#paypay.link_nantoka で返されるのはリンクチェックしたものだけ

paypay.link_receive("ここもURL / IDどっちでもOK")#送金リンク受け取り、パスワードはpassword=str
paypay.link_receive("ここもURL / IDどっちでもOK",link_info=link_info)#link_info=dict、これを設定するとリンクチェックをスキップする
paypay.link_reject("ここもURL / IDどっちでもOK")#送金リンクを辞退、これもlink_infoにdictをつっこめる

paypay.get_balance()#残高確認
print(paypay.all_balance)#すべての残高
print(paypay.useable_balance)#すべての使用可能な残高
print(paypay.money_light)#もってるマネーライト
print(paypay.money)#もってるマネー
print(paypay.point)#もってるポイント

paypay.get_profile()#ユーザー情報を確認
print(paypay.name)#ユーザー名
print(paypay.external_user_id)#識別のためのユーザーID、自分で決められるやつとは違う
print(paypay.icon)#アイコンのURL

print(paypay.get_history())#取引履歴を確認

paypay.create_p2pcode()#送金してもらうためのURLを作成する(PayPayアプリのQRコードとおなじ)
print(paypay.created_p2pcode)#↑で作ったURL

paypay.create_paymentcode()#レジでスキャンする用のバーコードを生成、画像はアプリ内で処理されるからコードだけ生成してもよっぽど機材を持ってる人じゃない限り無意味、死に機能

paypay.create_link(amount=1,password="1111")#送金リンクを作成、パスワードはpassword=str...この機能は2024/3月下旬に使えなくなった (エンドポイントから削除された)
paypay.send_money(amount=1,external_id="048f4fef00bdbad00")#指定したexternalidのユーザーに直接送金...この機能は2024/3月下旬に使えなくなった (エンドポイントから削除された)