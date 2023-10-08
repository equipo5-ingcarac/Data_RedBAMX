# Proyecto: ¿Es posible predecir excedentes agrícolas?

## Obtención y limpieza de datos

Los requisitos para esta primera parte son los siguientes:

1. Un archivo `README.md` que expñlique cual sería el objetivo final del análisis (aunque fuera en forma muy genética) y que justifique las acciones que se van a tomar (cuales fuentes se usan, cuales variables se retienen, el tipo de limpieza de los datos, las tablas tidy seleccionadas,…).

2. Un script o libreta que descargue datos de al menos dos fuentes diferentes, y que genere un archivo texto con la descripción de las fuentes, las fechas de descarga y de ser posible la descripción (o enlaces) que expliquen la naturaleza de los datos descargados. Si los datos venían sin explicación, agregar la explicación propia para simplificar el proceso.

3. Una libreta o script que transforme y utilice los datos de acuerdo a su tipo, selecciones la información que se desea utilizar y se generen los Dataframes necesarios.

4. Un diccionario de datos por cada dataframe

Como extra se considerará la implementación de algún método para asegurar la calidad de los datos.

Mas informacion sobre los requisitos/diferentes opciones del proyecto en [este link](https://mcd-unison.github.io/ing-caract/proyecto1/)

# Datos

## SNIIM

Los datos referentes a los precios de diversos productos agrícolas fueron obtenidos a partir de la página del [Sistema Nacional de Información e Integración de Mercados](http://www.economia-sniim.gob.mx/nuevo/) de la Secretaría de Economía, la cual ofrece datos sobre los precios de diversos productos agrícolas en distintos puntos de venta en el país.

### Descarga y limpieza de los datos

Los datos ofrecidos en esta página se presentan en forma de tablas HTML. Para poder recuperar y almacenar estos datos, se utilizó un web scraper basado en [este proyecto](https://github.com/mxabierto/scraper-sniim) desarrollado por la iniciativa México Abierto.

El script para obtener estos datos se encuentra en el archivo `agriculture.py`. Este script puede ser ejecutado directamente desde la terminal, navegando a la carpeta del proyecto y ejecutando el siguiente comando:

`python3 agriculture.py`

O bien, se puede ejecutar directamente en una libreta ejecutando la siguiente linea en una celda:

`!python3 agriculture.py`

Una vez recuperados los datos para cada producto, estos se almacenan en diversos archivos de tipo csv en el directorio `./data/sniim`, los nombres para cada muestra son de la forma `producto_año.csv`. **Es importante notar que debido a la cantidad de datos recuperados, este script puede tomar entre 1 y 3 horas en recuperar los datos, dependiendo de diversos factores.**

Una vez almacendaos los datos los datos, en la libreta `Data_SNIIM.ipynb`, los datos son recopilados en una dataframe de pandas, se limpian los datos faltantes y se realizan los procesamientos necesarios para que cada columna tenga el tipo de dato que le corresponde (`datetime`,`float`,`etc`).

# Integrantes

- Iván Dario Dávila Peralta
- David Peña Peralta
- Jesús Martín Gaytán Villarreal
