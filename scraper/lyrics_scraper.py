from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotVisibleException
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import requests
import lxml.html as html
import re
import warnings
import pandas as pd
import csv

URL_LYRICS= 'https://www.azlyrics.com/'

def scrape_lyrics_selenium(song):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-startup-window')
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    wait = WebDriverWait(driver,.5)
    try:
        driver.get(URL_LYRICS)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/form/div/div/input')))
        lyrics_search = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/form/div/div/input')
        lyrics_search.click()
        write_name = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/form/div/div/input')
        write_name.send_keys(song)
        write_name.send_keys(u'\ue007')
        current_url = driver.current_url
        click_on_song = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/table/tbody/tr[1]/td/a')
        click_on_song.click()
        WebDriverWait(driver, .5).until(EC.url_changes(current_url))
        r = requests.get(driver.current_url)
        driver.close()
        if r.status_code == 200:
            html_home = r.content.decode('utf-8')
            parsed = html.fromstring(html_home)
            lyrics = parsed.xpath('/html/body/div[2]/div/div[2]/div[5]/text()')
            lyrics = ''.join(lyrics)
            lyrics = re.sub('\s+', ' ', lyrics)
            return lyrics
        else:
            print(r.status_code)
    except (TimeoutException, ElementClickInterceptedException,NoSuchElementException) as e:
        print(f'There was an error looking for the song {song}')
    

def scrape_lyrics_requests(name, artists):
    #print(name)
    name = name.replace("Remasterizado", " ")
    artist = re.sub(r'[^a-zA-Z0-9]+', '', artists)
    name = re.sub(r'[^a-zA-Z0-9ñÑ]+', '', name)
    
    sub_url = artist + '/' +  name
    sub_url = sub_url.replace(" ", "")
    full_url=URL_LYRICS + 'lyrics/' + sub_url + '.html'
    full_url = str(full_url.lower())
    print(full_url)
    r = requests.get(full_url)
    if r.status_code > 199 and r.status_code <= 299:
        
        html_home = r.content.decode('utf-8')
        parsed = html.fromstring(html_home)
        lyrics = parsed.xpath('/html/body/div[2]/div/div[2]/div[5]/text()')
        lyrics = ''.join(lyrics)
        lyrics = re.sub('\s+', ' ', lyrics)
        return lyrics
    else:
        return None

def save_to_csv(song, lyrics):
    print(song, lyrics)
    print(type(song), type(lyrics))

def select_years(years):
    counter = 0
    songs_lyrics_dict = {}
    df =  pd.read_csv('../in/temp.csv')
    with open('lyrics3.csv', 'a', newline='', encoding="utf-8", errors="ignore") as f:
        w = csv.writer(f)
        for index, row in df.iterrows():
            if re.match('^[a-zA-Z.,]+$', row['name']) or (row['year'] <= 1950 or row['year'] > 1954):#or row['year'] != year:#(row['year'] < 1923 or row['year'] > 1980):
                pass
            else:
                lyrics = None
                lyrics = scrape_lyrics_selenium(row['name'])
                #lyrics = scrape_lyrics_requests(row['name'], row['artists'])
                if lyrics is not None:
                    if re.match('^[0-9a-zA-Z.,]+$', lyrics):
                        pass
                    else:
                        w.writerow([row['name'],lyrics, row['year']])
                        print('Added song: ', row['name'])

if __name__ == '__main__':
    header = ["song", "lyrics", "year"]
    with open('lyrics3.csv', 'w+', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
    #select_years(list(range(1923,1981,1)))
    select_years(1)


