import requests
import re
import demjson

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
    }

    resp = requests.get('http://cn.bing.com', headers=headers)
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


