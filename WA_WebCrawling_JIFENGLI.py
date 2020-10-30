#Crael data from Twitter
import tweepy
import csv

auth = tweepy.auth.OAuthHandler('z9RWirdb6Om1ineEQoRJws78c', '4c7LRooGsv7LQHcYYHArMo4B1Z8ogoep5zvtXLDH5Wqg5Q8TkC')
auth.set_access_token('1313537844284137475-Y6YKs98y7B9YIjADOufsOfvQqQiDlm', 'Jz0LWN7WaC4PQTBWLBIPDtswSNKWHN1K26U9dleG72SWK')

api = tweepy.API(auth)

def search_term(outputFile, term, limit):
    result = open(outputFile, 'a')
    csvWriter = csv.writer(result)
    csvWriter.writerow(["Screen Name", "Number of Followers", "Location", "Tweet"])
    try:
        i = 0
        for tweet in tweepy.Cursor(api.search,
                                    q = term,
                                    lang = "en").items(limit):

            csvWriter.writerow([tweet.user.screen_name,
                                tweet.user.followers_count,
                                tweet.user.location,
                                tweet.text.encode('utf-8')])
            i = i+1
        print(str(i)+" rows of data crawled from Twitter related to " + term)
        result.close()
    except:
        print("Waiting to crawl...")

search_term('Amazon.csv', 'Amazon', 200)
search_term('Walmart.csv', 'Walmart', 200)
search_term('Costco.csv', 'Costco', 200)

#Crawl reviews from yelp
from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd

preview=[]
review=[]
star=[]
id=[]

urls = ['https://www.yelp.com/biz/holey-cream-new-york?osq=ice+cream','https://www.yelp.com/biz/holey-cream-new-york?osq=ice%20cream&start=20','https://www.yelp.com/biz/holey-cream-new-york?osq=ice%20cream&start=40','https://www.yelp.com/biz/holey-cream-new-york?osq=ice%20cream&start=60','https://www.yelp.com/biz/holey-cream-new-york?osq=ice%20cream&start=80','https://www.yelp.com/biz/holey-cream-new-york?osq=ice%20cream&start=100']

for url in urls:
    ourUrl = urllib.request.urlopen(url)
    soup = BeautifulSoup(ourUrl,'html.parser')

    for i in soup.find_all('p',{'class':'lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'}):
        per_review=i.find('span')
        new_review=str(per_review).split('>')[1]
        new_review=new_review.split('<')[0]
        review.append(new_review)

    section= soup.find('ul',{'class':'lemon--ul__373c0__1_cxs undefined list__373c0__3GI_T'})
    for i in soup.find_all('div',{'class':'lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT arrange-unit-grid-column--8__373c0__2dUx_ border-color--default__373c0__3-ifU'}):
        per_star=i.find('div',{'class':'lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT border-color--default__373c0__3-ifU'})
        if per_star!= None:
            per_star=per_star.find('span')
            per_star=per_star.find('div')
            new_star=str(per_star).split('"')[1]
            new_star=new_star.split(' ')[0]
            star.append(int(new_star))

    section= soup.find('ul',{'class':'lemon--ul__373c0__1_cxs undefined list__373c0__3GI_T'})
    for i in soup.find_all('div',{'class':'lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT arrange-unit-grid-column--4__373c0__33Wpc border-color--default__373c0__3-ifU'}):
        pre_id=i.find('div',{'class':'lemon--div__373c0__1mboc border-color--default__373c0__3-ifU'})
        if pre_id != None:
            pre_id=pre_id.find('div',{'class':'lemon--div__373c0__1mboc user-passport-info border-color--default__373c0__3-ifU'})
            pid=pre_id.find('a')
            nid=str(pid).split('>')[1]
            nid=nid.split('<')[0]
            id.append(nid)

list=[id, star,review]
name=['reviewID', 'reviewRating', 'reviewText']
pro2=pd.DataFrame(index=name, data=list)
pro2=pro2.T
print(pro2)
pro2.to_csv('Review.csv',encoding='utf-8')

