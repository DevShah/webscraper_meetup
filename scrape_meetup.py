

import urllib2
import lxml.html
from pymongo import MongoClient

hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

for x in range(1,10):

    url = 'https://news.ycombinator.com/news?p=%s'
    url = url % x
    req = urllib2.Request(url, headers=hdr)

    resp = urllib2.urlopen(req)

    doc = lxml.html.fromstring(resp.read().decode("utf8"))


table_doc = doc.xpath("//table")[2]

data = []

for index, tr in enumerate(table_doc.xpath("tr//td[@class='title']/a")):
    data_hash = {}
    if(tr.text_content() != 'More'):
        comments = tr.xpath("../../following-sibling::tr")[0]
        

        user = comments.xpath("td[@class='subtext']/a[contains(@href,'user')]")
        if(user):
            user = user[0].text_content()


        comment = comments.xpath("td[@class='subtext']/a[contains(@href,'item')]")
        if(comment):
            comment = comment[0].text_content()


        score = comments.xpath("td[@class='subtext']/span")
        if(score):
            score = score[0].text_content()

        title = tr.text_content()

        data_hash['title'] = title
        data_hash['user'] = user
        data_hash['comment'] = comment
        data_hash['score'] = score
        data.append(data_hash)
            
    db = client.test_database
    collection = db.test_collection
    collection.insert(data)





# #
# http://www.w3schools.com/ajax/default.asp
# driver.find_element_by_tag_name("button”)
# driver.find_element_by_tag_name("button").click()

import os
from selenium import webdriver

chromedriver = "/Users/itsdev/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("http://www.w3schools.com/ajax/default.asp")
# driver.quit()
# #
