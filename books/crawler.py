import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def search_books(keyword):
    base_url = "https://www.bigee.cc/s?q="
    url = base_url + keyword
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    book_boxes = soup.find_all('div', class_='bookbox')
    books = []
    for box in book_boxes:
        book_info = {}
        book_info['书名'] = box.find('h4', class_='bookname').text.strip() if box.find('h4', class_='bookname') else 'N/A'
        book_info['链接'] = "https://www.bigee.cc" + box.find('h4', class_='bookname').find('a')['href'] if box.find('h4', class_='bookname').find('a') else 'N/A'
        book_info['作者'] = box.find('div', class_='author').text.strip().replace("作者：", "") if box.find('div', class_='author') else 'N/A'
        book_info['简介'] = box.find('div', class_='uptime').text.strip() if box.find('div', 'uptime') else 'N/A'
        books.append(book_info)
    if len(book_boxes) == 0:
        return None  # 如果搜索结果为空，返回 None
    return books



def get_book_details(book_url):
    response = requests.get(book_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    chapter_list = soup.find('div', class_='listmain')
    
    chapters = []
    if chapter_list:
        for dd in chapter_list.find_all('dd'):
            a = dd.find('a')
            if a:
                chapter_info = {}
                chapter_info['章节名'] = a.text.strip()
                chapter_info['链接'] = "https://www.bigee.cc" + a['href']
                chapters.append(chapter_info)
    return chapters

def get_chapter_content(chapter_url):
    response = requests.get(chapter_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    
    content_div = soup.find('div', class_='Readarea ReadAjax_content')
    
    if content_div:
        unwanted_p = content_div.find('p', class_='readinline')
        if unwanted_p:
            unwanted_p.decompose()
        return content_div.get_text(separator='\n').strip()
    return '章节内容获取失败'

def get_chapter_title(chapter_url):
    response = requests.get(chapter_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', class_='wap_none')
    if(title_tag!=''):
        return title_tag.get_text().strip()
    return '标题获取失败'
    

