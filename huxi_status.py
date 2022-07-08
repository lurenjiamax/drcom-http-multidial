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
