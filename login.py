import requests
import json
import re
import fcntl
from requests_toolbelt.adapters.source import SourceAddressAdapter
url = "http://10.254.7.4"
header = {
'Uip':'va5=1.2.3.4.'
}
#判断账号状态
def check_status(url,header,interface): 
    for prefix in ('http://', 'https://'):
        session.mount(prefix, SocketOptionsAdapter(getlocal_ip(interface)))
    resp = session.get(url,headers=header)
    resp = requests.get(url,headers=header).text
    regex = re.compile(r'[\'](.*?)[\s+\']',re.S)
    uid = re.findall(r'uid=[\'0-9A-Za-z\s\u4e00-\u9fa5，.-]+',resp)
    if len(uid)==0 :
        return False
    uid = re.findall(regex,uid[0])[0].strip()
    flow = re.findall(r'flow=[\'0-9A-Za-z\s\u4e00-\u9fa5，.-]+',resp)
    flow = re.findall(regex,flow[0])[0].strip()
    time = re.findall(r'time=[\'0-9A-Za-z\s\u4e00-\u9fa5，.-]+',resp)
    time = re.findall(regex,time[0])[0].strip() + 'Min'
    flow = int(flow)
    messure = str(int((flow-flow%1024)/1024))+'.'+str(int((flow%1024*1000-flow%1024*1000%1024)/1024)) 
    messure = str((float(messure)/1024).__round__(3)) + 'Gb'
    return uid,time,messure
#字典
def get_status(msg,msga,else_msg):
    msg_status = {
        "15" : "登录成功",
        "14" : "注销成功",
        "11" : "本账号只能在指定地址使用",
        "10" : "密码修改成功",
        "09": "新密码与确认新密码不匹配,不能修改",
        "08": "本账号正在使用,不能修改",
        "07": "已登录,返回流量信息",
        "06": "System buffer full",
        "05": "本账号暂停使用",
        "04": "本账号费用超支或时长流量超过限制",
        "03" :"本账号只能在指定地址使用",
        "02": "该账号正在使用中，请您与网管联系"
    }
    msga_status = {
        'error0' : "本IP不允许Web方式登录",
        'error1' : "本账号不允许Web方式登录",
        'error2' : "本账号不允许修改密码",
        'userid error1' : "账号不存在",
        'userid error2' : "密码输入错误",
        'userid error3' : "密码输入错误",
        '本帐号已被强制注销，将被停用一段时间' : "密码错误次数达到限制,请在120s后重试"
    }
    if (else_msg != None) | (msg == '15') :
        return '登录成功'
    else:
        if msg != '01':
            if msg_status.get(msg) != None:
                return msg_status.get(msg)
            return "unknow msg" + msg
        else:
            if msga_status.get(msga) != None:
                return msga_status.get(msga)
            return "unknow msga" + msga
#多网卡支持
def get_local_ip(interface):
    #return netifaces.ifaddresses(interface)[ni.AF_INET][0]['addr'] #使用了netifaces库
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(interface[:15], 'utf-8'))
    )[20:24])

def do_login(payload,url,header):
    for prefix in ('http://', 'https://'):
        session.mount(prefix, SocketOptionsAdapter(getlocal_ip(payload['interface'])))
    status = check_status(url,header,payload['interface'])
    if status!=False:
        print(status[0],status[1],status[2],'已登录',sep=(','),end='')
        return status
    k = [{"DDDDD": payload['account'],"upass": payload['password'],"0MKKey":'0123456789', "R6":payload['mobile'] }]
    Response = requests.post(url,data=k,headers=header)
    res = Response.text
    #print(res)
    regex = re.compile(r'[\'](.*?)[\'.]',re.S)
    msga= re.findall(r'msga=[\'0-9A-Za-z\s\u4e00-\u9fa5，.]+',res)
    msga= re.findall(regex,msga[0])[0].strip()
    msg= re.findall(r'Msg=[0-9]+',res)[0].split('=')[1]
    else_msg = re.match(r'<div id="info" style="height:100px; padding-top:30px;" class="font1">您已经成功登录。<br>',res)
    result =  payload['username'] + ',' + payload['password'] + ',' + str(get_status(msg,msga,else_msg)) + '\n'
    return result

account = [
	{
		"enabled":True
        "account":"2018xxxx",
		"password":"233333", 	# If there is ' in your password, you should manually escape
		"mobile":"0", 				# mobile flag
		"interface":"wan0" 		# Warning: this interface value should be interface name as used in mwan3, rather than alias in luci
	},
	{
        "enabled":True  
        "account":"2018xxxx",
        "password":"233333", 
        "mobile":"0",
        "interface":"wan0" 		
	}
]
while True:
    for payload in account:
        if payload['enabled']== True and check_status(url,header,payload['interface']) == False
            m = do_login(payload,url,header)
            print(m)
            continue
        sleep(5)
exit()