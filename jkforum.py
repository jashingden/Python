# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 17:48:11 2020

@author: eddyteng
"""
import mechanicalsoup

name_1476 = "中山區.林森北路"
url_1476 = "type-1128-1476.html"
name_1950 = "板橋.中永和"
url_1950 = "type-1128-1950.html"

home = "https://www.jkforum.net/"
name = name_1950
url = url_1950

mydir = 'D:\MITAKE\APK\JKF'
output = ""

def parse_url(url, max_count=10):
    global output
    start_url = home + url
    
    browser = mechanicalsoup.StatefulBrowser()
    page = browser.get(start_url)
    
    a_list = [a for a in page.soup.find_all("a") if a.get("href") is not None]
    count = 0
    for a in a_list:
        link = a["href"]
        if "forum.php?mod=viewthread" in link:
            if a.get("onclick") is not None:
                click = a["onclick"]
                if "atarget(this)" in click:
                    count = count + 1
                    content_url = home + link
                    og_url = parse_content(content_url)
                    if len(og_url) > 0:
                        output = output + "<br><a href='"+og_url+"'>"+a.text+"</a><br>\r\n"
                        output = output + "<hr>"
                        #print(a.text)
                        #print(content_url)
                        #print("-----------------")
                    if count >= max_count:
                        return

def parse_content(url):
    global output
    
    browser = mechanicalsoup.StatefulBrowser()
    page = browser.get(url)
    
    table_list = [table for table in page.soup.find_all("table") if table.get("class") is not None]
    for table in table_list:
        cls = table["class"]
        if "view-data" in cls:
            found = find_line(table)
            og_url = ""
            if found:
                #print(table)
                #print("-----------------")
                meta = page.soup.find("meta", property='og:url')
                if meta is not None:
                    og_url = meta["content"]
                    
                    img_list = [img for img in table.find_all("img") if img.get("file") is not None]
                    for img in img_list:
                        img_file = img["file"]
                        img_width = img["width"]
                        output = output + "<img src='"+img_file+"' width='"+img_width+"'>\r\n"
                        #print(img_file, img_width)
            return og_url

def find_line(table):
    font_list = table.find_all("font")
    for font in font_list:
        line_text = ("Line", "LINE", "賴")
        for t in line_text:
            if t in font.text:
                #print(font)
                #print("-----------------")
                return True
    return False

def saveHTML(path, html):
    file = open(path, 'w', encoding='UTF-8')
    file.write(html)
    file.close()


output = "<html><body><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8' />"
parse_url(url, 10)

output = output + "</body></html>"
#print(output)
saveHTML(mydir + '\\' + 'test.html', output)
