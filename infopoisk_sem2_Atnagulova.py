import requests
from bs4 import BeautifulSoup
from IPython.display import HTML, display

def crouler(url):
    req = requests.get(url)
    p1 = reqsts(req, 'p', {'style':'text-align:center; font-size:94%; margin-top:0'})
    p2 = reqsts(requests.get(p1[0]), 'tr', {'class':'mw-statistics-articles'})
    p3 = reqsts2(requests.get(p2[0]), 'ul', {'class':'mw-allpages-chunk'})
    return p3
          
def reqsts(req, tag, attr):
    soup = BeautifulSoup(req.text, 'lxml')
    final_link = []
    for i, h in enumerate(soup.findAll(tag, attrs = attr)):
        link = h.findAll('a')
        if link:
            for a in link:
                if 'Special' in a['href']:
                    final_link.append(url + a['href'])
    return final_link

def reqsts2(req, tag, attr):
    soup = BeautifulSoup(req.text, 'lxml')
    final_link = []
    for i, h in enumerate(soup.findAll(tag, attrs = attr)):
        link = h.findAll('a')
        if link:
            for a in link:
                final_link.append(url + a['href'])
    return final_link

url = 'http://mo.wikipedia.org'
crouler(url)
