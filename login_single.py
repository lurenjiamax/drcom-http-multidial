import requests
import json
import re
import sys
from huxi_status import get_status

username = sys.argv[1]
password = sys.argv[2]
R6 = sys.argv[3]
url = "http://10.254.7.4"
header = {
'Uip':'va5=1.2.3.4.'
}
regex = re.compile(r'[\'](.*?)[\'.]',re.S)
def do_single_login(username,password,R6):
    k = {"DDDDD": username ,"upass": password ,"0MKKey":'0123456789', "R6": R6 }
    Response = requests.post(url,data=k,headers=header)
    res = Response.text
    msga= re.findall(r'msga=[\'0-9A-Za-z\s\u4e00-\u9fa5，.]+',res)
    else_msg = re.search(r'您已经成功登录',res)
    msg=''
    if else_msg==None:
        msga= re.findall(regex,msga[0])[0].strip()
        msg= re.findall(r'Msg=[0-9]+',res)[0].split('=')[1]
    result = "result:"+ username + ','  + str(get_status(msg,msga,else_msg)) + ',' + R6
    return result
result=do_single_login(username,password,R6)
print(result)