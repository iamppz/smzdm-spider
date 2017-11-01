import requests
import re
import demjson
from common import const

if __name__ == '__main__':
    resp = requests.get('http://cn.bing.com', headers=const.HEADERS)
    pattern = re.compile('g_img={(.+?)}')
    match = pattern.search(resp.text)
    print('match group 0: ' + match.group(0))
    if match:
        json_str = match.group(0)[6:]
        print('json: %s' % json_str)
        json = demjson.decode(json_str)
        path = json['url']
        print('image: %s' % path)
        image = requests.get('http://cn.bing.com%s' % path).content
        with open(path[16:], 'wb') as handler:
            handler.write(image)


