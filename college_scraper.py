# HTML parser
# http://lxml.de/lxmlhtml.html
import lxml.html

# extensible library for opening URLs
# https://docs.python.org/2/library/urllib2.html
import urllib2

# The base url - after we specify the page number which will replace that %s, we have the link that we will be scraping
link = 'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+%s'


# We're going to iterate for the first ten pages of usnews for national-university rankings
for page in xrange(1,10):
    # open_link = 'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+1', 'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+2', etc. as a result of this line
    open_link = link % page

    # Open up the url and store the response.
    # The response typically contains a response code (200 signals a good response; and there are a whole list of bad responses like 404 or 300). Afterwards we read the response which gives us the page source. This will look like this: view-source:http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+1
    response = urllib2.urlopen(open_link).read() 

    # Response is currently just text, we need to actually convert it into something parsable. To do this we call lxml's library and convert it from a string
    doc = lxml.html.fromstring(response)

    # Now comes the tricky part. We want to search and iterate over all the rows of the table. To do this, I typically go into the web browser and look for where exactly my data is. If I look around, I see that it's stored within a <table> tag. And if I keep going into that tag, I see that all of the rows are <tr> tags. 

    # xpath let's you specify a string which comes in the following format
    # xpath("//<tag_name>//<tag_name2>//<tag_name3>")
    # You can also specify things for each tag, like any attributes it has
    # See the following example:
    # The following returns a list of div tags which has contains the class attribute
    # 'tag' and 'btag'.
    # 
    # //div[contains(@class,'atag') and contains(@class ,'btag')]
    #
    # On the page source, it would most likely look like this
    #
    # <div class = 'atag maybe_some_more_stuff btag other_stuff_maybe'></div>
    #
    # The notation [1:] means that we want everything from the first element onward
    # i.e. omit the zeroth element
    for row in doc.xpath("//table//tr")[1:]:
        # name is in the 2nd column, and tuition in the 3rd (columns start at zero/are zero indexed)
        name = row.xpath("td/a")[0].text_content().strip()
        tuition = row.xpath("td")[2].text_content().strip()
        enrollment = row.xpath("td")[3].text_content().strip()
        print "The name is: "
        print name
        print "The tuition is: "
        print tuition
        print "The enrollment is: "
        print enrollment
        print "============================="



# Things to keep in mind
# Variables are means of storing data, x is the variable in the following scenario
# x = 5
# Here, y is the variable and it is assigned to a list of 3 numbers
# y = [1, 2, 3] 
#
# arrays are zero index meaning that 5 is the first element at index 0
# 15 is the second element at index 1, 29 the third element at index 2, etc.
#        [5, 15, 29, 30]
# index   0,  1,  2,  3
#
# Everything is Google-able!
#
# 
# 
