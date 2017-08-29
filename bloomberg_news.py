import urllib
import re
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

class bloomberg(object):
    def __init__(self,query):
        self.query = urllib.parse.quote(query)
        
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
                ('My boss is horrible.', 'neg'),
                ('Wells Fargo shares slipped 3% in extended trading on Tuesday before recovering.','neg'),
                ('Brace for more negative news from Wells Fargo','neg'),
                ('Harvey makes landfall as Cat 4; gas price hikes to depend on flooding damage','neg'),
                ('Trucking stocks ride higher','pos'),
                ('Stocks Drop, Gold Leads Havens After Korea Missile: Markets Wrap','neg')]
        new = [i for i in self.newsclean]
        cl = NaiveBayesClassifier(train)
        if cl.classify(new[1]) == "neg":
            print("Cautions! \n")
            print(new[1])
        else:
            print("it's good news!")
            print(new[1])

query = input("What do you looking for?: ")                               
info = bloomberg(query)
page = info.get_page()
info = info.get_info()
info.new()   
