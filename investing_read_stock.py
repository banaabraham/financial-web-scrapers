# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:42:10 2017

@author: lenovo
"""

import urllib
from yahoo_finance import Share

class investing_read(object):
    def __init__(self,stock):
        self.stock = stock
        
    def get_text(self):
        s = Share(self.stock)
        name = s.get_name()
        name = name.replace(" ","-")
        print (name[:14])
        name = name[:14].lower()
        url = 'https://www.investing.com/equities/'+name+"-ratios"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        print (url)
        response = urllib.request.Request(url,headers=hdr)
        with urllib.request.urlopen(response) as f:
            self.page = f.read().decode('utf-8')
        
        return self.page.split('\n')   
    
    def read_text(self):
        #f = open(self.page,'r')
        f = self.page.split('\n')
        trigger = 0
        file = []
        #text = [x for x in f.readlines()]
        text = f
        for i in range(len(text)):
            if 'genTbl reportTbl' in text[i]:
                trigger=1
            if trigger==1:
                file.append(text[i])
        PE = file[21].strip().replace("<td>","").replace("</td>","")
        PPS = file[26].strip().replace("<td>","").replace("</td>","")
        PPB = file[41].strip().replace("<td>","").replace("</td>","")
        DIVY = file[367].strip().replace("<td>","").replace("</td>","").replace("%","")
        return PPS,PPB,DIVY,PE

s = investing_read('ggrm.jk')   
page=s.get_text()
try: 
    s.read_text()
except Exception as e:
    print (e)

   