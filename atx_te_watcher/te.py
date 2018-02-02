# -*- coding: utf-8 -*-

import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from .helper import get_year_from_tag, get_day_from_tag, create_datetime

class TePageCrawler:
    url_encout = 'https://www.at-x.com/encount/'

    __driver = None
    __driver_wait = None
    __soup = None

    def __init__(self):
        pass
    
    def start(self):
        options = Options()
        options.add_argument('--headless') # ヘッドレスモードを有効にする

        driver = webdriver.Chrome(chrome_options=options)
        driver.set_page_load_timeout(10) #ページロードのタイムアウト(秒)

        driver_wait = WebDriverWait(driver, 10) #操作した時のタイムアウト時間

        # AT-Xの番組紹介ページから放送日を取得する
        driver.get('https://www.at-x.com/encount/')

        driver_wait.until(ec.presence_of_all_elements_located) #処理待ち

        assert '東京エンカウント' in driver.title
        data = driver.page_source.encode('utf-8')
        self.__soup = BeautifulSoup(data, 'lxml')
        self.__driver = driver
        self.__driver_wait = driver_wait

    def get_contents_digest(self):
        schedule = self.__soup.find(id="schedule")
        schedule_digest = hashlib.sha224(str(schedule.text).encode('utf-8')).hexdigest()
        return schedule_digest
    
    def get_timetable(self):
        schedule = self.__soup.find(id="schedule")
        ttl_lv03 = schedule.find_all(class_='ttl_lv03')
        time_table = schedule.find_all(class_='time_table')

        schedule_list = []
        for h3, div in zip(ttl_lv03, time_table):
            story_number = h3.find(class_='icon_number')
            year = div.find_all(class_='year')[0]
            days = div.find_all(class_='days')[0].find_all('li')
            for day in days:
                yyyy = get_year_from_tag(year)
                mo, day, h, m = get_day_from_tag(day)
                date = create_datetime(yyyy, mo, day, h, m, 'Asia/Tokyo')
                # entry = TePageCrawlerShedule(len(schedule_list), date.timestamp(), story_number.text)
                entry = TePageCrawlerShedule(len(schedule_list), date, story_number.text)
                schedule_list.append(entry)

        schedule_list.sort(key=lambda x:x.date) #放送日順
        return schedule_list

    def get_newest_story(self):
        right_contents = self.__soup.find(id='right_contents')
        new_story_title = right_contents.find(class_='ttl_lv02').text.strip()
        new_story_body = right_contents.find(class_='contents').text.strip()
        # TODO: 漢数字を変換
        return (new_story_title, new_story_body)

    def close(self):
        """Terminate Browser"""
        self.__driver.quit()

class TePageCrawlerShedule:
    raw_index = 0
    date = None
    story_title = ''

    def __init__(self, raw_index, date, story_title):
        self.raw_index = raw_index
        self.date = date
        self.story_title = story_title

