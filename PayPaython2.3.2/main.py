import requests
import datetime
import uuid

headers={
        "Accept":"application/json, text/plain, */*",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        "Content-Type":"application/json"
        }

class PayPayLoginError(Exception):
    pass
class PayPay:
    def __init__(self,phone:str=None,password:str=None,client_uuid:str=str(uuid.uuid4()),token:str=None,proxy:dict=None):
        self.session = requests.Session()
        self.proxy=proxy
        self.uuuid=client_uuid
        self.phone=phone
        self.pas=password
        if token==None:
            loginj = {
            "scope":"SIGN_IN",
            "client_uuid":self.uuuid,
            "grant_type":"password",
            "username":self.phone,
            "password":self.pas,
            "add_otp_prefix": True,
            "language":"ja"
            }

            login=self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token",json=loginj,headers=headers,proxies=proxy)
            try:
                self.token=(login.json()["access_token"])
            except:
                if login.json()["response_type"]=="ErrorResponse":
                    raise PayPayLoginError(login.json())
                else:
                    self.pre=login.json()["otp_prefix"]
                    self.refid=login.json()["otp_reference_id"]
        else:
            self.session.cookies.set("token",token)

    def login(self,otp:str):
        otpj = {
                "scope":"SIGN_IN",
                "client_uuid":self.uuuid,
                "grant_type":"otp",
                "otp_prefix": self.pre,
                "otp":otp,
                "otp_reference_id":self.refid,
                "username_type":"MOBILE",
                "language":"ja"
                }
        
        login=self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token",json=otpj,headers=headers,proxies=self.proxy)
        login1=login.json()
        login1.update({"client_uuid":str(self.uuuid)})
        return login1

    def resend_otp(self,otp_reference_id:str):
        resendj={
            "add_otp_prefix":"true"
        }
        resend=self.session.post(f"https://www.paypay.ne.jp/app/v1/otp/mobile/resend/{otp_reference_id}",json=resendj,headers=headers,proxies=self.proxy)
        try:
            self.pre=resend.json()["otp_prefix"]
            self.refid=resend.json()["otp_reference_id"]
        except:
            raise PayPayLoginError(resend.json())
        return resend.json()
    
    def balance(self) -> dict:
        balance=self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo",headers=headers,proxies=self.proxy)
        return balance.json()
    
    def user_info(self) -> dict:
        uinfo=self.session.get("https://www.paypay.ne.jp/app/v1/getUserProfile?",headers=headers,proxies=self.proxy)
        return uinfo.json()
    
    def display_info(self) -> dict:
        dinfo=self.session.get("https://www.paypay.ne.jp/app/v2/bff/getProfileDisplayInfo",headers=headers,proxies=self.proxy)
        return dinfo.json()
    
    def payment_method(self) -> dict:
        payment=self.session.get("https://www.paypay.ne.jp/app/v2/bff/getPaymentMethodList",headers=headers,proxies=self.proxy)
        return payment.json()
    
    def history(self) -> dict:
        history=self.session.get("https://www.paypay.ne.jp/app/v2/bff/getPay2BalanceHistory",headers=headers,proxies=self.proxy)
        return history.json()
    
    def create_link(self,kingaku:int,password:int=0) -> dict:
        clink = {
            "androidMinimumVersion": "3.45.0",
            "requestId": str(uuid.uuid4()),
            "requestAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900'),
            "theme": "default-sendmoney",
            "amount": kingaku,
            "iosMinimumVersion": "3.45.0"
            }

        if not password==0:
            clink["passcode"] = str(password)

        createlink = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/executeP2PSendMoneyLink",  headers=headers, json=clink,proxies=self.proxy)
        return createlink.json()
        
    def check_link(self,pcode:str) -> dict:
        info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={pcode}",headers=headers,proxies=self.proxy)
        return info.json()
    
    def receive(self,pcode:str,password:int=4602,info:dict=None) -> dict:
        if info==None:
            info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={pcode}",headers=headers,proxies=self.proxy).json()
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

        rece = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/acceptP2PSendMoneyLink",json=recevej,headers=headers,proxies=self.proxy)
        return rece.json()
    
    def reject(self,pcode:str,info:dict=None) -> dict:
        if info==None:
            info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={pcode}",headers=headers,proxies=self.proxy).json()
        rejectj = {
                "requestAt":datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900'),
                "orderId":info["payload"]["pendingP2PInfo"]["orderId"],
                "verificationCode":pcode,
                "requestId":str(uuid.uuid4()),
                "senderMessageId":info["payload"]["message"]["messageId"],
                "senderChannelUrl":info["payload"]["message"]["chatRoomId"],
                "iosMinimumVersion":"3.45.0",
                "androidMinimumVersion":"3.45.0",
                "client_uuid":self.uuuid
                }

        reje = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/rejectP2PSendMoneyLink",json=rejectj,headers=headers,proxies=self.proxy)
        return reje.json()
    
    def send_money(self,kingaku:int,external_id:str) -> dict:
        sendj = {
            "theme": "default-sendmoney",
            "externalReceiverId": external_id,
            "amount": kingaku,
            "requestId": str(uuid.uuid4()),
            "requestAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900'),
            "iosMinimumVersion":"3.45.0",
            "androidMinimumVersion":"3.45.0"
        }
        send = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/executeP2PSendMoney",headers=headers,json=sendj,proxies=self.proxy)
        return send.json()
    
    def create_p2pcode(self) -> dict:
        cp2c = self.session.post("https://www.paypay.ne.jp/app/v1/p2p-api/createP2PCode",headers=headers,proxies=self.proxy)
        return cp2c.json()
    
    def create_payment_otcfh(self) -> dict:
        cpotcj = {
            "paymentMethodType":"WALLET",
            "paymentMethodId":"106177237",
            "paymentCodeSessionId":str(uuid.uuid4()),
        }
        cpotc = self.session.post("https://www.paypay.ne.jp/app/v2/bff/createPaymentOneTimeCodeForHome",headers=headers,proxies=self.proxy,json=cpotcj)
        return cpotc.json()

class Pay2:
    def __init__(self,proxy:dict=None):
        self.proxy=proxy

    def check_link(self,pcode:str) -> dict:
        info=requests.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={pcode}",headers=headers,proxies=self.proxy)
        return info.json()