import datetime
import os
import random
import time
from math import ceil
from bs4 import BeautifulSoup
import pandas as pd
import requests
from clint.textui import puts, colored, indent

def normalize(s):
    """
    Normalizar string parara eliminar espacios y mayusculas
    """
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper()).replace(' ','_').lower().replace('/','')
    return s

def get_previous_week(dt):
    """
    Obtener el numero de semana directamente anterior, si la semana es la primera del mes, regresar 4 (ultima semana del mes anterior)
    """
    first_day = dt.replace(day=1)
    day_of_month = dt.day

    if(first_day.weekday() == 6):
       adjusted_dom = (1 + first_day.weekday()) / 7
    else:
       adjusted_dom = day_of_month + first_day.weekday()

    week_no = int(ceil(adjusted_dom/7.0))
    return week_no - 1 if week_no > 1 else 4


class ScrapperMarketAgriculture:
    total_records = 0
    inserted_records = 0
    total_rows = 0
    

    base_url = 'http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas'
    init_urls = [
        ['Frutas y Hortalizas', '/ConsultaFrutasYHortalizas.aspx', '/ResultadosConsultaFechaFrutasYHortalizas.aspx']
    ]

    headers = {
        "Accept" : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        "Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "en-US,en;q=0.9",
        "Cache-Control" : "max-age=0",
        "Connection" : "keep-alive",
        "Host" : "www.economia-sniim.gob.mx",
        "Referer" : "http://www.economia-sniim.gob.mx/nuevo/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaFrutasYHortalizas.aspx?SubOpcion=4",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    def __init__(self, *args, **kwargs):
        pass

    def read_category(self, category, url, url_form):
        """
        Genera el payload necesario para el request al SNIIM
        """
        category_page = requests.get(self.base_url + url)
        category_page = BeautifulSoup(category_page.content, features="html.parser")

        products = [(product.getText(), product['value'], ) for product in category_page.select_one('select#ddlProducto').find_all('option')]

        for product in products:
            product_name, product_id = product
            if product_id == '-1':
                continue

            puts(colored.magenta("Producto: {}".format(str(product_name))))

            today = datetime.datetime.today()
            for year in range(2020, today.year + 1):
                if year == today.year:
                    end_date = '{0}'.format(today.strftime('%d/%m/%Y'))
                else:
                    end_date='01/01/{0}'.format(str(year + 1))
                
                payload = {
                    'fechaInicio':'01/01/{0}'.format(str(year)),
                    'fechaFinal': end_date,
                    'ProductoId':product_id,
                    'OrigenId':'-1',
                    'Origen':'Todos',
                    'DestinoId':'-1',
                    'Destino':'Todos',
                    'PreciosPorId':'2',
                    'RegistrosPorPagina':'20000'
                }

                if not self.gather_prices(payload, url_form, product_name, year):
                    next

        return

    def scraping(self):
        self.total_records = 0
        self.inserted_records = 0

        if not os.path.exists("./data/sniim"):
            os.mkdir("./data/sniim")

        for category, url, url_form in self.init_urls:
            self.read_category(category, url, url_form)
        
        with open("./info_sniim.txt", 'w') as f:
            f.write("Archivos sobre personas desaparecidas\n")
            info = f"""
            Datos de precios registrados a nivel nacional para distintos productos agricolas en distintas centrales de abasto del pais.

            Los datos se obtuvieron del Sistema Nacional de Informacion e Integracion de Mercados de la Secretaria de Economia
            con fecha desde el 1 de enero de 2020 hasta la fecha ({datetime.datetime.today().strftime("%d-%m-%Y")})

            Los datos son recibidos en forma de tablas HTML y almacenados en archivos CSVs para su posterior tratamiento.
            """ 
            f.write(info + '\n')
            f.write("Descargado el " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("Desde: " + self.base_url + "\n")
            f.write(f"Registros recuperados: {self.total_rows}")

    def gather_prices(self, payload, url_form, product_name, year):

        if os.path.exists(f"./data/sniim/{normalize(product_name).split('_-_')[0]}_{year}.csv"):
            #puts(colored.red(f"Ya existe registro: {normalize(product_name).split('_-_')[0]}_{year}.csv"))
            return

        #puts(colored.blue("Peticion: {}".format(str(payload))))

        response = requests.get(self.base_url + url_form, params=payload, headers=self.headers)

        if response.status_code != 200:
            puts(colored.red("Error en la peticion HTTP: {}".format(str(response.text))))
            return False

        product_prices = BeautifulSoup(response.content, features="html.parser")

        try:
            table_prices = product_prices.select_one('table#tblResultados')
        
        except Exception as error:
            puts(colored.red("Error en el parseo: {}".format(str(error))))
            return False

        fields = ('fecha', 'presentacion', 'origen', 'destino', 'precio_min', 'precio_max', 'precio_frec', 'obs')
        counter_row = 0
        
        df = pd.DataFrame(columns=fields)

        for observation in table_prices.find_all('tr'):
            if counter_row > 1:
                row = {}
                counter_field = 0

                for metric in observation.find_all('td'):
                    row[fields[counter_field]] = [metric.getText()]
                    counter_field += 1
                
                row_df = pd.DataFrame(row)
                df = pd.concat([df,row_df], ignore_index=True)

            self.total_records += 1
            counter_row += 1
            
        
        if not df.empty:
            self.total_rows += df.shape[0]
            df.to_csv(f"./data/sniim/{normalize(product_name).split('_-_')[0]}_{year}.csv", index=False)
            
        time.sleep(random.uniform(0,0.5))
        return True


if __name__ == '__main__':
    agricola = ScrapperMarketAgriculture()
    agricola.scraping()
