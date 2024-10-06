from youtube_search import YoutubeSearch
# from youtubesearchpython import VideosSearch
import pandas as pd
import traceback
class scraper:
    def __init__(self, searchQuery, numberOfVideos, numberOfScrolls):
        self.searchQuery = searchQuery
        self.numberOfVideos = numberOfVideos
        self.numberOfScrolls = numberOfScrolls

    
    def main(self):
        try:
            results = YoutubeSearch(self.searchQuery, max_results=self.numberOfVideos).to_dict()
            data = {
                "Video Title": [],
                "Links": [],
                "Channel Name": [],
                "Duration": [],
                "Views": [],
                "Days since Upload": [],
            }

            for item in results:
                data["Video Title"].append(item['title'])
                data["Links"].append('www.youtube.com'+item['url_suffix'])
                data["Channel Name"].append(item['channel'])
                data["Duration"].append(item['duration'])
                data["Views"].append(item['views'])
                data["Days since Upload"].append(item['publish_time'])

            data = pd.DataFrame(data)
            data.to_csv("data.csv")
            return data
        except:
            traceback.print_exc()
            return None


if __name__ == "__main__":
    scraper.main()
