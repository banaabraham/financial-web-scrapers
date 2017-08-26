import urllib
import re
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

class bloomberg(object):
    def __init__(self,query):
        self.query = query
        
    def get_page(self):
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
            self.news.append(str(re.findall('"body":.*"publishedAt"',i))\
                             .replace("body","").replace("publishedAt","")\
                             .replace("<em>","").replace("</em>",""))
        self.newsclean = []
        for i in self.news:
            self.newsclean.append((re.sub(r'\W+', ' ', i)))           
        return self.newsclean 
       
    
    def new(self):
        train = [('I love this sandwich.', 'pos'),
                ('This is an amazing place!', 'pos'),
                ('I feel very good about these beers.', 'pos'),
                ('This is my best work.', 'pos'),
                ("What an awesome view", 'pos'),
                ('I do not like this restaurant', 'neg'),
                ('I am tired of this stuff.', 'neg'),
                ("I can't deal with this", 'neg'),
                ('He is my sworn enemy!', 'neg'),
                ('My boss is horrible.', 'neg')]
        new = [i for i in self.newsclean]
        cl = NaiveBayesClassifier(train)
        if cl.classify(new[1]) == "neg":
            print("Cautions!")
            print(new[1])
        else:
            print("it's good")
            print(new[1])
                               
goog = bloomberg("google")
page = goog.get_page()
info = goog.get_info()
goog.new() 
