from flask import Flask
from flask import Flask, render_template, redirect, url_for, request
from bs4 import BeautifulSoup
import requests
import time
import re

blacklist_lines = []
names_lines = []

timestamp = 0
timeout_sec = 60
url_pattern = '(http|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'

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

def build_link(formString,pages = 0):
    words = formString.split()
    search = ""
    for w in words:
    	if(search == ""):
    	    search = w
    	else:
    	    search = search + "+" + w
    #&first=X
    
    search = "http://www.bing.com/search?q="+search+"&form=QBRE"+"&first="+str(pages)
   
    return search

def get_search_body(url):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    source = requests.get(url,headers=headers).text
    soup = BeautifulSoup(source, 'lxml')

    mydivs = soup.find_all("li", {"class": "b_algo"})
    return mydivs


def filtered_html_body(url):
    divList = get_search_body(url)
    string = ""

    for div in divList:
        string = string + str(div)
    #string = re.sub('<cite>(http|https):\/\/([\w\-_\\])+<\cite>',"",string)
    regex = r"<a [a-zA-Z0-9%=;&\-\"_\\.\?\/: ,]*>Diese Seite übersetzen<\/a>"
    string = re.sub(regex,'',string)

    regexForm = r"<form\s*.*>\s*.*<\/form>"
    string = re.sub(regexForm,'',string)

    i,j = 0,0
    while(True):
        print("im doing it")
        prog = re.compile('.*')
        result = prog.match(string)
        print(result)
        break
    
    return string

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
        if request.form.get("next"):
			# do something
            if(request.args.get('pages')):
                pages = request.args.get('pages')
                pages = int(pages)
                pages= pages + 7
            else:
                pages = 0
            arg = request.args.get('q')
            return redirect("/search?q=abc&pages="+str(pages))
        elif request.form.get("prev"):
            if(request.args.get('pages')):
                pages = request.args.get('pages')
                pages = int(pages)
                pages= pages - 7
                if pages < 0:
                    pages =0
            else:
                pages = 0
            arg = request.args.get('q')
            return redirect("/search?q=abc&pages="+str(pages))


        if request.form['search'] :
            if isBlocked(request.form['search']):
                return redirect(url_for('wait'))#Should add imidiate punishment
            else:
                result=filtered_html_body(build_link(request.form['search']))
                return render_template('search.html',result=result)
        else:
            error = 'Search'
            return 'error boy'+request.form['search'] 

    # the code below is executed if the request method is Get
    pages = 0
    if(request.args.get('pages')):
        pages = request.args.get('pages')
    print(pages)
    if request.args.get('q'):
        arg = request.args.get('q')
        print(arg)
        if isBlocked(arg):
                return redirect(url_for('wait'))#Should add imidiate punishment
        else:
            result=filtered_html_body(build_link(arg,pages))
            return render_template('search.html',result=result)
    return render_template('search.html')    
   
@app.route('/wait',methods=['POST', 'GET'])
def wait():
    global timestamp
    timestamp = time.time()
    if request.method == 'POST':
        return render_template('search.html',result="you have been blocked for (another)..." + str(timeout_sec) + "seconds")
    else:
        return render_template('search.html',result="you have been blocked for (another)..." + str(timeout_sec) + "seconds")
