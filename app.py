from flask import Flask, render_template, request
import pandas as pd
from YouTube_Scraper import search_youtube
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = search_youtube(search_term)
        res=results.to_dict('dict')

        print(res)
        return render_template('results.html', results=res)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
