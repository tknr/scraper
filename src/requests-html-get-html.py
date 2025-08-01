#!/usr/bin/python
import sys
import os

from requests_html import HTMLSession

def showUsage():
    print("usage: %s [url] [text|TEXT:text html|HTML:html]" % os.path.basename(__file__))


args = sys.argv
args_length = len(args)
#print(args_length)
if args_length == 1:
    showUsage()
    exit()

URL = args[1]
#print(URL)

session = HTMLSession()
r = session.get(URL)
r.html.render(timeout=20)

for t in r.html.find('body'):
    if args_length == 2 or args[2] == "text" or args[2] == "TEXT" :
        print(t.text)
    elif args[2] == "html" or args[2] == "HTML" : 
        print(t.html)

r.close()
session.close()

