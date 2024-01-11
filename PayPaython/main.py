import requests
import json
import datetime
import uuid

class PayPay:
    def __init__(self,phone:str,password:str,client_uuid:str=None,proxy:dict=None):
        self.proxy=proxy
        self.session = requests.Session()
        if client_uuid==None:
            self.uuuid=str(uuid.uuid4())
        else:
            self.uuuid=client_uuid
        self.phone=phone
        self.pas=password
        self.headers={
        "Accept":"application/json, text/plain, */*",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        "Content-Type":"application/json"
        }
        self.json = {
        "scope":"SIGN_IN",
        "client_uuid":self.uuuid,
        "grant_type":"password",
        "username":self.phone,
        "password":self.pas,
        "add_otp_prefix": True,
        "language":"ja"
        }
        
        logingo=self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token",json=self.json,headers=self.headers,proxies=proxy)
        login=logingo.json()
        try:
            token=(login["access_token"])
            print("ログイン成功！")
        except:
            if login["response_type"]=="ErrorResponse":
                print("電話番号かパスワードがまちがっています")
                return
            else:
                pre=(login["otp_prefix"])
                otp = input(f"SMSに届いた番号:{pre}-")
                self.json1 = {
                            "scope":"SIGN_IN",
                            "client_uuid":self.uuuid,
                            "grant_type":"otp",
                            "otp_prefix": pre,
                            "otp":str(otp),
                            "otp_reference_id":login["otp_reference_id"],
                            "username_type":"MOBILE",
                            "language":"ja"
                        }
                logingo=self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token",json=self.json1,headers=self.headers,proxies=proxy)
                login=logingo.json()
                try:
                    if login["response_type"]=="ErrorResponse":
                        print("認証番号がまちがってます...")
                        return
                except:
                    None
                try:    
                    token=(login["access_token"])
                    print(f"ログイン成功！\nuuid: {self.uuuid}")
                except:
                    if login["response_type"]=="ErrorResponse":
                        return login
        
    def balance(self) -> dict:
        balance=self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo",headers=self.headers,proxies=self.proxy)
        return balance.json()
    
    def user_info(self) -> dict:
        uinfo=self.session.get("https://www.paypay.ne.jp/app/v1/getUserProfile?",headers=self.headers,proxies=self.proxy)
        return uinfo.json()
    
    def display_info(self) -> dict:
        dinfo=self.session.get("https://www.paypay.ne.jp/app/v2/bff/getProfileDisplayInfo",headers=self.headers,proxies=self.proxy)
        return dinfo.json()
    
    def payment_method(self) -> dict:
        payment=self.session.get("https://www.paypay.ne.jp/app/v2/bff/getPaymentMethodList",headers=self.headers,proxies=self.proxy)
        return payment.json()
    
    def history(self) -> dict:
        history=self.session.get("https://www.paypay.ne.jp/app/v2/bff/getPay2BalanceHistory",headers=self.headers,proxies=self.proxy)
        return history.json()
    
    def create_link(self,kingaku:int,password:int=0) -> dict:
        clink = {
        
            "androidMinimumVersion": "3.45.0",
            "requestId": str(uuid.uuid4())(),
            "requestAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900'),
            "theme": "default-sendmoney",
            "amount": kingaku,
            "iosMinimumVersion": "3.45.0"
        }

        if not password==0:
            clink["passcode"] = str(password)

        createlink = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/executeP2PSendMoneyLink",  headers=self.headers, json=clink,proxies=self.proxy)
        return createlink.json()
        
    def check_link(self,pcode:str) -> dict:
        info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={pcode}",headers=self.headers,proxies=self.proxy)
        return info.json()
    
    def receive(self,pcode:str,password:str="4602") -> dict:
        info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={pcode}",headers=self.headers,proxies=self.proxy)
        try:
            if (info["payload"]["orderStatus"]) == "SUCCESS":
                print("このリンクは受け取り済みです")
                return
            if info["payload"]["orderStatus"] =="REJECTED":
                print("このリンクは辞退済みです")
                return
            if (info["payload"]["pendingP2PInfo"]["isSetPasscode"])==True:
                password = input("パスワードを入力してください: ")
        except:
            print("このリンクは使用不可です")
            return
        recevej = {
            "verificationCode":pcode,
            "client_uuid":self.uuuid,
            "passcode":str(password),
            "requestAt":str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900')),
            "requestId":info["payload"]["message"]["data"]["requestId"],
            "orderId":info["payload"]["message"]["data"]["orderId"],
            "senderMessageId":info["payload"]["message"]["messageId"],
            "senderChannelUrl":info["payload"]["message"]["chatRoomId"],
            "iosMinimumVersion":"3.45.0",
            "androidMinimumVersion":"3.45.0"
            }

        rece = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/acceptP2PSendMoneyLink",json=recevej,headers=self.headers,proxies=self.proxy)
        return rece.json()
    
    def reject(self,pcode:str) -> dict:
        info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={pcode}",headers=self.headers,proxies=self.proxy)
        try:
            if (info["payload"]["orderStatus"]) == "SUCCESS":
                print("このリンクは受け取り済みです")
                return
            if info["payload"]["orderStatus"] =="REJECTED":
                print("このリンクはすでに辞退済みです")
                return
        except:
            print("このリンクは使用不可です")
            return
        rejectj = {"requestAt":datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900'),
                   "orderId":info["payload"]["pendingP2PInfo"]["orderId"],
                   "verificationCode":pcode,
                   "requestId":str(uuid.uuid4()),
                   "senderMessageId":info["payload"]["message"]["messageId"],
                   "senderChannelUrl":info["payload"]["message"]["chatRoomId"],
                   "iosMinimumVersion":"3.45.0",
                   "androidMinimumVersion":"3.45.0",
                   "client_uuid":self.uuuid}

        reje = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/rejectP2PSendMoneyLink",json=rejectj,headers=self.headers,proxies=self.proxy)
        return reje.json()
    
    def send_money(self,kingaku:int,externalid:str) -> dict:
        sendj = {
            "theme": "default-sendmoney",
            "externalReceiverId": externalid,
            "amount": kingaku,
            "requestId": str(uuid.uuid4()),
            "requestAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900'),
            "iosMinimumVersion":"3.45.0",
            "androidMinimumVersion":"3.45.0"
        }
        send = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/executeP2PSendMoney",headers=self.headers,json=sendj,proxies=self.proxy)
        return send.json()
    
    def create_p2pcode(self) -> dict:
        cp2c = self.session.post("https://www.paypay.ne.jp/app/v1/p2p-api/createP2PCode",headers=self.headers,proxies=self.proxy)
        return cp2c.json()
    
    def create_payment_otcfh(self) -> dict:
        cpotcj = {
            "paymentMethodType":"WALLET",
            "paymentMethodId":"106177237",
            "paymentCodeSessionId":str(uuid.uuid4()),
        }
        cpqr = self.session.post("https://www.paypay.ne.jp/app/v2/bff/createPaymentOneTimeCodeForHome",headers=self.headers,proxies=self.proxy,json=cpotcj)
        return cpqr.json()