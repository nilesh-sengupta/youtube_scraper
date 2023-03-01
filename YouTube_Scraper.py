# importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import date
import pandas as pd

def search_youtube(search_term):
    title = []
    links = []
    channel_name = []
    comments = []
    duration = []
    views = []
    likes = []
    days = []

    # preparing the URL
    url = "https://www.youtube.com/results?search_query="
    # search_term = "indian+budget+2023"
    url = url + search_term

    # creating the webdriver object
    driver = webdriver.Chrome('./chromedriver')
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['disable-logging'])
    # driver = webdriver.Chrome(options=options)

    # start the webdriver and search for the URL
    driver.get(url)
    # delay as per network latency
    time.sleep(5)
    driver.maximize_window()
    # scroll the page by 1000 pixels for n number of times(as per the requirement of data entries)
    for i in range(6):
        driver.execute_script("window.scrollBy(0,1000)", "")
        time.sleep(2)
    time.sleep(5)

    # fetching video title by HTML id
    temp = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    meta = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-video-meta-block')
    j = 0
    for i in range(min(len(temp), len(meta))):
        live = meta[i].text
        if "watch" in live:
            continue
        title.append(temp[i].text)
        links.append(temp[i].get_attribute('href'))
        if links[j] == None:
            del title[j]
            del links[j]
            j -= 1
        j += 1

    links = links[0:2]
    # fetching channel name by HTML class name
    temp = driver.find_elements(By.ID, 'channel-info')
    for i in temp:
        channel_name.append(i.text)


    def convert_time(t):
        l = t.split(':')
        for i in range(len(l)):
            l[i] = int(l[i])
        if len == 2:
            mins = l[0] + 60 * l[1]
        else:
            mins = l[0] / 60 + l[1] + 60 * l[2]
        return mins


    def date_converter(d):
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

        return date(int(d[-4:]), month, day)


    # fetching duration, views, likes, upload date & no. of comments from each video in search results
    for i in links:
        driver.get(i)
        time.sleep(2)
        try:
            video_duration = driver.find_element(By.CLASS_NAME,
                                                'style-scope ytd-thumbnail-overlay-time-status-renderer').text
        except:
            video_duration = driver.find_element(By.CLASS_NAME, 'ytp-time-duration').text
        duration.append(video_duration)
        # duration.append(convert_time(video_duration))
        # metadata = driver.find_element(By.CLASS_NAME, 'style-scope ytd-watch-metadata').text
        # meta_lines = metadata.splitlines()
        # view = [s for s in meta_lines if " views" in s][0].split(' ')[0]
        # views.append(view)
        try:
            like = driver.find_element(By.XPATH,
                                '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span').text
        except:
            like = driver.find_element(By.XPATH, '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span').text
        likes.append(like)
        driver.execute_script("window.scrollBy(0,800)", "")
        time.sleep(3)
        try:
            no = int(driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text.replace(',', ''))
        except:
            no = -1
        comments.append(no)
        # btn = driver.find_elements(By.XPATH, '//*[@id="text"]')
        # aria_label = [label.get_attribute("aria-label") for label in btn]
        # for j in aria_label:
        #     if j is None:
        #         continue
        #     elif 'likes' in j:
        #         likes.append(int(j[:-6].replace(',', '')))
        driver.execute_script("window.scrollBy(0,-800)", "")
        try:
            btn = driver.find_element(By.XPATH, '//*[@id="expand"]').click()
            time.sleep(2)
            view = driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text.split(' ')[0]
            views.append(view)
            upload_date = driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text
            d1 = date.today()
            d0 = date_converter(upload_date)
            delta = d1 - d0
            days.append(delta.days)
        except:
            views.append(-1)
            days.append(-1)

    # to create a pandas dataframe
    data = {'Video Title': [], 'Links': [], 'Channel Name': [], 'Duration': [], 'Views': [], 'Likes': [],
            'No. of Comments': [],
            'Days since Upload': []}
    n = min(len(title), len(links), len(channel_name), len(duration), len(views), len(likes), len(comments), len(days))
    print(title)
    print(links)
    print(channel_name)
    print(comments)
    print(duration)
    print(views)
    print(likes)
    print(days)
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
    print(df)

    # exporting to csv format
    df.to_csv('data.csv')
    time.sleep(4)
    driver.close()
    return df
