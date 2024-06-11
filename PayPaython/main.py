import requests
import datetime
from uuid import uuid4

headers={
    "Accept":"application/json, text/plain, */*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    "Content-Type":"application/json"
}

class PayPayError(Exception):
    pass
class PayPayNetWorkError(Exception):
    pass
class PayPayLoginError(Exception):
    pass
class NetWorkError(Exception):
    pass
class PayPay:
    def __init__(self,phone:str=None,password:str=None,client_uuid:str=str(uuid4()).upper(),access_token:str=None,proxy:dict=None):
        self.session = requests.Session()
        self.proxy=proxy
        self.client_uuid=client_uuid
        self.phone=phone
        self.password=password
        if access_token:
            self.session.cookies.set("token",access_token)
        else:
            self.access_token=None
            payload = {
                "scope":"SIGN_IN",
                "client_uuid":self.client_uuid,
                "grant_type":"password",
                "username":self.phone,
                "password":self.password,
                "add_otp_prefix": True,
                "language":"ja"
            }
            try:
                login=self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token",json=payload,headers=headers,proxies=proxy)
            except Exception as e:
                raise NetWorkError(e)
            try:
                self.access_token=(login.json()["access_token"])
            except:
                try:
                    if login.json()["response_type"]=="ErrorResponse":
                        raise PayPayLoginError(login.json())
                    else:
                        self.otp_prefix=login.json()["otp_prefix"]
                        self.otp_reference_id=login.json()["otp_reference_id"]
                except:
                    raise PayPayNetWorkError(login.text)

    def login(self,otp:str):
        payload = {
            "scope":"SIGN_IN",
            "client_uuid":self.client_uuid,
            "grant_type":"otp",
            "otp_prefix": self.otp_prefix,
            "otp":otp,
            "otp_reference_id":self.otp_reference_id,
            "username_type":"MOBILE",
            "language":"ja"
        }
        
        login=self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token",json=payload,headers=headers,proxies=self.proxy).json()
        try:
            self.access_token=(login["access_token"])
        except:
            raise PayPayLoginError(login)
        
        return login

    def resend_otp(self,otp_reference_id:str):
        payload={
            "add_otp_prefix":"true"
        }
        resend=self.session.post(f"https://www.paypay.ne.jp/app/v1/otp/mobile/resend/{otp_reference_id}",json=payload,headers=headers,proxies=self.proxy).json()
    
        try:
            self.otp_prefix=resend["otp_prefix"]
            self.otp_reference_id=resend["otp_reference_id"]
        except:
            raise PayPayLoginError(resend)
        
        return resend
    
    def get_balance(self) -> dict:
        if not self.access_token:
            raise PayPayLoginError("まずはログインしてください")
        
        balance=self.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo",headers=headers,proxies=self.proxy).json()
        if balance["header"]["resultCode"] == "S0001":
            raise PayPayLoginError(balance)
        
        if balance["header"]["resultCode"] != "S0000":
            raise PayPayError(balance)

        self.money=balance["payload"]["walletDetail"]["emoneyBalanceInfo"]["balance"]
        self.money_light=balance["payload"]["walletDetail"]["prepaidBalanceInfo"]["balance"]
        self.all_balance=balance["payload"]["walletSummary"]["allTotalBalanceInfo"]["balance"]
        self.useable_balance=balance["payload"]["walletSummary"]["usableBalanceInfoWithoutCashback"]["balance"]
        self.point=balance["payload"]["walletDetail"]["cashBackBalanceInfo"]["balance"]

        return balance
    
    def get_profile(self) -> dict:
        if not self.access_token:
            raise PayPayLoginError("まずはログインしてください")
        
        profile=self.session.get("https://www.paypay.ne.jp/app/v1/getUserProfile",headers=headers,proxies=self.proxy).json()

        if profile["header"]["resultCode"] == "S0001":
            raise PayPayLoginError(profile)

        if profile["header"]["resultCode"] != "S0000":
            raise PayPayError(profile)
        
        self.name=profile["payload"]["userProfile"]["nickName"]
        self.external_user_id=profile["payload"]["userProfile"]["externalUserId"]
        self.icon=profile["payload"]["userProfile"]["avatarImageUrl"]

        return profile
    
    def get_history(self) -> dict:
        if not self.access_token:
            raise PayPayLoginError("まずはログインしてください")
        
        history=self.session.get("https://www.paypay.ne.jp/app/v2/bff/getPay2BalanceHistory",headers=headers,proxies=self.proxy).json()
        if history["header"]["resultCode"] == "S0001":
            raise PayPayLoginError(history)
        
        if history["header"]["resultCode"] != "S0000":
            raise PayPayError(history)
        
        return history
        
    def link_check(self,url:str) -> dict:
        if "https://" in url:
            url=url.replace("https://pay.paypay.ne.jp/","")

        param={
            "verificationCode":url
        }
        link_info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo",headers=headers,params=param,proxies=self.proxy).json()
        
        if link_info["header"]["resultCode"] != "S0000":
            raise PayPayError(link_info)
        
        self.link_sender_name=link_info["payload"]["sender"]["displayName"]
        self.link_sender_external_id=link_info["payload"]["sender"]["externalId"]
        self.link_sender_icon=link_info["payload"]["sender"]["photoUrl"]
        self.link_order_id=link_info["payload"]["pendingP2PInfo"]["orderId"]
        self.link_chat_room_id=link_info["payload"]["message"]["chatRoomId"]
        self.link_amount=link_info["payload"]["pendingP2PInfo"]["amount"]
        self.link_status=link_info["payload"]["message"]["data"]["status"]
        self.link_money_light=link_info["payload"]["message"]["data"]["subWalletSplit"]["senderPrepaidAmount"]
        self.link_money=link_info["payload"]["message"]["data"]["subWalletSplit"]["senderEmoneyAmount"]
        self.link_has_password=link_info["payload"]["pendingP2PInfo"]["isSetPasscode"]

        return link_info
    
    def link_receive(self,url:str,password:str=None,link_info:dict=None) -> dict:
        if not self.access_token:
            raise PayPayLoginError("まずはログインしてください")
        
        if "https://" in url:
            url=url.replace("https://pay.paypay.ne.jp/","")
        
        if not link_info:
            param={
                "verificationCode":url
            }
            link_info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo",headers=headers,params=param,proxies=self.proxy).json()
            if link_info["header"]["resultCode"] != "S0000":
                raise PayPayError(link_info)
        
        if link_info["payload"]["orderStatus"] != "PENDING":
            raise PayPayError("すでに 受け取り / 辞退 / キャンセル されているリンクです")
        
        if link_info["payload"]["pendingP2PInfo"]["isSetPasscode"] and password==None:
            raise PayPayError("このリンクにはパスワードが設定されています")
        
        payload = {
            "verificationCode":url,
            "client_uuid":self.client_uuid,
            "requestAt":str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900')),
            "requestId":link_info["payload"]["message"]["data"]["requestId"],
            "orderId":link_info["payload"]["message"]["data"]["orderId"],
            "senderMessageId":link_info["payload"]["message"]["messageId"],
            "senderChannelUrl":link_info["payload"]["message"]["chatRoomId"],
            "iosMinimumVersion":"3.45.0",
            "androidMinimumVersion":"3.45.0"
            }
        
        if password:
            payload["passcode"]=password

        receive = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/acceptP2PSendMoneyLink",json=payload,headers=headers,proxies=self.proxy).json()
        if receive["header"]["resultCode"] == "S0001":
            raise PayPayLoginError(receive)
        
        if receive["header"]["resultCode"] != "S0000":
            raise PayPayError(receive)
        
        return receive
    
    def link_reject(self,url:str,link_info:dict=None) -> dict:
        if not self.access_token:
            raise PayPayLoginError("まずはログインしてください")
        
        if not link_info:
            param={
                "verificationCode":url
            }
            link_info=self.session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo",headers=headers,params=param,proxies=self.proxy).json()
            if link_info["header"]["resultCode"] != "S0000":
                raise PayPayError(link_info)

        if link_info["payload"]["orderStatus"] != "PENDING":
            raise PayPayError("すでに 受け取り / 辞退 / キャンセル されているリンクです")

        payload = {
            "requestAt":datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M:%S+0900'),
            "orderId":link_info["payload"]["pendingP2PInfo"]["orderId"],
            "verificationCode":url,
            "requestId":str(uuid4()).upper(),
            "senderMessageId":link_info["payload"]["message"]["messageId"],
            "senderChannelUrl":link_info["payload"]["message"]["chatRoomId"],
            "iosMinimumVersion":"3.45.0",
            "androidMinimumVersion":"3.45.0",
            "client_uuid":self.client_uuid
        }

        reject = self.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/rejectP2PSendMoneyLink",json=payload,headers=headers,proxies=self.proxy).json()
        if reject["header"]["resultCode"] == "S0001":
            raise PayPayLoginError(reject)

        if reject["header"]["resultCode"] != "S0000":
            raise PayPayError(reject)
        
        return reject
    
    def create_p2pcode(self) -> dict:
        if not self.access_token:
            raise PayPayLoginError("まずはログインしてください")
        
        p2pcode = self.session.post("https://www.paypay.ne.jp/app/v1/p2p-api/createP2PCode",headers=headers,proxies=self.proxy).json()
        if p2pcode["header"]["resultCode"] == "S0001":
            raise PayPayLoginError(p2pcode)
        
        if p2pcode["header"]["resultCode"] != "S0000":
            raise PayPayError(p2pcode)
        
        self.created_p2pcode=p2pcode["payload"]["p2pCode"]

        return p2pcode
    
    def create_paymentcode(self,method:str="WALLET",method_id:str="106177237") -> dict:
        if not self.access_token:
            raise PayPayLoginError("まずはログインしてください")
        
        payload = {
            "paymentMethodType":method,
            "paymentMethodId":method_id,
            "paymentCodeSessionId":str(uuid4()),
        }
        paymentcode = self.session.post("https://www.paypay.ne.jp/app/v2/bff/createPaymentOneTimeCodeForHome",headers=headers,proxies=self.proxy,json=payload).json()
        if paymentcode["header"]["resultCode"] == "S0001":
            raise PayPayLoginError(paymentcode)
        
        if paymentcode["header"]["resultCode"] != "S0000":
            raise PayPayError(paymentcode)
        
        return paymentcode
    
    def create_link(self,amount:int,password:str=None) -> None:
        raise PayPayError("404 Not Found")
    def send_money(self,amount:int,external_id:str) -> None:
        raise PayPayError("404 Not Found")