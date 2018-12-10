# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 15:41:49 2017

@author: eddyteng
"""
import os
import urllib.request
from bs4 import BeautifulSoup

home = "http://www.comicnad.com/comic/"
url = "102900311096001.html"
folder = "031"
url_list = {}

def parse_url(url):
    start_url = home + url
    url_list[url] = start_url

    #設置假的瀏覽器資訊
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
    req = urllib.request.Request(url=start_url,headers=headers)
    page = urllib.request.urlopen(req)
    contentBytes = page.read()
    soup = BeautifulSoup(str(contentBytes), "html.parser")
    
    img_list = soup.find_all("img")
    for img in img_list:
        img_url = img["src"]
        if img_url.find("cartoonmad.com") > 0:
            file_path = os.getcwd() + "/" + folder + "/" + img_url[img_url.rfind('/')+1:]
            if not os.path.isfile(file_path):
                print("Download " + img_url + " > " + file_path)
                urllib.request.urlretrieve(img_url, file_path)

    a_list = soup.find_all("a", {"class":"pages"})
    for a in a_list:
        url = a["href"]
        if not url in url_list:
            return url

while not (url is None):
    url = parse_url(url)

