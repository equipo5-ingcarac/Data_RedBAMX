import datetime
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from clint.textui import puts, colored, indent

class ScraperSniimHortalizas:
    total_records = 0
    inserted_records = 0

    base_url = 'http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas'
    init_urls = [
        ['Frutas y Hortalizas', '/ConsultaFrutasYHortalizas.aspx', '/ResultadosConsultaFechaFrutasYHortalizas.aspx']
    ]