import urllib
import urllib2

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) " + \
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"
headers = {'User-Agent': userAgent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    print response.read()
except urllib2.URLError, e:
    print e

