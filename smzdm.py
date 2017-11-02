import sys

import bs4
import requests

from common import const

if __name__ == '__main__':
    page_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 10
    top = int(sys.argv[2]) if len(sys.argv) >= 3 else 32
    infos = []
    for page in range(1, 11):
        response = requests.get('https://%s/p%d' % (const.DOMAIN_SMZDM, page),
                                headers=const.HEADERS)
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

            infos.append((up, '(%s/%s): %s(%s)' % (up, down, text, href)))

        print('Page %d of %d complete.' % (page, page_count))

    for info in sorted(infos, key=lambda item: -item[0])[0: top]:
        print(info[1])
