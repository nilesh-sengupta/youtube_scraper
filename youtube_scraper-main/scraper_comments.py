# importing necessary libraries
from itertools import islice
from youtube_comment_downloader import *
import time
import pandas as pd
import traceback
import csv

driver = None
comments = []

class scraper_comments:

    def __init__(self, url) :
        self.url = "https://"+url
    def get_comments(self):
        try:
            downloader = YoutubeCommentDownloader()
            comments = downloader.get_comments_from_url(self.url, sort_by=SORT_BY_POPULAR)
            print(self.url)
            comment_data = []
            print("Done Downloading")
            print(comment_data)
            for comment in islice(comments, 10):
                print(comment)
                comment_data.append(comment['text'])
            return comment_data
        except:
            traceback.print_exc()
        return None

    def main(self):
        comments = self.get_comments()
        with open('comments.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Comment'])
            for comment in comments:
                writer.writerow([comment])
        return comments
