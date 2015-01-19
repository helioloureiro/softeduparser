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

        # fixing license here...
        license_url = MYDATA[nome_programa_text]['licenca']['url']
        """
        #print "Licenca:", license_url
        if not license_url:
            MYDATA[nome_programa_text]['licenca']['tipo'] = \
                'N/A (Domínio público)'
        elif (re.search("Gnu", license_url)):
            MYDATA[nome_programa_text]['licenca']['tipo'] = 'GNU GPL'
        elif (re.search("Apache", license_url)):
            MYDATA[nome_programa_text]['licenca']['tipo'] = 'Apache 2.0'
        elif (re.search("art%C3%ADstica", license_url)):
            MYDATA[nome_programa_text]['licenca']['tipo'] = 'Licença Artística'
        elif (re.search("MIT", license_url)):
            MYDATA[nome_programa_text]['licenca']['tipo'] = 'MIT/X11'
        elif (re.search("BSD", license_url)):
            MYDATA[nome_programa_text]['licenca']['tipo'] = 'Estilo BSD'
        else:
            MYDATA[nome_programa_text]['licenca']['tipo'] = 'Arrumar'
        """
    return MYDATA

def generateoutput(msg):
    # this formated one is enough to save into a file
    # if json output is wanted
    json_formated = json.dumps(msg, indent=4)
    table = json.loads(json_formated)
    """
    Current format:
<tr style="background: rgb(196, 202, 172) none repeat scroll 0% 50%; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;">
<td>Biologia - Genética
</td>
<td data-sort-value="1">Não
</td>
<td data-sort-value="1">Não
</td>
<td data-sort-value="1">Não
</td>
<td data-sort-value="1">Não
</td>
<td>Sim
</td>
<td><a rel="nofollow" class="external text" href="http://genocad.org">GenoCAD</a>
</td>
<td data-sort-value="Sim"><a rel="nofollow" class="external text" href="http://sourceforge.net/projects/genocad/files">Windows</a>
</td>
<td data-sort-value="Sim"><a rel="nofollow" class="external text" href="http://sourceforge.net/projects/genocad/files">GNU/Linux</a>
</td>
<td data-sort-value="Sim"><a rel="nofollow" class="external text" href="http://sourceforge.net/projects/genocad/files">Mac</a>
</td>
<td data-sort-value="http&#58;//sourceforge.net/projects/genocad/files"><a rel="nofollow" class="external text" href="http://sourceforge.net/projects/genocad/files">Fonte</a>
</td>
<td><a rel="nofollow" class="external text" href="https://en.wikipedia.org/wiki/Apache_License">Apache 2.0</a>
</td>
<td data-sort-value="en">en
</td>
<td data-sort-value="en"><a rel="nofollow" class="external text" href="https://en.wikipedia.org/wiki/GenoCAD">EN</a>
</td></tr>
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
    output = ""
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
        output += "<tr style=\"background: %s %s\">" % \
            (colors[current_color], tr_opts)
        output += "<td>%s</td>" % area_conhecimento
        for v in [
            nivel_ensino_EI,
            nivel_ensino_AIEF,
            nivel_ensino_AFEF,
            nivel_ensino_EM,
            nivel_ensino_ES,
            ]:
            if (v == "Sim") or (v == "sim"):
                output += "<td data-sort-value=\"1\">%s</td>" % v
            else:
                output += "<td>%s</td>" % v
        output += "<td><a rel=\"nofollow\" class=\"external text\" " + \
            "href=\"%s\">%s</a></td>" % (app_url, app_name)
        output += "<td data-sort-value=\"Sim\"><a rel=\"nofollow\" " + \
            "class=\"external text\" " + \
            "href=\"%s\">Windows</a></td>" % down_win_url
        output += "<td data-sort-value=\"Sim\"><a rel=\"nofollow\" " + \
            "class=\"external text\" " + \
            "href=\"%s\">GNU/Linux</a></td>" % down_lnx_url
        output += "<td data-sort-value=\"Sim\"><a rel=\"nofollow\" " + \
            "class=\"external text\" " + \
            "href=\"%s\">Mac</a></td>" % down_mac_url
        output += "<td data-sort-value=\"%s\">" % \
            re.sub(":", "&#58;", down_src_url)
        output += "<a rel=\"nofollow\" class=\"external text\" " + \
            "href=\"%s\">Fonte</a></td>" % down_src_url
        output += "<td><a rel=\"nofollow\" class=\"external text\" " + \
            "href=\"%s\">%s</a></td>" % (licenca_url, licenca)
        output += "<td data-sort-value=\"%s\">%s</td>" % \
            (idioma, idioma)
        # to be fixed...
        output += "<td data-sort-value=\"%s\">" % wikipedia + \
            "<a rel=\"nofollow\" class=\"external text\" " + \
            "href=\"%s\">%s</a></td>" % (wikipedia_url, wikipedia)

        #print app_name
        output += "</tr>\n"
    html = BeautifulSoup(output)
    return html.prettify()

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