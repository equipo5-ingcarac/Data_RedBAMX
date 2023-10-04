import datetime
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from math import ceil
from clint.textui import puts, colored, indent

def normalize(s):
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
    

    base_url = 'http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas'
    init_urls = [
        #['Frutas y Hortalizas', '/ConsultaFrutasYHortalizas.aspx', '/ResultadosConsultaFechaFrutasYHortalizas.aspx'],
        #['Flores', '/ConsultaFlores.aspx?SubOpcion=5', '/ResultadosConsultaFechaFlores.aspx'],
        # ['Granos', '/ConsultaGranos.aspx?SubOpcion=6', '/ResultadosConsultaFechaGranos.aspx']
        ['Aceites', '/ConsultaAceites.aspx?SubOpcion=8', '/ResultadosConsultaFechaAceite.aspx']
    ]

    def __init__(self, *args, **kwargs):
        pass

    def read_category(self, category, url, url_form):
        category_page = requests.get(self.base_url + url)
        category_page = BeautifulSoup(category_page.content, features="html.parser")

        products = [(product.getText(), product['value'], ) for product in category_page.select_one('select#ddlProducto').find_all('option')]

        for product in products:
            product_name, product_id = product
            if product_id == '-1':
                continue

            with indent(4):
                puts(colored.magenta("Producto: {}".format(str(product_name))))

            today = datetime.datetime.today()
            deleta = datetime.timedelta(days=-1)
            if category == 'Aceites':
                payload = {
                        'Semana': get_previous_week(today),
                        'Mes':9,
                        'Anio':2023,
                        'AceiteId':product_id,
                        'DestinoId':'-1',
                        'Destino':'Todos',
                        'RegistrosPorPagina':'1000'
                    }

                if not self.gather_prices(payload, url_form, product_name, category):
                    next
            elif category == 'Frutas y Hortalizas':
                payload = {
                        'fechaInicio':'{}'.format(today.strftime('%d/%m/%Y')),
                        'fechaFinal':'{}'.format((today).strftime('%d/%m/%Y')),
                        'ProductoId':product_id,
                        'OrigenId':'-1',
                        'Origen':'Todos',
                        'DestinoId':'-1',
                        'Destino':'Todos',
                        'PreciosPorId':'2',
                        'RegistrosPorPagina':'1000'
                    }

                if not self.gather_prices(payload, url_form, product_name, category):
                    continue

        return

    def scraping(self):
        self.total_records = 0
        self.inserted_records = 0

        for category, url, url_form in self.init_urls:
            self.read_category(category, url, url_form)
            time.sleep(30)

    def gather_prices(self, payload, url_form, product_name, category):

        with indent(4):
            puts(colored.blue("Peticion: {}".format(str(payload))))

        response = requests.get(self.base_url + url_form, params=payload)

        if response.status_code != 200:
            with indent(4):
                puts(colored.red("Error en la peticion HTTP: {}".format(str(response.text))))
            return False

        product_prices = BeautifulSoup(response.content, features="html.parser")

        # pagination = product_prices.select_one('span#lblPaginacion').getText().split(' ')[-1]

        try:
            table_prices = product_prices.select_one('table#tblResultados')
        
        except Exception as error:
            with indent(4):
                puts(colored.red("Error en el parseo: {}".format(str(error))))
            return False

        fields = ('fecha', 'presentacion', 'origen', 'destino', 'precio_min', 'precio_max', 'precio_frec', 'obs')
        counter_row = 0
        
        df = pd.DataFrame(columns=fields)

        # print(table_prices)
        for observation in table_prices.find_all('tr'):
            if counter_row > 1:
                row = {}
                counter_field = 0

                for metric in observation.find_all('td'):
                    row[fields[counter_field]] = metric.getText()
                    counter_field += 1

                with indent(4):
                    puts(colored.yellow("Insertando: {}".format(str(row))))
                
                df = df.append(row,ignore_index=True)

                # if self.mongo.insert_one(row):
                #     self.inserted_records += 1
                #     with indent(4):
                #         puts(colored.green("Insertado: {}".format(str(row))))
                # else:
                #     with indent(4):
                #         puts(colored.red("No Insertado: {}".format(str(row))))

            self.total_records += 1
            counter_row += 1
            
        
        if not df.empty:
            df.to_csv(f"./data/sniim/{normalize(category)}/{normalize(product_name).split('_-_')[0]}.csv", index=False)
            
        return True


if __name__ == '__main__':
    agricola = ScrapperMarketAgriculture()
    agricola.scraping()

#     vacas = ScrapperMarketLiveStock()
#     vacas.scraping()
