#!/usr/bin/python
import urllib.request, urllib.parse, urllib.error
 
username = 'honeytweeter'
password = 'fuckfacebook' 
message = "Hello Twitter!" 
data = urllib.parse.urlencode({"status" : message})
res = urllib.request.urlopen("http://%s:%s@twitter.com/statuses/update.xml" % (username,password), data)
