import os
def get_local_ip():    #获取本机ip地址
    result = []
    ipv4 = None
    for x in os.popen('ipconfig'):
        result.append(x)
    for x in range(len(result)):
        if 'IPv4' in result[x] and result[x+2][-2] != ' ':
            ipv4 = result[x][result[x].find(':') + 2:-1]
    return ipv4
exit_code = os.system('ping 202.38.193.28 -n 1')    #判断是否连接成功
if exit_code==0:
    os._exit(0)
else:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.action_chains import ActionChains
    driver = webdriver.Edge(service=Service(r""))   #填上Edge驱动路径
    driver.get("https://s.scut.edu.cn/a79.htm?source-address="+str(get_local_ip())+"&wlanacname=WX6108E-slot7-AC&ssid=scut-student&wlanacip=172.18.255.250&source-mac=")
    #source-mac=后面上填本机MAC地址
    get_local_ip()
    element_1 = driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/form/input[2]")
    element_1.send_keys("")     #填上账号
    element_2 = driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/form/input[3]")
    element_2.send_keys("")     #填上密码
    above = driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/form/input[1]")
    driver.execute_script("arguments[0].click();", above)
    from time import sleep
    sleep(0.4)
    driver.quit()
