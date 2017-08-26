import urllib
import re
import pandas as pd
from textblob import TextBlob
class bloomberg(object):
    def __init__(self,query):
        self.query = query
        
    def get_text(self):
        url = 'https://www.bloomberg.com/search?query='+self.query
        hdr = {'User-Agent': 'Mozilla/5.0'}
        #print (url)
        response = urllib.request.Request(url,headers=hdr)                                
        with urllib.request.urlopen(response) as f:
            self.page = f.read().decode('utf-8')
        
        return self.page.split('\n')
    
    def get_info(self):
        page = self.page.split('\n')
        for i in range(len(page)):
            if "storyType" in page[i]:
                pertinent = page[i]
        info = pertinent.split("storyType")
        self.news = []
        
        for i in info:
            self.news.append(str(re.findall('"body":.*"publishedAt"',i)).replace("body","").replace("publishedAt",""))
        self.newsclean = []
        for i in self.news:
            self.newsclean.append((re.sub(r'\W+', ' ', i)))           
        return self.newsclean        
    def analyze(self):
        for i in self.newsclean:
            negative = 0        
            blob = TextBlob(i).sentiment
            if blob.polarity<0:
                print(i)
                negative+=1           
        if negative>0:
            print("Cautions!")
                        
        
goog = bloomberg("exxon")
page = goog.get_text()
info = goog.get_info()    
sentiment = goog.analyze()
