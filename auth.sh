#!/bin/sh
# curl script for scut-student
LOGGER=1
AUTO_PARAMS=1
username="xxxx"
password="xxxx"

ifname="apclii0"
userip_default="10.192.17.21"
wlanacip_default="192.168.66.187"
usermac_default="TY%1D%A0A%BD%B7%1C&g%8F"
det_ips="223.5.5.5 119.29.29.29"

get_params() {
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    response=$(curl -k -s --interface $ifname http://www.scut.edu.cn/ --user-agent "$user_agent" -w "%{redirect_url}" -o /dev/null)
    
    userip=$(echo "$response" | sed 's/.*userip=\([^&]*\).*/\1/')
    wlanacip=$(echo "$response" | sed 's/.*wlanacip=\([^&]*\).*/\1/')
    usermac=$(echo "$response" | sed 's/.*usermac=\([^&]*\).*/\1/')
}

for n in $det_ips
do
    /bin/ping -I "$ifname" -c 1 -W 2 "$n" >/dev/null 2>&1
    if [ "$?" = "0" ]; then
        exit 0
    fi
done

[ $LOGGER -eq 0 ] || logger -t "scut_auth" "Connection failed, restart auth"
if [ $AUTO_PARAMS -eq 0 ]; then
    userip=$userip_default
    wlanacip=$wlanacip_default
    usermac=$usermac_default
else
    get_params  # get_params function to get userip, wlanacip, usermac
fi

curl -k -s -o /dev/null --interface $ifname \
--url "https://s.scut.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=$username&user_password=$password&wlan_user_ip=$userip&wlan_user_ipv6=&wlan_user_mac=$$usermac_default&wlan_ac_ip=$wlanacip&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=zh-cn&v=8040&lang=zh:"