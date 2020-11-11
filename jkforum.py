# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 17:48:11 2020

@author: eddyteng
"""
import mechanicalsoup

home = "https://www.jkforum.net/"
name = "中山區.林森北路"
url = "type-1128-1476.html"


def parse_url(url, max_count=10):
    start_url = home + url
    
    browser = mechanicalsoup.StatefulBrowser()
    page = browser.get(start_url)
    
    a_list = page.soup.find_all("a")
    count = 0
    for a in a_list:
        if not (a.get("href") is None):
            link = a["href"]
            if "forum.php?mod=viewthread" in link:
                if not (a.get("onclick") is None):
                    click = a["onclick"]
                    if "atarget(this)" in click:
                        count = count + 1
                        content_url = home + link
                        found = parse_content(content_url)
                        if found:
                            print(a.text)
                            #print(content_url)
                            print("-----------------")
                        if count >= max_count:
                            return

def parse_content(url):
    browser = mechanicalsoup.StatefulBrowser()
    page = browser.get(url)
    
    table_list = page.soup.find_all("table")
    for table in table_list:
        if not (table.get("class") is None):
            cls = table["class"]
            if "view-data" in cls:
                found = find_line(table)
                if found:
                    meta = page.soup.find("meta", property='og:url')
                    if meta is not None:
                        print(meta["content"])
                    #print(table)
                    #print("-----------------")
                return found

def find_line(table):
    font_list = table.find_all("font")
    for font in font_list:
        line_text = {"Line", "LINE", "賴"}
        for t in line_text:
            if t in font.text:
                #print(font)
                #print("-----------------")
                return True
    return False

        
parse_url(url, 30)
