import sys, json, pymongo, time
from pymongo import MongoClient
from bson import json_util
from urllib.request import urlopen
from flask import Flask, request, redirect, render_template
from bs4 import BeautifulSoup
from URLimporter import ImportURL

app = Flask(__name__)
client = MongoClient()
db = client.TEDtalks
talks = db.talks

@app.route('/', methods=['GET', 'POST'])
def Search():
    talksCount = talks.count()
    if request.method == 'GET':
        return render_template('search.html', talksCount=talksCount, hasResults=False)

    else:
        searchTerm = request.form['term']
        results = talks.find({"$text": {"$search": searchTerm}})
        hasResults = True if results.count() > 0 else False
        return render_template('search.html', talksCount=talksCount, results=results, hasResults=hasResults)


@app.route('/importall', methods=['GET', 'POST'])
def ImportAll():
    if request.method == 'GET':
        return render_template('importall.html', title='Batch Import')

    else:
        for i in range(1,100):
            url = "https://www.ted.com/talks/" + str(i)
            didImport = ImportURL(url)
            if didImport:
                time.sleep(20)
        return render_template('success.html', title='Batch import successful')

@app.route('/import', methods=['GET', 'POST'])
def ImmportSingle():
    if request.method == 'GET':
        return render_template('importsingle.html', title="Import Talk")

    else:
        didImport = ImportURL(request.form['url'])
        if didImport:
            return render_template('success.html', title="Import Successful")
        else:
            return render_template('failure.html', errormsg="Talk already in DB")

if __name__ == '__main__':
    app.run()
