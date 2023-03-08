#importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import pandas as pd
import traceback
import multiprocessing

#Chrome Driver object
driver = None
BATCH_SIZE=5
#video details that are not accessed during multiprocessing
title = []
links = []
channel_name = []

class scraper:

    #Initializing search query, number of videos and number of scrolls
    def __init__(self, searchQuery, numberOfVideos, numberOfScrolls):
        self.searchQuery = searchQuery
        self.numberOfVideos = numberOfVideos
        self.numberOfScrolls = numberOfScrolls

    def driver_setup(self):
        try:
            url = "https://www.youtube.com/results?search_query="
            url = url + self.searchQuery
            global driver
            #driver settings: headless, if any element is not found driver waits for 10 seconds
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--mute-audio')
            driver = webdriver.Chrome('./chromedriver',options=options)
            driver.implicitly_wait(10)
            driver.get(url)
        except:
            traceback.print_exc()
        return None

    def scroll_page(self):
        global driver
        try:
            for i in range(self.numberOfScrolls):
                driver.execute_script("window.scrollBy(0,500)", "")
        except:
            traceback.print_exc()
        return None
    
    def get_title_and_link(self):

        try:
            global title
            global links
            titleAndLinkRawData = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
            checkIsLive = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-video-meta-block')
            j = 0
            for i in range(min(len(titleAndLinkRawData), len(checkIsLive))):
                live = checkIsLive[i].text
                if "watch" in live:
                    continue
                title.append(titleAndLinkRawData[i].text)
                links.append(titleAndLinkRawData[i].get_attribute('href'))
                if links[j] == None:
                    del title[j]
                    del links[j]
                    j -= 1
                j += 1

            links = links[0:self.numberOfVideos]
        except:
            traceback.print_exc()
        return None
    
    def get_channel_info(self):

        try:
            global channel_name
            channelInfoRawData = driver.find_elements(By.ID, 'channel-info')
            for i in channelInfoRawData:
                channel_name.append(i.text)
        except:
            traceback.print_exc()
        return None
    
    def date_converter(self,d):
        try:
            if "Streamed" in d:
                d = d[17:]
            if "Premiered" in d:
                d = d[10:]
            if d[:3] == 'Jan':
                month = 1
            elif d[:3] == 'Feb':
                month = 2
            elif d[:3] == 'Mar':
                month = 3
            elif d[:3] == 'Apr':
                month = 4
            elif d[:3] == 'May':
                month = 5
            elif d[:3] == 'Jun':
                month = 6
            elif d[:3] == 'Jul':
                month = 7
            elif d[:3] == 'Aug':
                month = 8
            elif d[:3] == 'Sep':
                month = 9
            elif d[:3] == 'Oct':
                month = 10
            elif d[:3] == 'Nov':
                month = 11
            else:
                month = 12
            if len(d) == 12:
                day = int(d[4:6])
            else:
                day = int(d[4:5])
        except:
            traceback.print_exc()
            return None
        return date(int(d[-4:]), month, day)
    
    def get_duration(self,driver_mp,duration,i):
        try:
            try:
                video_duration = driver_mp.find_element(By.CLASS_NAME, 'style-scope ytd-thumbnail-overlay-time-status-renderer').text
            except:
                video_duration = driver_mp.find_element(By.CLASS_NAME, 'ytp-time-duration').text
            duration.insert(i,video_duration)
        except:
            traceback.print_exc()
            return None
        return None
    
    def get_likes(self,driver_mp,likes,i):
        try:
            like = driver_mp.find_element(By.XPATH, '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span').text
            likes.insert(i,like)
        except:
            traceback.print_exc()
            return None
        return None
    
    def get_comments(self,driver_mp,comments,i):
        try:
            driver_mp.execute_script("window.scrollBy(0,100)", "")
            numberOfComments=-1
            try:
                numberOfComments = int(driver_mp.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text.replace(',', ''))
            except:
                traceback.print_exc()
            comments.insert(i,numberOfComments)
            driver_mp.execute_script("window.scrollBy(0,-100)", "")
        except:
            traceback.print_exc()
            return None
        return None
    
    def getDaysSinceUploadAndViews(self,driver_mp,views,days,i):
        try:
            descriptionExpandButton = driver_mp.find_element(By.XPATH, '//*[@id="expand"]').click()
            viewsRawData = driver_mp.find_element(By.XPATH, '//*[@id="info"]/span[1]').text.split(' ')[0]
            views.insert(i,viewsRawData)
            uploadDataText = driver_mp.find_element(By.XPATH, '//*[@id="info"]/span[3]').text
            dateToday = date.today()
            dateUpload = self.date_converter(uploadDataText)
            daysPassed = dateToday - dateUpload
            days.insert(i,daysPassed.days)
            driver_mp.close()
        except:
            traceback.print_exc()
            views.insert(i,-1)
            days.insert(i,-1)
            return None
        return None
    
    def get_details(self,url,duration,likes,days,views,comments,i):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--mute-audio')
            driver_mp = webdriver.Chrome('./chromedriver',options=options)
            driver_mp.implicitly_wait(10)
            driver_mp.get(url)
            self.get_duration(driver_mp,duration,i)
            self.get_likes(driver_mp,likes,i)
            self.get_comments(driver_mp,comments,i)
            self.getDaysSinceUploadAndViews(driver_mp,views,days,i)
        except:
            traceback.print_exc()
            return None
        return None

    def dataframe_to_csv(self,df):
        try:
            df.to_csv('data.csv')
        except:
            traceback.print_exc()
            return None
        return None
    
    def main(self):
        try:
            global BATCH_SIZE
            #lists to store details pertaining to a video
            manager = multiprocessing.Manager()
            comments = manager.list()
            duration = manager.list()
            views = manager.list()
            likes = manager.list()
            days = manager.list()
            self.driver_setup()
            self.scroll_page()
            self.get_title_and_link()
            self.get_channel_info()
            driver.close()
            processes = []

            for i in range(len(links)):
                duration.append(-1)
                likes.append(-1)
                days.append(-1)
                views.append(-1)
                comments.append(-1)
            for i in range(0,len(links),BATCH_SIZE):
                if(i+BATCH_SIZE<len(links)):
                    for j in range(i,i+BATCH_SIZE):
                        p = multiprocessing.Process(target=self.get_details, args=(links[j],duration,likes,days,views,comments,j))
                        p.start()
                        processes.append(p)
                    for p in processes:
                        p.join()
                else:
                    for j in range(i,len(links)):
                        p = multiprocessing.Process(target=self.get_details, args=(links[j],duration,likes,days,views,comments,j))
                        p.start()
                        processes.append(p)
                    for p in processes:
                        p.join()
            data = {'Video Title': [], 'Links': [], 'Channel Name': [], 'Duration': [], 'Views': [], 'Likes': [],'No. of Comments': [],'Days since Upload': []}
            n = min(len(title), len(links), len(channel_name), len(duration), len(views), len(likes), len(comments), len(days))
            for i in range(0, n):
                data['Video Title'].append(title[i])
                data['Links'].append(links[i])
                data['Channel Name'].append(channel_name[i])
                data['No. of Comments'].append(comments[i])
                data['Duration'].append(duration[i])
                data['Views'].append(views[i])
                data['Likes'].append(likes[i])
                data['Days since Upload'].append(days[i])
            df = pd.DataFrame(data)
            self.dataframe_to_csv(df)
            return df
        except:
            traceback.print_exc()
            return None

if __name__=="__main__":
    multiprocessing.freeze_support()
    obj=scraper("indian budget 2023",3,5)
    df=obj.main()
    print(df)