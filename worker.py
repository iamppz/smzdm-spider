import sys
import requests
import bs4

if __name__ == '__main__':
    page_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 10

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
    }
    counter = 0
    for page in range(page_count):
        response = requests.get('https://www.smzdm.com/p%d' % page,
                                headers=headers)
        soup = bs4.BeautifulSoup(response.text)
        feeds = soup.select('.feed-row-wide')
        for feed in feeds:
            counter += 1

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

            print('%d(%s/%s): %s(%s)' % (counter, up, down, text, href))
