import requests
import bs4

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
    }
    for page in range(10):
        response = requests.get('https://www.smzdm.com/p%d' % page,
                                headers=headers)
        soup = bs4.BeautifulSoup(response.text)
        feeds = soup.select('.feed-block-title')
        for feed in feeds:
            print(feed.get_text())
