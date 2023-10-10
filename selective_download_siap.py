import selector as s
import data_dicts as dd
import os
import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

data_dir = "./data/siap"

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

"""
selector_data = {
    'Anio':[],
    'Ciclos':['Otoño - Invierno'],
    'Cultivos':['Aguacate'],
    'Meses':['Enero'],
    'Modalidad':['Riego']
}
"""

rel_data_filter = {
    'Anio': s.anios,
    'Ciclos':s.ciclos,
    'Cultivos':s.cultivos,
    'Meses':s.meses,
    'Modalidad':s.modalidad
}

def download_selector(selector):
    sel_keys = selector.keys()
    for u in sel_keys:
        if len(selector[u]) == 0:
            selector[u] = rel_data_filter[u]
    for year in selector['Anio']:
        dd.payload['xajaxargs[]'][1] = str(year)
        for key_mes in selector['Meses']:
            dd.payload['xajaxargs[]'][14] = dd.dict_mes[key_mes]

            for key_cultivo in selector['Cultivos']:
                if dd.dict_cultivos[key_cultivo] == "0":
                    continue
                    
                if os.path.exists(f"{data_dir}/{key_cultivo.lower().replace(' ','_')}_{key_mes.lower()}_{year}.csv"):
                    continue

                dd.payload['xajaxargs[]'][7] = dd.dict_cultivos[key_cultivo]

                response = requests.request("POST", dd.url, headers=dd.headers, data=dd.payload, verify=False)
                response.encoding='ISO-8859-1'

                #extract the cdata as a string
                root = etree.fromstring(response.content)
                cd = root.xpath('//cmd//text()')[0]

                parsed_html = BeautifulSoup(str(cd),"lxml")
                parsed_table = parsed_html.body.find("table")

                if parsed_table is None:
                    continue

                df_iter = pd.read_html(str(parsed_html.body.find("table")))[0]

                df_iter.to_csv(f"{data_dir}/{key_cultivo.lower().replace(' ','_')}_{key_mes.lower()}_{year}.csv",index=False)
                time.sleep(0.1)

download_selector(s.selector_data)