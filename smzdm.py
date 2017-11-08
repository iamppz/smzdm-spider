import sys

import bs4
import requests
from multiprocessing.dummy import Pool as ThreadPool

from common import const


def get_info(url):
    result = []
    response = requests.get(url, headers=const.HEADERS)
    soup = bs4.BeautifulSoup(response.text)
    feeds = soup.select('.feed-row-wide')
    for feed in feeds:
        article_id = feed.attrs['articleid']
        if str(article_id).split('_')[0] != '3':
            continue

        title = feed.select('.feed-block-title')[0]
        text = title.get_text()
        href = title.select('a')[0].attrs['href']
        up = int(feed.select('.price-btn-up .unvoted-wrap')[0]
                 .get_text().lstrip().rstrip())
        down = int(feed.select('.price-btn-down .unvoted-wrap')[0]
                   .get_text().lstrip().rstrip())
        if up == 0 or up < down:
            continue

        result.append((up, '(%s/%s): %s(%s)' % (up, down, text, href)))
    print('fetch complete: %s' % url)
    return result


if __name__ == '__main__':
    page_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 8
    top = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    keyword = sys.argv[3] if len(sys.argv) >= 4 else ''
    pool = ThreadPool(8)
    results = pool.map(lambda page: get_info('https://%s/p%d' % (const.DOMAIN, page)),
                       range(1, page_count + 1))
    infos = [item for sublist in results for item in sublist]

    for info in sorted(infos, key=lambda item: -item[0])[0: top]:
        if keyword not in info[1]:
            continue

        print(info[1])
