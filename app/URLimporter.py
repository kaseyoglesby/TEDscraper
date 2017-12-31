import sys, json, pymongo, time
from pymongo import MongoClient
from bson import json_util
from urllib.request import urlopen
from flask import Flask, request, redirect, render_template
from bs4 import BeautifulSoup

client = MongoClient()
db = client.TEDtalks
talks = db.talks

def ImportURL(rawURL):
    urlid = rawURL[(rawURL.rfind('/')+1):]
    results = (talks.find({"id" : urlid}))
    if not results.count():
        transcriptURL = rawURL + "/transcript.json"
        response = urlopen(transcriptURL)
        data = json_util.loads(response.read())

        rawHTML = urlopen(rawURL)
        soup = BeautifulSoup(rawHTML, 'html.parser')
        title = soup.head.title.getText()
        data['title'] = title[(title.index(':')+1):title.index('|')].strip()
        data['author'] = title[:title.index(':')]
        data['id'] = urlid

        result = talks.insert_one(data)
        return True
    return False
