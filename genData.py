#! /usr/bin/python

import urllib2
import re
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def getWikicfp():
    url =  "http://www.wikicfp.com/cfp/servlet/event.showlist?lownerid=84778&ltype=w"
    web = urllib2.urlopen(url)

    html = web.read()
    start = html.find("<table cellpadding=\"3\" cellspacing=\"1\" align=\"center\" width=\"100%\">")
    end = start+html[start:].find("</table>")+8

    soup = BeautifulSoup(html[start:end], "html.parser")
    temp = []
    conf = []
    i = 0
    for idx, val in enumerate(soup.find_all('td')):
        text = val.get_text().strip().encode('utf-8')
        if (idx > 4 and text != ""):
            if (text == "N/A"):
                temp.append("")
            else:
                temp.append(text)
            i = i + 1
        if (i == 5):
            conf.append(temp)
            i = 0
            temp = []

    conf.sort(compare)

    conf_str = str(conf)
    conf_str = conf_str.replace("[[", "[\n[").replace("]]", "]\n]").replace("], ","],\n")
    with open('cfp.js', 'w') as f:
        f.write("var cfp = "+conf_str+";")


def compare(a, b):
    return (datetime.strptime(a[4].split(" (")[0], "%b %d, %Y") > datetime.strptime(b[4].split(" (")[0], "%b %d, %Y"))


getWikicfp()
