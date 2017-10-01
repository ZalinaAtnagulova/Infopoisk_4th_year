import requests
from bs4 import BeautifulSoup
from IPython.display import HTML, display
import re

def main(url):
    req = requests.get(url)
    txt = []
    articles_links = []
    pages_links = []
    sections = reqsts(req, 'td', {'id':'mn'})
    
    for section in sections:
        articles_links.extend(reqsts(requests.get(section), 'div', {'id':'s3d'}))
        pages_links = reqsts(requests.get(section), 'div', {'style':'padding:10px 0 15px 0;'})
        articles_links.extend(reqsts(requests.get(pages_links[0]), 'div', {'id':'s3d'}))

    f = open('Corpora.txt', 'w', encoding = 'utf-8')
    for article_link in articles_links:
        f.write(article_data(requests.get(article_link), link = article_link))
    f.close()
    
    return

def reqsts(req, tag, attr):
    soup = BeautifulSoup(req.text, 'lxml')
    final_link = []
    for i, h in enumerate(soup.findAll(tag, attrs = attr)):
        link = h.findAll('a')
        if link:
            for a in link:
                if url + a['href'] not  in final_link:
                    final_link.append(url + a['href'])
    return final_link

def article_data(article, link):
    author = '@au Noname\n'
    title = '@ti '
    date = '@da '
    topic = '@topic '
    url = '@url '
    text = ''
    a = []
    months = {'января':'01', 'февраля':'02', 'марта':'03', 'апреля':'04', 'мая':'05', 'июня':'06', 'июля':'07',
              'августа':'08', 'сентября':'09', 'октября':'10', 'ноября':'11', 'декабря':'12'}
    
    topics = {'politics':'ПОЛИТИКА', 'economy':'ЭКОНОМИКА', 'society':'ОБЩЕСТВО', 'incidents':'ПРОИСШЕСТВИЯ',
              'afish':'КУЛЬТУРА', 'sport':'СПОРТ', 'media':'МЕДИА', 'world':'В МИРЕ',
              'auto':'АВТО', 'tech':'ТЕХНОЛОГИИ'}
    
    soup = BeautifulSoup(article.text, 'lxml')
    for i, h in enumerate(soup.find('h1')):
        title = title+str(h)+'\n'
        
    for i, h in enumerate(soup.find('div', {'class':'sgray'})):
        a.append(h)
    original_date = re.sub('\,(.*)', '', a[0])
    original_date = original_date.split()
    if original_date[1] in months:
        original_date[1] = months[original_date[1]]
    date = date+'.'.join(original_date)+'\n'

    for key in topics.keys():
        if key in link:
            topic = topic+topics[key]+'\n'

    url = url+str(link)+'\n'

    for i, h in enumerate(soup.findAll('div', {'style':'float:left;margin:5px 20px 10px 0;width:300px;'})):
        for a in h.next_siblings:
            if len(a) > 1:
                text += str(a).strip(' ') + '\n'
    return author+title+date+topic+url+text
    
url = 'http://briansk.ru/'
main(url)
