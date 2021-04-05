from flask import Flask
from flask import Flask, render_template, redirect, url_for, request
from bs4 import BeautifulSoup
import requests
import time

blacklist_lines = []
names_lines = []

timestamp = 0
timeout_sec = 60

def read_lower_lines(filepath):
    lines = []
    with open(filepath, 'r') as fileinput:
        for line in fileinput:
            line = line.lower()
            lines.append(line.rstrip('\n'))
    return lines

def prepare():
    global blacklist_lines
    blacklist_lines = read_lower_lines('./data/blackList.txt')
    global names_lines
    names_lines = read_lower_lines('./data/pornStarNames.txt')

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

def get_search_body(url):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    source = requests.get(url,headers=headers).text
    soup = BeautifulSoup(source, 'lxml')

    mydivs = soup.find_all("li", {"class": "b_algo"})
    return mydivs


def html_body(url):
    divList = get_search_body(url)
    sb = ""

    for div in divList:
        sb = sb + str(div)
    return sb

def isBlocked(words):
    words = words.lower()
    words = words.split()
    #search for easy blocked words
    for word in words:
        if word in blacklist_lines:
            return True
 
    for name in names_lines:
        count = 0
        lengthName = len(name.split())
        nameParts = name.split()
        for namePart in nameParts:
            if namePart in words:
                count = count + 1
        if count >= lengthName:
            return True
    return False
        
               

prepare()
app = Flask(__name__)


@app.route('/search', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def search():
    now = time.time() - timestamp
    if (now < timeout_sec and timestamp > 0):
        return redirect(url_for('wait'))
    error = None
    if request.method == 'POST':
        if request.form['search'] :
            if isBlocked(request.form['search']):
                return redirect(url_for('wait'))#Should add imidiate punishment
            else:
                result=html_body(build_link(request.form['search']))
                return render_template('search.html',result=result)
        else:
            error = 'Search'
            return 'error boy'+request.form['search'] 

    # the code below is executed if the request method is Get
    if request.args.get('q'):
        arg = request.args.get('q')
        print(arg)
        if isBlocked(arg):
                return redirect(url_for('wait'))#Should add imidiate punishment
        else:
            result=html_body(build_link(arg))
            return render_template('search.html',result=result)
    return render_template('search.html')    
   
@app.route('/wait')
def wait():
    global timestamp
    timestamp = time.time()
    return render_template('search.html',result="you have been blocked for (another)..." + str(timeout_sec) + "seconds")