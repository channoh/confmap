#! /usr/bin/python

import urllib2
import re
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def getWikiCfp(url):
    # url =  "http://www.wikicfp.com/cfp/servlet/event.showlist?lownerid=84778&ltype=w"
    web = urllib2.urlopen(url)

    html = web.read()
    start = html.find("<table cellpadding=\"3\" cellspacing=\"1\" align=\"center\" width=\"100%\">")
    end = start+html[start:].find("</table>")+8

    soup = BeautifulSoup(html[start:end], "html.parser")
    temp = []
    i = 0
    for idx, val in enumerate(soup.find_all('td')):
        if (idx < 4):
            continue
        if (idx > 8):
            break
        else:
            text = val.get_text().strip().encode('utf-8')
            if (text == "N/A"):
                temp.append("")
            else:
                temp.append(text)
    print("%s") % (temp[0])
    return temp



def compare(a, b):
    return (datetime.strptime(a[4].split(" (")[0], "%b %d, %Y") > datetime.strptime(b[4].split(" (")[0], "%b %d, %Y"))



def getRecentEvent():
    conferences = [
        ["ISCA",   "http://www.wikicfp.com/cfp/program?id=1683&s=ISCA&f=International%20Symposium%20on%20Computer%20Architecture"],
        ["ASPLOS", "http://www.wikicfp.com/cfp/program?id=242&s=ASPLOS&f=Architectural%20Support%20for%20Programming%20Languages%20and%20Operating%20Systems"],
        ["MICRO",  "http://www.wikicfp.com/cfp/program?id=2052&s=MICRO&f=International%20Symposium%20on%20Microarchitecture"],
        ["HPCA",   "http://www.wikicfp.com/cfp/program?id=1220&s=HPCA&f=High-Performance%20Computer%20Architecture"],
        ["CGO",    "http://www.wikicfp.com/cfp/program?id=429&s=CGO&f=Symposium%20on%20Code%20Generation%20and%20Optimization"],
        ["PLDI",   "http://www.wikicfp.com/cfp/program?id=2369&s=PLDI&f=Programming%20Language%20Design%20and%20Implementation"],
        ["LCTES",  "http://www.wikicfp.com/cfp/program?id=1950&s=LCTES&f=Languages,%20Compilers,%20and%20Tools%20for%20Embedded%20Systems"],
        ["PACT",   "http://www.wikicfp.com/cfp/program?id=2291&s=PACT&f=International%20Conference%20on%20Parallel%20Architectures%20and%20Compilation%20Techniques"],
        ["ISMM",   "http://www.wikicfp.com/cfp/program?id=1730&s=ISMM&f=International%20Symposium%20on%20Memory%20Management"],
        ]

    json = []
    for conf in conferences:
        json.append(getWikiCfp(conf[1]))

    json.sort(compare)

    json_str = str(json)
    json_str = json_str.replace("[[", "[\n[").replace("]]", "]\n]").replace("], ","],\n")
    print(json_str)
    with open('cfp.js', 'w') as f:
        f.write("var cfp = "+json_str+";")


getRecentEvent()
# getWikicfp()
