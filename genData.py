#! /usr/bin/python

import urllib2
import re
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import json

def getWikiCfp(url, old):
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
    updated = "" if temp[0] == old else " ... updated"
    print("%s%s") % (temp[0], updated)
    return temp



def compare(a, b):
    try:
        ret = (datetime.strptime(a[4].split(" (")[0], "%b %d, %Y") > datetime.strptime(b[4].split(" (")[0], "%b %d, %Y"))
    except:
        ret = 1;
    return ret;




def getRecentEvent(old_cfp):
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
        ["FAST",   "http://www.wikicfp.com/cfp/program?id=1011&s=FAST&f=File%20and%20Storage%20Technologies"],
        ]

    json = []
    for i, conf in enumerate(conferences):
        json.append(getWikiCfp(conf[1], old_cfp[i][0]))

    json.sort(compare)
    return json


if __name__ == "__main__":
    with open ('cfp.js', 'r') as f:
        old_cfp = f.read().replace("var cfp = ", "old_cfp = ").replace(";", "").replace("\n", "")
        exec(old_cfp)   ## gen array 'old_cfp'
        new_cfp = getRecentEvent(old_cfp)

        cfp_str = str(new_cfp)
        cfp_str = cfp_str.replace("[[", "[\n[").replace("]]", "]\n]").replace("], ","],\n")
        ## print(cfp_str)
        with open('cfp.js', 'w') as f:
            f.write("var cfp = "+cfp_str+";")

