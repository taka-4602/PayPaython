# PayPayレスポンス集
ハロー、takaです
PayPayで返ってくるレスポンスの例をここにまとめます
もしここに載っていないレスポンス受け取った方、レスポンス.jsonを添付してtakaまで連絡くれると非常に助かります！！  
## 注意：このドキュメントはまだ書きかけです
## ログイン時

```{'response_type': 'ErrorResponse', 'result_info': 
{'result_status': 'F', 'result_code_id': '01102004', 'result_code': 'INTERNAL_AUTH_INVALID_GRANT_ERROR', 'result_msg': 'Bad credentials'}}
電話番号 / パスワード```


{'response_type': 'ErrorResponse', 'result_info': 
{'result_status': 'F', 'result_code_id': '01102015', 'result_code': 'INVALID_AUTH_SEND_OTP_OVER_LIMIT_COUNT_BAD_REQUEST', 
'result_msg': '[400] during [POST] to [http://notification-sender-service/v1/sms/send/otp] [OtpSenderClient#sendOtpBySms(SendOtpBySmsRequest)]:
 [{"result_info":{"result_status":"F","result_code_id":"01810001","result_code":"BAD_REQUEST","result_msg":"over limit of send count."}}]'}}


{'response_type': 'ErrorResponse','result_info': 
{'result_status': 'F', 'result_code_id': '01101007', 'result_code': 'INTERNAL_COMMON_SIGN_IN_FRAU D_CHECK_ERROR', 'result_msg': 'IP_BLACKLIST'}}



ログイン時以外
{'header': 
{'resultCode': 'S9999', 'resultMessage': 'Specific Error with half sheet'}, 
'error': 
{'backendResultCode': '', 'displayErrorResponse': 
{'backendResultCode': '', 'iconUrl': 'https://image.paypay.ne.jp/error/app/caution.png', 'title': '現在ご利用を制限しています', 'description': '安心安全な決済サービスを維持するため\nご利用を制限させていただく場合があります\n詳細はヘルプページをご確認ください',
 'canCloseByOutsideTap': True, 'buttonList': 
 [{'title': 'ヘルプページを確認する', 'actionType': 'DEEPLINK', 'deeplink': 'paypay://embed?url=https://paypay.ne.jp/rd/support/help/c0088/', 
 'nativeAction': None, 'buttonType': 'BLUE', 'googleAnalyticsInfo': None}, 
 {'title': '閉じる', 'actionType': 'CLOSE', 'deeplink': None, 'nativeAction': None, 'buttonType': 'WHITE', 'googleAnalyticsInfo': None}]}}}
