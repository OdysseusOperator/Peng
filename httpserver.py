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
            result=pullHtml(build_link(request.form['search']))
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
    search = "http://www.bing.com/search?q="+search+"&form=QBRE"
    return search

def pullHtml(url):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    source = requests.get(url,headers=headers).text
    soup = BeautifulSoup(source, 'lxml')

    mydivs = soup.find_all("li", {"class": "b_algo"})
    return mydivs


def prepare():
    return
