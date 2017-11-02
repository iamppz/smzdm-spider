import ctypes
import re
import struct
import demjson
import os
import requests

from common import const

SPI_SETDESKWALLPAPER = 20


def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ


def get_sys_parameters_info():
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def setWallpaper(path):
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, path, 3)


if __name__ == '__main__':
    resp = requests.get('http://%s' % const.DOMAIN_BING, headers=const.HEADERS)
    pattern = re.compile('g_img={(.+?)}')
    match = pattern.search(resp.text)
    print('match group 0: ' + match.group(0))
    if match:
        json_str = match.group(0)[6:]
        print('json: %s' % json_str)
        json = demjson.decode(json_str)
        path = json['url']
        print('image: %s' % path)
        image = requests.get('http://%s%s' % (const.DOMAIN_BING, path)).content
        file_name = path[16:]
        with open(file_name, 'wb') as handler:
            handler.write(image)
        setWallpaper('c:/workspace/smzdm-spider/%s' % file_name)
