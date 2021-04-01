from flask import Flask
from flask import Flask, render_template, redirect, url_for, request
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def search():
    error = None
    if request.method == 'POST':
        if request.form['search'] :
            #return redirect("http://www.bing.com/search?q="+request.form['search'])
            result="http://www.bing.com/search?q="+build_link(request.form['search'])
            return render_template('search.html',result=result)
        else:
            error = 'Search'
            return 'error boy'+request.form['search'] 
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('search.html')    
   
def build_link(formString):
    words = formString.split()
    search = ""
    for w in words:
    	if(search == ""):
    	    search = w
    	else:
    	    search = search + "+" + w
    return search

def pullHtml():
    source = requests.get('https://webscraper.droppages.com/').text
    soup = BeautifulSoup(source, 'lxml')
    return(soup)


def prepare():
    return
