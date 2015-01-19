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
import json
import re

# patch to avoid UTF-8 errors - why coding isn't working?
reload(sys)
sys.setdefaultencoding("UTF-8")

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
        licenca = info[11].getText()
        licenca_url = geturl(info[11])
        idioma = info[12].string
        wikipedia = info[13].getText()
        wikipedia_url = geturl(info[13])
        # skipping first line (summaries)
        if (area_conhecimento == "Total"):
            continue
        MYDATA[nome_programa_text] = {}
        MYDATA[nome_programa_text]['area_conhecimento'] = area_conhecimento
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
        MYDATA[nome_programa_text]['licenca'] = {}
        MYDATA[nome_programa_text]['licenca']['tipo'] = licenca
        MYDATA[nome_programa_text]['licenca']['url'] = licenca_url
        MYDATA[nome_programa_text]['wikipedia'] = {}
        MYDATA[nome_programa_text]['wikipedia']['tipo'] = wikipedia
        MYDATA[nome_programa_text]['wikipedia']['url'] = wikipedia_url

    return MYDATA

def generateoutput(msg):
    # this formated one is enough to save into a file
    # if json output is wanted
    json_formated = json.dumps(msg, indent=4)
    table = json.loads(json_formated)
    """
    Current format:
|- style="background: rgb(195, 210, 207) none repeat scroll 0% 50%; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;"
|Alfabetização
|Sim
|Sim
|data-sort-value="1"|Não
|data-sort-value="1"|Não
|data-sort-value="1"|Não
|[http://jiletters.sourceforge.net/ JIlettres]
|data-sort-value="Sim"|[http://sourceforge.net/projects/jiletters/files/ Windows]
|data-sort-value="Sim"|[http://sourceforge.net/projects/jiletters/files/ GNU/Linux]
|data-sort-value="Sim"|[http://sourceforge.net/projects/jiletters/files/ Mac]
|data-sort-value="http://sourceforge.net/projects/jiletters/files/"|[http://sourceforge.net/projects/jiletters/files/ Fonte]
|[https://pt.wikipedia.org/wiki/Gnu_gpl GNU GPL]
|data-sort-value="en"|en
|data-sort-value="1"|Não

    """
    # retrieved using:
    # grep '<tr' tabela_2015.htm  | sort -u | sed "s/.*\(rgb(.*)\).*/\1/"
    COLORCODES = """rgb(072, 142, 192)
rgb(125, 249, 225)
rgb(148, 197, 228)
rgb(158, 197, 228)
rgb(171, 190, 191)
rgb(180, 154, 119)
rgb(192, 168, 1)
rgb(195, 210, 207)
rgb(196, 201, 220)
rgb(196, 202, 172)
rgb(196, 234, 228)
rgb(202, 239, 206)
rgb(205, 216, 217)
rgb(206, 144, 196)
rgb(206, 210, 234)
rgb(221, 197, 213)
rgb(222, 206, 194)
rgb(225, 224, 220)
rgb(252, 205, 236)"""
    colors = COLORCODES.split("\n")
    tr_opts = "none repeat scroll 0% 50%; " + \
        "-moz-background-clip: -moz-initial; " + \
        "-moz-background-origin: -moz-initial; " + \
        "-moz-background-inline-policy: -moz-initial;"
    output = """
{| id="tab" class="wikitable sortable" style="text-align:center; align=center; width: 100%;"
|- class="cabecalho"
! rowspan="2" | Área do conhecimento
! class="sorter-false" colspan="5" | Nível de Ensino
! rowspan="2" | Nome do programa e página oficial
! class="filter-false" rowspan="2" width="64" | Baixar versão Windows
! class="filter-false" rowspan="2" width="64" | Baixar versão GNU/Linux
! class="filter-false" rowspan="2" width="64" | Baixar versão Mac
! class="filter-false" rowspan="2" width="64" | Baixar código fonte
! class="filter-select" rowspan="2" width="88" | Licença
! class="filter-select" rowspan="2" width="64" | Idioma
! class="filter-false"  rowspan="2" | Wikip.
|- class="cabecalho"
! class="filter-false" | EI
! class="filter-false" | AIEF
! class="filter-false" | AFEF
! class="filter-false" | EM
! class="filter-false" | ES

"""
    current_color = -1
    last_area_conhecimento = None
    for app_name in table:
        # removed and parsed all variables before to retrieve here...
        # REALLY?!
        area_conhecimento = table.get(app_name).get('area_conhecimento')
        app_url = table.get(app_name).get('url')
        nivel_ensino_EI = table.get(app_name).get('nivel_ensino').get('EI')
        nivel_ensino_AIEF = table.get(app_name).get('nivel_ensino').get('AIEF')
        nivel_ensino_AFEF = table.get(app_name).get('nivel_ensino').get('AFEF')
        nivel_ensino_EM = table.get(app_name).get('nivel_ensino').get('EM')
        nivel_ensino_ES = table.get(app_name).get('nivel_ensino').get('ES')
        down_win_url = table.get(app_name).get('download').get('windows')
        down_lnx_url = table.get(app_name).get('download').get('linux')
        down_mac_url = table.get(app_name).get('download').get('mac')
        down_src_url = table.get(app_name).get('download').get('source')
        idioma = table.get(app_name).get('idioma')
        licenca = table.get(app_name).get('licenca').get('tipo')
        licenca_url = table.get(app_name).get('licenca').get('url')
        wikipedia = table.get(app_name).get('wikipedia').get('tipo')
        wikipedia_url = table.get(app_name).get('wikipedia').get('url')
        # end of stupid part (a lot)

        # check if area_conhecimento change
        # if so, change row color
        if (area_conhecimento != last_area_conhecimento):
            current_color += 1
            last_area_conhecimento = area_conhecimento
            # just checking for no bugs
            if ((len(colors) - 1) > current_color):
                current_color = 0

        # now build html line
        output += "|- style=\"background: %s %s\"\n" % \
            (colors[current_color], tr_opts)
        output += "|%s\n" % area_conhecimento
        for v in [
            nivel_ensino_EI,
            nivel_ensino_AIEF,
            nivel_ensino_AFEF,
            nivel_ensino_EM,
            nivel_ensino_ES,
            ]:
            if (v == u"Sim") or (v == u"sim"):
                output += "|%s\n" % v
            else:
                output += "|data-sort-value=\"1\"|%s\n" % v
        output += "|[%s %s]\n" % (app_url, app_name)
        # It needs to be fixed for data-sort-value
        output += "|data-sort-value=\"Sim\"|[%s Windows]\n" % down_win_url
        output += "|data-sort-value=\"Sim\"|[%s GNU/Linux]\n" % down_lnx_url
        output += "|data-sort-value=\"Sim\"|[%s Mac]\n" % down_mac_url
        output += "|data-sort-value=\"%s\"|[%s Fonte]\n" % \
            (down_src_url, down_src_url)
        output += "|[%s %s]\n" % (licenca_url, licenca)
        output += "|data-sort-value=\"%s\"|%s" % (idioma, idioma)
        output += "data-sort-value=\"%s\"|[%s %s]\n" % \
            (wikipedia, wikipedia_url, wikipedia)

        #print app_name
        output += "\n"
    return output

def usage():
    print "Use: %s <url>" % sys.argv[0]
    sys.exit(1)

if __name__ == '__main__':
    try:
        URL = sys.argv[1]
    except:
        usage()
    html = getdata(URL)
    j = parsedata(html)
    output = generateoutput(j)
    print output