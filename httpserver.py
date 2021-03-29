from flask import Flask
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/search/', methods=['POST', 'GET'])
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
    
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
    
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
    
def log_the_user_in(S):
    return redirect("/hello/"+S)
    
def valid_login(name,pw):
    return True
