from flask import Flask
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['POST', 'GET'])
def search():
    error = None
    if request.method == 'POST':
        if request.form['search'] :
            #return redirect("http://www.bing.com/search?q="+request.form['search'])
            return render_template('search.html',result="http://www.bing.com/search?q="+request.form['search']) 
        else:
            error = 'Search'
            return 'error boy'+request.form['search'] 
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('search.html')    
    
