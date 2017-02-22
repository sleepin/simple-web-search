"simple-web-search"
from __future__ import print_function
import argparse
import time
import random
import requests
from bs4 import BeautifulSoup
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs



def main():
    """
    Run web search
    """
    parser = argparse.ArgumentParser(description='Search web')
    parser.add_argument('-x', '--engine',
                        default='GoogleWeb',
                        help="Available options: GoogleWeb (default) GoogleCSE")
    parser.add_argument('-q', '--query',
                        default='Python & R',
                        help="search query.")
    parser.add_argument('-k', '--key',
                        help="search engine CSE key")
    parser.add_argument('-i', '--id',
                        help="search engine CSE ID")

    options = parser.parse_args()

    if options.engine == 'GoogleCSE':
        if not (options.key and options.id):
            print("Please, specific Google CSE Key and Google CSE ID. "
                  "See https://cse.google.com/")
            return

        res = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={'key': options.key, 'cx': options.id, 'q': options.query}
        )
        for item in res.json()['items']:
            print(u"{}\t{}".format(item['title'], item['link']))
    elif options.engine == 'GoogleWeb':
        time.sleep(random.randint(2, 5))  # dont annoy google

        res = requests.get(
            "https://www.google.ru/search",
            params={'hl': 'en', 'q': options.query, 'btnG': 'Google Search'},
            headers={'User-Agent':
                     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}
        )
        soup = BeautifulSoup(res.content, 'html.parser')
        for item in soup.find(id='search').findAll('a'):
            # filter out Cached and Similar links
            if item.text not in ('Cached', 'Similar'):
                link = parse_qs(urlparse(item['href']).query)['q'][0]
                text = item.getText()
                print(u"{}\t{}".format(text, link))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
