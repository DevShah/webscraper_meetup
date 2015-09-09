

import urllib2
import lxml.html
from pymongo import MongoClient

hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

# We will be grabbing the first ten pages of ycombinator
for x in range(1,10):
    # The format of the site will look like 'https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2', etc
    url = 'https://news.ycombinator.com/news?p=%s'
    url = url % x
    
    # Create the request
    req = urllib2.Request(url, headers=hdr)
    # Receieve a response from the request
    resp = urllib2.urlopen(req)
    # Create a parsable lxml doc from the response
    doc = lxml.html.fromstring(resp.read().decode("utf8"))

# Search for all tables, and store the second one inside of table_doc
table_doc = doc.xpath("//table")[2]

# data is an empty list
data = []

# enumerate takes a list of things and gives back the index and value e.g. (0, value0) (1, value1) (2, value2) etc.
# 
# Starting with the table we stored earlier, find the first tr tag, then the td flag with class name title under that
# and all of the references located there
for index, tr in enumerate(table_doc.xpath("tr//td[@class='title']/a")):
    data_hash = {}
    
    # Check to see if one of the links does not say 'More', than store the comment
    if(tr.text_content() != 'More'):
        comments = tr.xpath("../../following-sibling::tr")[0]
        
        # Grab the user if one exists
        user = comments.xpath("td[@class='subtext']/a[contains(@href,'user')]")
        if(user):
            user = user[0].text_content()

        # Grab the comment if one exists
        comment = comments.xpath("td[@class='subtext']/a[contains(@href,'item')]")
        if(comment):
            comment = comment[0].text_content()

         # Grab the comment score if one exists
        score = comments.xpath("td[@class='subtext']/span")
        if(score):
            score = score[0].text_content()
        # Grab the title if one exists
        title = tr.text_content()

        data_hash['title'] = title
        data_hash['user'] = user
        data_hash['comment'] = comment
        data_hash['score'] = score
        data.append(data_hash)
    
    # Save all of that data to a database        
    db = client.test_database
    collection = db.test_collection
    collection.insert(data)





# #
# SELENIUM CODE
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
