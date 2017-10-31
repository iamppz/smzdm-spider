import requests
import bs4

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
    }
    counter = 0
    for page in range(10):
        response = requests.get('https://www.smzdm.com/p%d' % page,
                                headers=headers)
        soup = bs4.BeautifulSoup(response.text)
        feeds = soup.select('.feed-row-wide')
        for feed in feeds:
            article_id = feed.attrs['articleid']
            if str(article_id).split('_')[0] != '3':
                continue

            title = feed.select('.feed-block-title')[0]
            counter += 1
            text = title.get_text()
            href = title.select('a')[0].attrs['href']
            up = feed.select('.price-btn-up .unvoted-wrap')[0].get_text()
            down = feed.select('.price-btn-down .unvoted-wrap')[0].get_text()
            print('%d(%s/%s): %s(%s)' % (counter,
                                         str(up).lstrip().rstrip(),
                                         down.lstrip().rstrip(),
                                         text,
                                         href))
