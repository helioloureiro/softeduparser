#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# THE BEERWARE LICENSE (Revision 42):
#  Helio Loureiro wrote this. As long as you retain this notice you
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

def geturl(text):
    try:
        url = text.a.get("href")
    except AttributeError:
        url = None
    return url

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
        nome_programa_text = nome_programa.getText()
        nome_programa_url = geturl(nome_programa)
        down_win = info[7]
        down_win_url = geturl(down_win)
        down_lnx = info[8]
        down_lnx_url = geturl(down_lnx)
        down_mac = info[9]
        down_mac_url = geturl(down_mac)
        down_src = info[10]
        down_src_url = geturl(down_src)
        licenca = info[11].string
        idioma = info[12].string
        wikipedia = info[13]
        wikipedia_url = geturl(wikipedia)
        # skipping first line (summaries)
        if (area_conhecimento == "Total"):
            continue
        MYDATA[nome_programa_text] = {}
        MYDATA[nome_programa_text]['url'] = nome_programa_url
        MYDATA[nome_programa_text]['nivel_ensino'] = {}
        MYDATA[nome_programa_text]['nivel_ensino']['EI'] = nivel_ensino_EI
        MYDATA[nome_programa_text]['nivel_ensino']['AIEF'] = nivel_ensino_AIEF
        MYDATA[nome_programa_text]['nivel_ensino']['AFEF'] = nivel_ensino_AFEF
        MYDATA[nome_programa_text]['nivel_ensino']['EM'] = nivel_ensino_EM
        MYDATA[nome_programa_text]['nivel_ensino']['ES'] = nivel_ensino_ES
        MYDATA[nome_programa_text]['download'] = {}
        MYDATA[nome_programa_text]['download']['windows'] = down_win_url
        MYDATA[nome_programa_text]['download']['linux'] = down_lnx_url
        MYDATA[nome_programa_text]['download']['mac'] = down_mac_url
        MYDATA[nome_programa_text]['download']['source'] = down_src_url
        MYDATA[nome_programa_text]['idioma'] = idioma
        MYDATA[nome_programa_text]['licenca'] = licenca
        MYDATA[nome_programa_text]['wikipedia'] = wikipedia_url
        break
    return MYDATA

def generateoutput(msg):
    return msg

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