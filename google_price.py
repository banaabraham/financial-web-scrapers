import urllib
from yahoo_finance import Share
import re

class google_read(object):
    def __init__(self,stock):
        self.stock = stock
        
    def get_text(self):
        url = 'https://www.google.com/finance?q=IDX:'+self.stock
        hdr = {'User-Agent': 'Mozilla/5.0'}
        print (url)
        response = urllib.request.Request(url,headers=hdr)                                
        with urllib.request.urlopen(response) as f:
            self.page = f.read().decode('utf-8')
        
        return self.page.split('\n')   
    
    def read_price(self):
        #f = open(self.page,'r')
        f = self.page.split('\n')
        trigger = 0
        file = []
        #text = [x for x in f.readlines()]
        text = f
        for i in range(len(text)):
            if '<span class="pr">' in text[i]:
                trigger=1
            if trigger==1:
                file.append(text[i])
        c = re.findall(">.*<",str(file[1]))  
        if c:
            return float(str(c[0]).replace("<","").replace(">","").replace(",",""))
        
s = google_read('aapl')   
s.get_text()
page = s.read_price()
