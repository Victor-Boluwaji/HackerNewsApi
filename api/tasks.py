from operator import imod
from urllib import response
from celery import shared_task
from .models import HackerNews
import requests
import json

@shared_task(bind=True)
def do(self):
    NEWS_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty' # external endpoint that returns list of ids
    
    headers = {'user-agent': 'quickcheck/0.0.1'}
    response = requests.get(NEWS_URL, headers=headers)

    result = response.text.split(',')[1:len(response.text.split(','))-2] # in order to trim the last element
    last = response.text.split(',')[-1] # got this from API " 499287535 ] /n" --> reshaped to that below
    result.insert(len(result), last.strip().split()[0]) # "499287535"

    news = 400 # 100 downward/latest
    res = [int(id.strip()) for id in result[news+1:news+100]] # list comprehension

    for id in res:
        NEWS_URL = f'https://hacker-news.firebaseio.com/v0/item/{str(id)}.json?print=pretty'
        response = requests.get(NEWS_URL)
        data = json.loads(response.text)
        result.append(data)
        hackernewsid = id        
        by = data.get('by')
        category = data.get('type')
        title = data.get('title')
        text = data.get('text')
        kids = data.get('kids')
        urls = data.get('url')
        news=HackerNews(by=by,category=category, title=title, hackernewsid=hackernewsid, kids=kids, urls=urls)
        news.save()
        

