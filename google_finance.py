import urllib
import re
import time
import pandas as pd

class google_read(object):
    def __init__(self,stock):
        self.stock = stock
        
    def get_page(self):
        url = 'https://www.google.com/finance?q=IDX:'+self.stock
        hdr = {'User-Agent': 'Mozilla/5.0'}
        #print (url)
        response = urllib.request.Request(url,headers=hdr)                                
        with urllib.request.urlopen(response) as f:
            self.page = f.read().decode('utf-8')
        
        return self.page.split('\n')   
    
    def get_price(self):
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
    def get_pe_ratio(self):
        f = self.page.split('\n')
        trigger = 0
        file = []
        #text = [x for x in f.readlines()]
        text = f
        for i in range(len(text)):
            if ' data-snapfield="pe_ratio">P/E' in text[i]:
                trigger=1
            if trigger==1:
                file.append(text[i])
        c = re.findall(">.*",str(file[2]))  
        if c:
            return c[0].replace(">","")

    def get_eps(self):
        f = self.page.split('\n')
        trigger = 0
        file = []
        #text = [x for x in f.readlines()]
        text = f
        for i in range(len(text)):
            if 'data-snapfield="eps">EPS' in text[i]:
                trigger=1
            if trigger==1:
                file.append(text[i])
        c = re.findall(">.*",str(file[2]))  
        if c:
            return c[0].replace(">","")
            
    def get_div_yield(self):
        f = self.page.split('\n')
        trigger = 0
        file = []
        #text = [x for x in f.readlines()]
        text = f
        for i in range(len(text)):
            if 'data-snapfield="latest_dividend-dividend_yield">Div/yield' in text[i]:
                trigger=1
            if trigger==1:
                file.append(text[i])
        c = re.findall(">.*",str(file[2]))  
        if c:
            return c[0].replace(">","")
        
       
           
        
if __name__ == "__main__":   
    s = google_read('ggrm')
    waktu = time.asctime()
    page = s.get_text()
    eps = s.get_eps()
    divy = s.get_div_yield()
    price = s.get_price()
    pe = s.get_pe_ratio()
    print ("%.2f at %s" %(price,waktu))
