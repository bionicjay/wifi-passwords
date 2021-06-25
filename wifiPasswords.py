import subprocess as sb
import re


def get_wifi_passwords():
    profiles = sb.check_output('netsh wlan show profiles').decode('utf-8', 'backslashreplace')
    ssids = [res[2:-1] for res in re.findall(': .*\r', profiles)]
    profile_details = [sb.check_output(f'netsh wlan show profile {ssid} key=clear').decode('utf-8', 'backslashreplace') for ssid in ssids]
    pwd_sections = [re.findall('--+ \r\n.+?\r\n\r\n', pro_det, re.DOTALL)[-2] for pro_det in profile_details]
    passwords = [re.findall(': .+\r', pwd_section)[-1][2:-1] for pwd_section in pwd_sections]
    return dict(zip(ssids, passwords))


for key, value in get_wifi_passwords().items():
    print(f'{key}: {value}')
