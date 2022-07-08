import requests
import json
import re
import time
import subprocess
url = "http://10.254.7.4"
header = {
'Uip':'va5=1.2.3.4.'
}
#判断账号状态
def check_status(interface,url):
    resp = subprocess.check_output("mwan3 use {} curl -m 10 -s -X GET {}".format(interface,url),shell=True,encoding="GB2312")
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

def do_login(payload,url):
    print("try to login {} in on interface {}".format(payload['account'],payload['interface']))
    output = subprocess.check_output("mwan3 use {} python login_single.py {} {} {}".format(payload['interface'],payload['account'],payload['password'],payload['mobile']),shell=True,encoding="utf-8")
    result_regex = re.compile(r'^(result:)(.*)$',re.M)
    result = re.findall(result_regex,output)[0][1].strip()
    return result

data = [
	{
	    "enabled":True,
        "account":"20001122",
	    "password":"000000", 	# If there is ' in your password, you should manually escape
	    "mobile":"1", 				# mobile flag
	    "interface":"interface1" 		# Warning: this interface value should be interface name as used in mwan3, rather than alias in luci
	},
	{
        "enabled":True,  
        "account":"20001123",
        "password":"000000", 
        "mobile":"1",
        "interface":"interface1" 		
	}
]

while True:
    for payload in data:
        #print(payload)
        if payload['enabled']== True: 
            status = check_status(payload['interface'],url)
            if status == False:
                m = do_login(payload,url)
                print(m)
            else:
                print("[" + payload['interface'],end='] ')
                print(status[0],'Already log in',' ','Time:',status[1],' ','Meassure:',status[2],sep='')
        time.sleep(60)
exit()
