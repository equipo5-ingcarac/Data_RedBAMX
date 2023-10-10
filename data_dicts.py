import json

with open("idsSIAP.json",encoding='utf8') as json_file:
    dict_ids = json.load(json_file)

dict_cultivos = {k.split('_')[1]:v for k,v in dict_ids.items() if k.startswith("cultivo")}
dict_ciclos = {k.split('_')[1]:v for k,v in dict_ids.items() if k.startswith("ciclo")}
dict_mes = {k.split('_')[1]:v for k,v in dict_ids.items() if k.startswith("mes")}
dict_modalidad = {k.split('_')[1]:v for k,v in dict_ids.items() if k.startswith("modalidad")}

# Url donde se extraeran los datos.
url = "https://nube.siap.gob.mx/avance_agricola/"

# Formato de Descarga de los datos.

payload = {'xajax': 'reporte', # Para obtener la tabla
'xajaxr': '1696449941927', # Timestamp UNIX
'xajaxargs[]': [
    '1', # 1: Desglose por estados, 2: Cultivo total
    '2023', # Anio
    '5', # ID Ciclo
    '3', # ID Modalidad
    '0', # ID Estado (0: Nacional)
    '--',
    '--',
    '7', # ID Cultivo
    '200201',
    '0',
    '1', # 1: Por municipio
    'undefined',
    'undefined',
    'undefined',
    '8' # Valor del mes
    ]
}
# Requerimentos 
headers = {
  'Cookie': 'PHPSESSID=45ri2k73cbp2iptcrufu88p360',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}



