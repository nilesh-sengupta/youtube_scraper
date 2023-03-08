from flask import Flask, render_template, request, redirect
import pandas as pd
import scraper
import multiprocessing
from scraper import scraper

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term= request.form['search_term']
        scroll_num = request.form['scroll_num']
        num_vid = request.form['num_vid']
        multiprocessing.freeze_support() 
        search_results = scraper(search_term,int(num_vid),int(scroll_num))
        results = search_results.main()
        res=results.to_dict('dict')
        res['num_vid']=int(num_vid)
        return render_template('results.html', results=res)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
