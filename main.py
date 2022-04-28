import os
import time
import pywifi
from pywifi import const
#获取本机ip地址
def get_local_ip(): 
    result = []
    ipv4 = None
    for x in os.popen('ipconfig'):
        result.append(x)
    for x in range(len(result)):
        if 'IPv4' in result[x] and result[x+2][-2] != ' ':
            ipv4 = result[x][result[x].find(':') + 2:-1]
    return ipv4
#判断是否在宿舍
def indorm():
    get_wifiname = []
    # 定义接口操作
    wifi = pywifi.PyWiFi()
    # 这里iface就是获取的wifi接口
    iface = wifi.interfaces()[0]
    # 扫描WiFi
    iface.scan()
    time.sleep(1)
    # 获取扫描的profiles文件
    scan_wifi = iface.scan_results()
    for i in scan_wifi:
        if i.ssid not in get_wifiname:
            get_wifiname.append(i.ssid)
    print(get_wifiname)
    if "scut-student" in get_wifiname:
        print("在宿舍！")
        return True
if indorm():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = pywifi.Profile()
    profile.ssid = "scut-student"
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)
    profile.cipher = const.CIPHER_TYPE_NONE
    while iface.status() in [const.IFACE_DISCONNECTED,const.IFACE_INACTIVE]:
        #iface.remove_all_network_profiles()
        tep_profile = iface.add_network_profile(profile)
        iface.connect(tep_profile)
    else:
        print("连接Wifi成功！正在查看是否需登录...")
        if os.system('ping 202.38.193.28 -n 1')==0:
            print("已登录！")
            os._exit(0)
        else:
            print("正在登录...")
            os.system('''curl "https://s.scut.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=************&user_password=******&wlan_user_ip='''+get_local_ip()+'''&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=172.18.255.250&wlan_ac_name=WX6108E-slot7-AC&jsVersion=4.1.3&terminal_type=1&lang=zh-cn&v=7189&lang=zh"   -H "Accept: */*"   -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"   -H "Connection: keep-alive"   -H "DNT: 1"   -H "Referer: https://s.scut.edu.cn/"   -H "Sec-Fetch-Dest: script"   -H "Sec-Fetch-Mode: no-cors"   -H "Sec-Fetch-Site: same-site"   -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50"''')
            os._exit(0)
