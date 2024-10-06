from flask import Flask, render_template, request, redirect, send_file, jsonify
import pandas as pd
import scraper
import multiprocessing
from scraper import scraper
from scraper_comments import scraper_comments
from sentiment_analysis import SentimentAnalysis  # Updated import statement
import urllib.parse
import cur
import psycopg2
from gpt import gpt
comments = []
# conn = psycopg2.connect(
#     database="ParsentLogin",
#     user="postgres",
#     password="admin",
#     host="localhost",
#     port="5432"
# )
# cur = conn.cursor()


app = Flask(__name__,static_url_path='/static')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        provided_password = request.form['password']
        # query = "SELECT * FROM userdetails WHERE username = %s"
        # cur.execute(query, (username,))
        result = "admin"
        if result:
            if (provided_password == "admin"):
                return jsonify({'message': 'Authentication successful'})
            else:
                return jsonify({'message': 'Authentication failed'}), 401
        else:
            return jsonify({'message': 'User not found'}), 401
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = request.args.get('username')
    if username is not None:
        if request.method == 'GET':
            return render_template('dashboard.html', results=username)
        elif request.method == 'POST':
            return render_template('dashboard.html', results=username)
    else:
        return render_template('dashboard.html', results=None)

@app.route('/targettedmonitor', methods=['GET', 'POST'])
def targettedmonitor():
    if request.method == 'POST':
        
        search_term= request.form['search_term']
        num_vid = request.form['num_vid']
        multiprocessing.freeze_support() 
        search_results = scraper(search_term,int(num_vid),int(num_vid))
        results = search_results.main()
        res=results.to_dict('dict')
        res['num_vid']=int(num_vid)
        return render_template('results.html', results=res)
    else:
        return render_template('index.html')
    
@app.route('/sentiment')
def sentiment():
    obj = SentimentAnalysis(comments)  # Updated class instantiation
    score,subjectivity,objectivity=obj.main()
    data=[]
    data.append(score)
    data.append(subjectivity)
    data.append(objectivity)
    data.append(comments)
    data.append(int(len(comments)))
    print(data)
    return render_template('sentiment.html', res = data)

@app.route('/sentimentgpt')
def sentimentgpt():
    obj = gpt(comments)  # Updated class instantiation
    score=obj.main()
    data=[]
    data.append(score)
    data.append(comments)
    data.append(int(len(comments)))
    print(data)
    return render_template('sentimentgpt.html', res = data)

@app.route('/comments', methods=['POST'])
def comments():
    global comments
    if request.method == 'POST':
        d = request.get_data()
        params = d.decode().split('&')
        link = None
        for param in params:
            key, value = param.split('=')
            if key == 'link':
                link = value
        link = urllib.parse.unquote(link)
        data = scraper_comments(link)
        comments = data.main()
        return render_template('comments.html', comments=comments)
    else:
        return render_template('index.html')

@app.route('/download')
def download_file():
    file_path = './data.csv'
    return send_file(file_path, as_attachment=True)

@app.route('/downloadcomments')
def download_comments():
    file_path = './comments.csv'
    return send_file(file_path, as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)
