# Proyecto: ¿Es posible predecir excedentes agrícolas?

## Obtención y limpieza de datos

Los requisitos para esta primera parte son los siguientes:

1. Un archivo `README.md` que expñlique cual sería el objetivo final del análisis (aunque fuera en forma muy genética) y que justifique las acciones que se van a tomar (cuales fuentes se usan, cuales variables se retienen, el tipo de limpieza de los datos, las tablas tidy seleccionadas,…).

2. Un script o libreta que descargue datos de al menos dos fuentes diferentes, y que genere un archivo texto con la descripción de las fuentes, las fechas de descarga y de ser posible la descripción (o enlaces) que expliquen la naturaleza de los datos descargados. Si los datos venían sin explicación, agregar la explicación propia para simplificar el proceso.

3. Una libreta o script que transforme y utilice los datos de acuerdo a su tipo, selecciones la información que se desea utilizar y se generen los Dataframes necesarios.

4. Un diccionario de datos por cada dataframe

Como extra se considerará la implementación de algún método para asegurar la calidad de los datos.

Mas informacion sobre los requisitos/diferentes opciones del proyecto en [este link](https://mcd-unison.github.io/ing-caract/proyecto1/)

# Introducción

Red Banmax ha solicitado el análisis de la red de datos del sector agroindustrial para poder tener una predicción de sobrantes de cosecha de diversos frutos y leguminosas que no entra en el mercado, ya sea por cuestiones estéticas o por razones económicas. Estas cosechas son desperdiciadas por los agricultores, ya que han perdido su valor en el mercado, aun siendo que sean aptas para el consumo. RedBanmax propone adquirir este desperdicio como donación para poderla entregar en su banco de alimentos.

<p align="center">
    <img src="https://bamx.org.mx/wp-content/uploads/2022/05/RED-BAMX.png" width="341" height="132">
</p>

Red de Bancos de Alimentos (Red Bamx) es una OSC sin fines de lucro y apartidista, compuesto por 53 Bancos de Alimentos. Estos rescatan alimento a través de toda la cadena de distribución para llevarlo a familias, comunidades e instituciones que lo necesiten.

# Datos

Los datos se han recopilado de varias fuentes del gobierno de México:
-	Servicio de Información Agroalimentaria y Pesquera de la Secretaria de Agricultura y Desarrollo Rural.
-	Sistema Nacional de e Integración de mercados (SNIIM) de la secretaria de economía.


## SIAP

El Servicio de Información Agroalimentaria y Pesquera (SIAP), órgano administrativo desconcentrado de la Secretaría de Agricultura es el encargado de generar estadística e información geográfica en materia agroalimentaria, promoviendo además, la concurrencia y coordinación las demás dependencias y entidades de la Administración Pública Federal, de los Gobiernos Estatales, Municipales y de la Ciudad de México, para la implementación del Sistema Nacional de Información para el Desarrollo Rural Sustentable.

## Descarga y Limpieza de datos

Se adquirieron datos de la página del SIAP https://nube.siap.gob.mx/avance_agricola/, cuales son referentes a información estadística de 64 cultivos que son sembrados y cosechados a lo largo de México.

En la libreta ``API_SIAP_Descarga.ipynb`` se pueden descargar todos los datos referentes a todos los productos sembrados y cultivados en cada uno de los municipios de México, del 2020 al 2021. Este archivo utiliza web scaping para adquirir tablas de cada uno de los productos en XML, y transformándolos en `*.csv`.

Una vez descargado todos los datos, la libreta `clean_data_SIAP` concatena, procesa y limpia los datos en un sola base de datos Tidy para almacenarlos en un archivo con formato ``parquet``.

## SNIIM

Los datos referentes a los precios de diversos productos agrícolas fueron obtenidos a partir de la página del [Sistema Nacional de Información e Integración de Mercados](http://www.economia-sniim.gob.mx/nuevo/) de la Secretaría de Economía, la cual ofrece datos sobre los precios de diversos productos agrícolas en distintos puntos de venta en el país.

### Descarga y limpieza de los datos

Los datos ofrecidos en esta página se presentan en forma de tablas HTML. Para poder recuperar y almacenar estos datos, se utilizó un web scraper basado en [este proyecto](https://github.com/mxabierto/scraper-sniim) desarrollado por la iniciativa México Abierto.

El script para obtener estos datos se encuentra en el archivo `agriculture.py`. Este script puede ser ejecutado directamente desde la terminal, navegando a la carpeta del proyecto y ejecutando el siguiente comando:

```
python3 agriculture.py
```

O bien, se puede ejecutar directamente en una libreta ejecutando la siguiente linea en una celda:

```
!python3 agriculture.py
```


Una vez recuperados los datos para cada producto, estos se almacenan en diversos archivos de tipo csv en el directorio `./data/sniim`, los nombres para cada muestra son de la forma `producto_año.csv`. **Es importante notar que debido a la cantidad de datos recuperados, este script puede tomar entre 1 y 3 horas en recuperar los datos, dependiendo de diversos factores.**

Una vez almacendaos los datos los datos, en la libreta `Data_SNIIM.ipynb`, los datos son recopilados en una dataframe de pandas, se limpian los datos faltantes y se realizan los procesamientos necesarios para que cada columna tenga el tipo de dato que le corresponde (`datetime`,`float`,`etc`).


# Integrantes

- Iván Dario Dávila Peralta
- David Peña Peralta
- Jesús Martín Gaytán Villarreal
