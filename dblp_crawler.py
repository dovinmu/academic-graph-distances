'''
Crawls dblp, a bibliography of academic computer science publications with over 1.5 million authors.

Policy on web crawlers:
http://dblp.uni-trier.de/faq/Am+I+allowed+to+crawl+the+dblp+website.html

'''

import time
import random
from bs4 import BeautifulSoup
import requests
import sys

BASE_URL = 'http://dblp.uni-trier.de/pers/xc/'
start = 0
iters = 4
#limiter = 10000
names = {}
graph = {}
excludes = {'a/al=:et':'et al.'}

def crawl(verbose=False):
    with open('round_' + str(start)) as f:
        for line in f:
            if line.strip() != '':
                line = line.split(';')
                names[line[1].strip()] = line[0].strip()
                graph[line[0].strip()] = set()
                
    processing_nodes = [name for name in names.keys()]

    print('Starting round 1 of {} rounds'.format(iters))

    for n in range(start+1,iters+1):
    #while len(names) < limiter:
        newly_added = []
        i = 0
        for name_url in processing_nodes:
            author_name = names[name_url]      
            r = requests.get(BASE_URL + name_url)
            soup = BeautifulSoup(r.text)
            current_length = len(newly_added)
            for coauthor in soup.find_all('author'):
                coauthor_url = coauthor.get('urlpt')
                coauthor_name = coauthor.text
                if coauthor_url not in excludes:
                    if coauthor_url not in names:
                        names[coauthor_url] = coauthor_name
                        graph[coauthor_name] = set([author_name])
                        newly_added.append(coauthor_url)
                    graph[author_name].add(coauthor_name)
            i += 1
            if verbose:
                print('%d/%d. Added %d more names from author %s' % (i,len(processing_nodes),len(newly_added) - current_length, names[name_url]))
            else:
                print('{0}/{1}'.format(i, len(processing_nodes)), end='\r')
            time.sleep(2)
        
        if len(newly_added) > 0:
            with open('round_'+str(n),'w') as f:
                for author in newly_added:
                    f.write(names[author] + ' ; ' + author + '\n')
            with open('author_graph_round_'+str(n),'w') as f:
                for author in graph.keys():
                    s = author + ':'
                    for coauthor in graph[author]:
                        s += coauthor + ','
                    f.write(s + '\n')
        print('done with round %d, size of names: %d' % (n,len(names)))
        processing_nodes = [name for name in newly_added]




