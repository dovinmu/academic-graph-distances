import sys
import requests
from bs4 import BeautifulSoup

import dblp_crawler
import famous_matcher

def crawl(url, verbose=False):
    with open("round_0", 'w') as f:
        r = requests.get(dblp_crawler.BASE_URL + url)
        soup = BeautifulSoup(r.text)
        name = soup.find('coauthors').get('author')
        f.write('{0} ; {1}'.format(name, url))

    dblp_crawler.crawl(verbose)
    famous_matcher.find_matches()

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4 or (len(sys.argv) == 2 and sys.argv[1] == '-v'):
        print('''
Usage:
  distances.py [options] <author 1>
    -v: Print the 
  Note: Authors need to be entered as actual (partial) URLs to avoid ambiguity. Example:
  >>> python distances.py k/Knuth:Donald_E= 

  This command will search the connection graph outwards from Donald Knuth for connections to other famous computer scientists (and some mathematicians).
        ''')
    elif len(sys.argv) == 2:
        crawl(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == '-v':
        crawl(sys.argv[2], True)
    else:
        print('Finding the distance between two authors not yet supported.')
