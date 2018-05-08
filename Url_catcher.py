import requests, bs4
from selenium import webdriver
from time import sleep
from random import randint
#klasa URLCatcher opisuje obiekt, ktory bedzie laczyl sie do strony, ktorej
#adres jest podawany przy tworzeniu obiektu (url_to_analise). Metoda CatchUrls
#przeglada kolejne strony podanego urla (musi to byc url do paginowanej strony
#z artykulami) i wylawia z nich url'e do konkretnych artykulow.

# testowo - https://www.google.pl/search?q=nangar&num=100&safe=off&rlz=1C1JZAP_plPL741FR744&tbs=qdr:y&tbm=nws&start=0
# podstawiajac pod "nangar" powyzej mozna by bylo olac zabawe z suzkaniem w google, tylko szukac pod konkrety

class URLCatcher():

    def __init__(self, search_word):
        self.search_word = search_word.replace(' ','+')
        self.url_to_analise = 'https://www.google.pl/search?q=%s&num=100&safe=\
                        off&rlz=1C1JZAP_plPL741FR744&\
                        tbs=qdr:y&tbm=nws&tbs=cdr:1,cd_min:1/1/2018,cd_max:2/7/2018&start=' %self.search_word

    # metoda CatchUrlSel - lapie urle z pojedynczego url'a. Nie ma petli prze
    # wijajacej - sluzy glownie do skrobania z googla
    def CatchUrlSel(self,soup_command):
        url_list = list()
        browser = webdriver.Firefox()
        url = self.url_to_analise
        browser.get(url)
        soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
        for link in soup.select(soup_command):
            url_list.append(link.get('href'))
        return url_list

    def CatchUrlsSel(self,no_of_links,step, soup_command):
        url_list = list()
        browser = webdriver.Firefox()
        for i in xrange(1,no_of_links,step):
            url = self.url_to_analise + str(i)
            print (url[-2:0])
            browser.get(url)
            soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
            sleep(randint(4,6))
            for link in soup.select(soup_command):
                url_list.append(link.get('href'))
        return url_list

    def CatchUrlsReq(self,no_of_links,step,soup_command):
        url_list = list() #tworze liste url ktora bede zwracal
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                    (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
                    # I just used a general Chrome 41 user agent header
        for i in xrange(0,no_of_links,step): #petla przegladajaca strony z artami
            url = self.url_to_analise + str(i)
            res = requests.get(url, headers = headers)
            res.raise_for_status()
            self.soup = bs4.BeautifulSoup(res.text, 'html.parser')
            for link in self.soup.select(soup_command): #petla lapiaca url #a[class="clearfix pad"]
                url_list.append(link.get('href'))
        return url_list
