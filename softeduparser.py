#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# THE BEERWARE LICENSE (Revision 42):
#  Helio Loureiro wrote these scripts. As long as you retain this notice you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer in return.
#
#                                             Helio Loureiro
#                                             helio@loureiro.eng.br
#

"""
Simple site parser to create mediawiki alike output.
"""

from BeautifulSoup import BeautifulSoup
import urllib
import sys

def getdata(url):
    """
    Connect into required url and retrieve data.
    """
    web = urllib.urlopen(url)
    return web.read()

def parsedata(html):
    """
    Read html page and gather only wanted information.
    """
    MYDATA = {}
    soup = BeautifulSoup(html)
    # retrieve info only from table
    table = soup.find("table")
    # retrieve data info, per line
    tr = table.findAll("tr")
    for line in tr:
        info = line.findAll("td")
        # if no info found, got to next line
        if (len(info) == 0):
            continue
        # it could be done in one line
        # but let's make it more readable
        area_conhecimento = info[0].string
        nivel_ensino_EI = info[1].string
        nivel_ensino_AIEF = info[2].string
        nivel_ensino_AFEF = info[3].string
        nivel_ensino_EM = info[4].string
        nivel_ensino_ES = info[5].string
        nome_programa = info[6]
        down_win = info[7]
        down_lnx = info[8]
        down_mac = info[9]
        down_src = info[10]
        licenca = info[11].string
        idioma = info[12].string
        wikipedia = info[13]
        # skipping first line (summaries)
        if (area_conhecimento == "Total"):
            continue
        print area_conhecimento, \
            nivel_ensino_EI, \
            nivel_ensino_AIEF, \
            nivel_ensino_AFEF, \
            nivel_ensino_EM, \
            nivel_ensino_ES, \
            nome_programa, \
            down_win, \
            down_lnx, \
            down_mac, \
            down_src, \
            licenca, \
            idioma, \
            wikipedia

def generateoutput(msg):
    None
def usage():
    print "Use: %s <url>" % sys.argv[0]
    sys.exit(1)

if __name__ == '__main__':
    try:
        URL = sys.argv[1]
    except:
        usage()
    html = getdata(URL)
    json = parsedata(html)
    output = generateoutput(json)
    print output