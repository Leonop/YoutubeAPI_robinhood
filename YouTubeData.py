#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime as dt #sum the video's duration time
import pandas as pd 
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup as soup #used to beautifie the html code
import re


def get_html(): #used to get the html code of the current page
	innerHTML = driver.execute_script("return document.body.innerHTML")
	page_soup = soup(innerHTML, 'html.parser')
	return page_soup

def end_of_page(): #used to scroll down to the bottom of the page
	page_soup = get_html() #gets html to find the number of videos in playlist

	number_videos_container = page_soup.findAll('yt-formatted-string', {'class':'style-scope ytd-playlist-sidebar-primary-info-renderer'}) 
    #gets the number of videos for a future break in the scroll down loop
	str_number = number_videos_container[1].text #next lines clean up the string to make it a real number
	end_of_number = str_number.find(' ')
	str_number = str_number[:end_of_number].replace('.', '')

	number_videos = int(str_number) #number of videos

	times_scroll_down = int((number_videos/100) + 1)

	for i in range(times_scroll_down): #goes to the end of the playlist automatically
		elm = driver.find_element_by_tag_name('html')
		elm.send_keys(Keys.END)
		time.sleep(2)


# Initialize times
times = []  
#访问Youtube网站
driver = webdriver.Chrome()
#最大化窗口
driver.maximize_window()
#搜索 Stock to buy US, filter by last year and relevance
url= 'https://www.youtube.com/results?search_query=stock+to+buy+us&sp=CAMSBAgFEAE%253D' # Key words search in youtube is stock to buy
url_ps='https://www.youtube.com/results?search_query=penny+stock&sp=CAMSBAgFEAE%253D' # Key words search in youtube is penny stock
url_chinese='https://www.youtube.com/results?search_query=%E8%82%A1%E7%A5%A8&sp=CAMSBAgFEAE%253D' # Keywords =股票
url_chinese2='https://www.youtube.com/results?search_query=%E4%B8%AA%E8%82%A1&sp=CAMSBAgFEAE%253D' # Keyworkds = 个股
url_chinese3 ='https://www.youtube.com/results?search_query=%E7%89%9B%E8%82%A1&sp=CAMSAggF' # keywords=牛股
driver.get(url_chinese2) # Change keywords to get different vedio list
driver.save_screenshot("ytb1.png")#图片是为了比较变化

#将页面滚动条拖到底部 
    # js="var q=document.documentElement.scrollTop=30000" 
    # driver.execute_script(js) 
    # time.sleep(3)
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while(True):
    # 一直往下滑直到出现下一次的加载
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    # 等一下，直到加载完毕
    time.sleep(2)
    # 计算一下新的高度和上一次的高度进行比较
    new_height = driver.execute_script("return document.documentElement.scrollHeight")

    # driver.find_element_by_tag_name('body').send_keys(Keys.END)
    if new_height==last_height:
        break
    last_height = new_height

# One last scroll just in case 
driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

# end_of_page()

page_soup = get_html() #gets the complete html, after scrolling down, with all the duration and title of videos

time_containers = page_soup.findAll('div', {'class':'style-scope ytd-thumbnail'})
time_containers[0].text

print(time_containers[0].text)

for container in time_containers: #create a list with timestamps
	time = container.text[7:].rstrip()
	if time.count(':') == 1: #make so the timestamp includes hours as 00 if its shorter than 1 hour
		time = '00:'+ time
	else:
		time = time

	times.append(time)

times = list(filter(None, times)) #filter all the ZERO values of the list
time_total = dt.timedelta() #sets a variable in the HH:MM:SS format

user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
links = []
outcome = []
for i in user_data:
    try:
        link = i.get_attribute('href')
        links.append(link)
        v_id = str(link).replace('https://www.youtube.com/watch?v=','')
        v_title = i.get_attribute('title')
        v_description = i.get_attribute('aria-label')
        v_youtuber = re.findall('by(.+?)\d',v_description.replace(str(v_title),''))[0]
        v_post_time = re.findall('\d+\s+\w+\sago',v_description)[0].replace(' ago','')     
        v_view_count = re.findall('((\d+)|(\d+,\d+)) views',v_description)[0][0]
        outcome.append([v_youtuber, v_id, link, v_title, v_description, v_post_time, v_view_count])
    except:
        print('error')
    
outcome = pd.DataFrame(outcome, columns=['youtuber','vedio_id','link','vedio_title','description','post_time','views'])

# outcome.to_csv('stock_to_buy.csv') 
# change keywords for different outcome
# outcome.to_csv('penny_stock.csv') 
# outcome.to_csv('股票.csv') 
outcome.to_csv('个股.csv') 
# outcome.to_csv('牛股.csv') 
print(len(links)) 

driver.save_screenshot("ytb2.png")#图片是为了比较变化

