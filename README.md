# ESCatastroLib

La librería ESCatastroLib proporciona una interfaz sencilla para consultar el Catastro de España y obtener información geográfica precisa. Con esta librería, puedes acceder a datos como la ubicación de parcelas, características de construcción y valores geográficos.

# Clases

## Clase Municipio

Representa un municipio (ciudad o pueblo).

**Atributos/Inputs del constructor**

`provincia (str)`: El nombre de la provincia donde se encuentra el municipio.  Un valor por
defecto se establece y se puede proporcionar un valor diferente si es necesario.

`municipio (str, opcional)`:  El nombre del municipio. Si no se proporciona al crear una instancia, se
lanzará una excepción.  Si se especifica, debe coincidir al menos parcialmente con el nombre de un municipio válido encontrado en la base de datos o fuente de datos del sistema.

**Excepciones**

`Exception`: Si no se especifica el `municipio` o si es inválido, o si no corresponde a un municipio válido
en la base de datos del sistema. Se lanzará una excepción con la lista de municipios en ese caso.

## Clase Calle

La clase `Calle` es una entidad que representa una calle. 

**Atributos/Inputs del constructor:**

`municipio (Municipio)` : Objeto que representa el Municipio al que pertenece la calle.

`nombre_calle (str, opcional)` : El nombre de la calle asignada.

`tipo_via (str, opcional)` : El tipo de vía de la calle asignada. Se trata de una serie de siglas que puedes consultar en `utils.listar_tipos_via()`

**Excepciones**

`Exception`: Si no existe la calle, o la calle tiene más de un tipo de vía. Devuelve una lista de calles en formato `TipoVia NombreCalle`

## Clase ParcelaCatastral

Representa una parcela catastral.


**Inputs del constructor:**

* `rc (str, opcional)`: La referencia catastral de la parcela. Por defecto es `None`. Puede ser proporcionada
sola; también puede haber otros parámetros para buscar una parcela específica en el sistema.
* `provincia (str, opcional)`: El nombre de la provincia. Por defecto es `None`.  Se usa para
buscar por dirección o parcela.
* `municipio (str, opcional)`: El nombre del municipio. Por defecto es `None`. Se usa para buscar
por dirección o parcela.


* `poligono (int, opcional)`: El número del polígono. Por defecto es `None` y puede ser específico para zonas rurales.
* `parcela (int, opcional)`:  El número de la parcela. Por defecto es `None` y se usa para buscar zonas rurales.
  


* `tipo_via (str, opcional)`: El tipo de carretera en la dirección. Por defecto es `None` y es útil al buscar
direcciones urbanas.
* `calle (str, opcional)`:  El nombre de la calle en la dirección. Por defecto es `None` y es útil para
encontrar ubicaciones urbanas
* `numero (str, opcional)`: El número de la calle en la dirección. Por defecto es `None` y se usa para encontrar
ubicaciones urbanas por número.

**Excepciones:**
* `ValueError`:  Si no has proporcionado suficiente información para realizar la búsqueda, o si el RC hace
referencia a una MetaParcela.
* `ErrorServidorCatastro`: Si hay un error con la base de datos del Catastral Server.


**Atributos:**

* `rc (str)`: La referencia catastral de la parcela.
* `provincia (str)`:  El nombre de la provincia.
* `municipio (str)`: El nombre del municipio.
* `poligono (int)`:  El número del polígono. Solo se usa para terrenos rurales.
* `parcela (int)`:  El número de la parcela. Solo se usa para terrenos rurales.
* `tipo_via (str)`: El tipo de carretera en la dirección.
* `calle (str)`:  El nombre de la calle en la dirección.
* `numero (str)`:  El número de la calle en la dirección.
* `url_croquis (str)`: La URL del croquis de la parcela.
* `tipo (str)`: El tipo de terreno (urbano o rural).
* `antiguedad (str)`: La edad de la parcela (solo en lotes urbanos)
* `uso (str)`:  El uso de la parcela (solo en lotes urbanos)
* `nombre_paraje (str)`:  El nombre del área, solo se usa para terrenos rurales.
* `regiones (list)`: Una lista de regiones en la parcela con una descripción y superficie.
* `centroide (dict)`:  Las coordenadas del centroide de la parcela. (Latitud y longitud)
* `geometria (list)`:  Una lista de puntos que representan la geometría de la parcela. (Latitud y longitud)


## Clase MetaParcela

Representa una  MetaParcela, es decir, una gran parcela catastral con varias referencias catastrales (Parcels
Catastrales más pequeñas).


**Atributos/Inputs del constructor:**

*  `rc (Union[str,None])`: La referencia catastral de la MetaParcela. Puede ser proporcionada como `None`.
* `provincia (Union[str,None])`:  El nombre de la provincia donde se encuentra la MetaParcela. Por
defecto, es `None`, lo que permite usar nombres generales.
* `municipio (Union[str,None])`: El nombre del municipio donde se encuentra la MetaParcela. Por
defecto, es `None`, lo que permite usar nombres generales.
* `poligono (Union[int,None])`: El número del polígono en el que se encuentra la MetaParcela. Se utiliza para encontrar
una parcela específica.
* `parcela (Union[int,None])`: El número de parcelas dentro de la MetaParcela. Se utiliza para encontrar una parcela
específica.
* `tipo_via (Union[str,None])`: Tipo de camino en la dirección de la MetaParcela. Se usa para encontrar una parcela
específica.
* `calle (Union[str,None])`: Nombre de la calle de la MetaParcela. Se usa para encontrar una parcela específica.
* `numero (Union[str,None])`: Número de casa de la MetaParcela.

**Atributos:**

* `rc (str)`: La referencia catastral de la MetaParcela.
* `parcelas (list)`: Una lista de ParcelaCatastral que representan las parcelas que componen la MetaParcela.
  


# Funciones útiles

## `comprobar_errores()`

Comprueba si la respuesta contiene errores.

**Argumentos**:
* `respuesta (dict)`: El diccionario de respuesta.

**Excepciones**:
* El que venga de `lanzar_excepcion` (`ErrorServidorCatastro`): Si se encuentra un error en la respuesta.

**Devuelve**:
* `True` si no se encuentran errores

## `listar_provincias()`

Obtiene una lista de provincias.

**Devuelve**:
* `list`: Una lista de nombres de provincias.

## `listar_municipios()`

Obtiene una lista de municipios de España.

**Argumentos**:
* `provincia (str)`: El nombre de la provincia. Preferentemente en mayúsculas o capitalizado.
* `municipio (str, optional)`: El nombre del municipio. Por defecto es None.

**Devuelve**:
* `List[str]`: Una lista de nombres de municipios.

**Excepciones**:
* `Exception`: Si la provincia no existe. Muestra un mensaje con las provincias disponibles.

## `listar_tipos_via()`

Retorna una lista de los tipos de vía disponibles.

**Devuelve**:
* `list`: Una lista de los tipos de vía disponibles.

## `listar_calles()`

Devuelve una lista de calles para una provincia y municipio dados.

**Argumentos**:
* `provincia (str)`: El nombre de la provincia.
* `municipio (str)`: El nombre del municipio.

**Devuelve**:
* `list`: Una lista de calles en formato "tipo de vía nombre de vía".


# Conversores

Las clases `ParcelaCatastral` y `MetaParcela` incluyen métodos para exportar los datos en diferentes formatos. Estos métodos permiten convertir los datos de las parcelas en formatos útiles para análisis y almacenamiento.

## Métodos disponibles

### `to_dataframe()`

Convierte la parcela o metaparcela en un DataFrame de GeoPandas, el cual incluye información geográfica.

**Devuelve**:
* `gpd.GeoDataFrame`: Un DataFrame que contiene los datos de la parcela o metaparcela.

### `to_json()`
Convierte la parcela o metaparcela en un archivo JSON.

**Argumentos**:

`filename (str, opcional)`: Nombre del archivo donde guardar el JSON. Si no se proporciona, devuelve el JSON como cadena.

**Devuelve**:

`str`: Una cadena JSON que contiene los datos de la parcela o metaparcela, en caso de no añadir `filename`.

Un archivo con el `filename` en caso de añadirlo.

### `to_csv()`
Convierte la parcela o metaparcela en un archivo CSV.

**Argumentos**:

`filename (str, opcional)`: Nombre del archivo donde guardar el JSON. Si no se proporciona, devuelve el CSV como cadena.

**Devuelve**:

`str`: Una cadena CSV que contiene los datos de la parcela o metaparcela, en caso de no añadir `filename`.

Un archivo con el `filename` en caso de añadirlo.

# `to_shapefile()`
Guarda la parcela o metaparcela como un archivo Shapefile.

**Argumentos**:

`filename (str)`: El nombre del archivo Shapefile a guardar.

**Devuelve**:

Un archivo con el `filename`.

### `to_parquet()`
Guarda la parcela o metaparcela como un archivo Parquet.

**Argumentos**:

`filename (str)`: El nombre del archivo Parquet a guardar.

**Devuelve**:

Un archivo con el `filename`.

# Y esta librería... ¿Cómo se usa?
¡Buena pregunta! Os dejo algunos ejemplos:

```python
from ESCatastroLib import Municipio, Calle, ParcelaCatastral, MetaParcela
from ESCatastroLib.utils import listar_provincias, listar_tipos_via, listar_calles, listar_municipios

print(listar_provincias())
# > ['A CORUÑA', 'ALACANT', 'ALBACETE', 'ALMERIA', 'ASTURIAS', 'AVILA', 'BADAJOZ', ...]

print(listar_tipos_via())
# > {'AC': 'ACCESO', 'AG': 'AGREGADO', 'AL': 'ALDEA, ALAMEDA', 'AN': 'ANDADOR', 'AR': 'AREA, ARRABAL', 'AU': 'AUTOPISTA', 'AV': 'AVENIDA', ... }

print(listar_municipios(provincia='Granada'))
# > ['AGRON', 'ALAMEDILLA', 'ALBOLOTE', 'ALBONDON', 'ALBUÑAN', 'ALBUÑOL', 'ALBUÑUELAS', 'ALDEIRE', ...]

print(listar_municipios(provincia='Granada', municipio='B'))
# > ['ALBOLOTE', 'ALBONDON', 'ALBUÑAN', 'ALBUÑOL', 'ALBUÑUELAS', 'BAZA', 'BEAS DE GRANADA', 'BEAS DE GUADIX', ...]

print(listar_calles(provincia='Granada', municipio = 'Baza'))
# > ['CL  PARAISO (BAU)', 'CL A ALTOS', 'CL A PAVON', 'CL ABAD NAVARRO', 'PZ ABASTOS', 'CL ABEDUL', 'CL ABELARDO LOPEZ DE AYALA', 'CL ABENAMAR', 'CL ACEQUITA', 'CL ADARVE MONJAS', 'CL ADMINISTRADOR', 'TR ADUANA', 'CL ADUANA', 'CL AGUILA', 'CL AIRE', 'CL AIXA', ...]

municipio = Municipio(provincia='Granada')
# [!] Exception: Error al asignar municipio. No has especificado el municipio. Estos son los municipios disponibles: AGRON,ALAMEDILLA,ALBOLOTE,ALBONDON ...

municipio = Municipio(provincia='Granada', municipio='B')
# [!] Exception: Error al asignar municipio. No has especificado el municipio completamente. Estos son los municipios disponibles con esa búsqueda: ALBOLOTE,ALBONDON,ALBUÑAN,ALBUÑOL,ALBUÑUELAS,BAZA,BEAS DE GRANADA, ...

municipio = Municipio(provincia='Granada', municipio='Baza')
# [OK] {'provincia': 'Granada', 'municipio': 'BAZA'}

calle = Calle(municipio=municipio)
# [!] Exception: Error al asignar calle. No has especificado la calle. Estas son las calles disponibles: CL  PARAISO (BAU),CL A ALTOS,CL A PAVON,CL ABAD NAVARRO,PZ ABASTOS,CL ABEDUL,CL ABELARDO LOPEZ DE AYALA, ...

calle = Calle(municipio=municipio, nombre_calle= 'M')
# [!] Exception: Error al asignar calle. No has especificado la calle completamente, o ese nombre está en varios lados (indica el tipo de vía que aparezca al principio de la vía como PZ o CL). Estas son las calles disponibles con esa búsqueda: CL ABENAMAR,CL ADARVE MONJAS,CL ADMINISTRADOR,CL ALAMEDA,CL ALAMILLOS,CL ALAMILLOS ALTOS,CL ALAMILLOS BAJOS,CL ALAMO,CL ALGAMASILLA,CL ALHAMBRA,...

calle = Calle(municipio=municipio, nombre_calle='Mayor', tipo_via='PL')
# [!] ErrorServidorCatastro: Error del Catastro. NO HAY COINCIDENCIAS EN LA BÚSQUEDA DE VÍAS

calle = Calle(municipio=municipio, nombre_calle='Mayor', tipo_via='PZ')
# [OK] {'calle': 'MAYOR', 'tipo_via': 'PZ', 'municipio': <ESCatastroLib.models.Municipio.Municipio at 0x7f0075209e10>}

pc = ParcelaCatastral(rc='22113U490470815583UK')
# [!] ErrorServidorCatastro: Error del Catastro. NO EXISTE NINGÚN INMUEBLE CON LOS PARÁMETROS INDICADOS

pc = ParcelaCatastral(rc='28067A023001490000FJ')
# [OK] {'rc': '28067A023001490000FJ', 'url_croquis': 'https://www1.sedecatastro.gob.es/CYCBienInmueble/SECImprimirCroquisYDatos.aspx?refcat=28067A023001490000FJ', 'municipio': 'GUADALIX DE LA SIERRA', 'provincia': 'MADRID', 'tipo': 'Rústico', 'parcela': '149', 'poligono': '23', 'nombre_paraje': 'PE¥ARRUBIA', 'regiones': [{'descripcion': 'PRADOS O PRADERAS', 'superficie': '250266'}, {'descripcion': 'MONTE BAJO', 'superficie': '187652'}, {'descripcion': 'PASTOS', 'superficie': '1814'}], 'centroide': {'x': '40.76845', 'y': '-3.672895'}, 'geometria': [{'x': '40.764879', 'y': '-3.678524'}, {'x': '40.765874', 'y': '-3.678059'}, ...], 'superficie': 439732.0}

pc = ParcelaCatastral(rc='1541506VK4714B0002PK')
# [OK] {'rc': '1541506VK4714B0002PK', 'url_croquis': 'https://www1.sedecatastro.gob.es/CYCBienInmueble/SECImprimirCroquisYDatos.aspx?refcat=1541506VK4714B0002PK', 'municipio': 'MADRID', 'provincia': 'MADRID', 'tipo': 'Urbano', 'calle': 'CL ALFONSO XII', 'numero': '34', 'antiguedad': '1915', 'uso': 'Almacen-Estacionamiento.Uso Residencial', 'regiones': [{'descripcion': 'APARCAMIENTO', 'superficie': '37'}, {'descripcion': 'ELEMENTOS COMUNES', 'superficie': '2'}], 'centroide': {'x': '40.414193', 'y': '-3.689266'}, 'geometria': [{'x': '40.414358', 'y': '-3.689164'}, {'x': '40.414359', 'y': '-3.689094'}, {'x': '40.414288', 'y': '-3.689092'}, ...], 'superficie': 39.0}

pc = ParcelaCatastral(provincia='Granada', municipio='Baza', poligono=16, parcela=128)
# [OK] {'provincia': 'GRANADA', 'municipio': 'BAZA', 'poligono': '16', 'parcela': '128', 'rc': '18024A016001280000GY', 'url_croquis': 'https://www1.sedecatastro.gob.es/CYCBienInmueble/SECImprimirCroquisYDatos.aspx?refcat=18024A016001280000GY', 'tipo': 'Rústico', 'nombre_paraje': 'BAICO', 'regiones': [{'descripcion': 'LABOR O LABRADÍO REGADÍO', 'superficie': '14608'}], 'centroide': {'x': '37.544352', 'y': '-2.742683'}, 'geometria': [{'x': '37.543611', 'y': '-2.74347'}, {'x': '37.543717', 'y': '-2.743522'}, {'x': '37.543945', 'y': '-2.743435'}, ...], 'superficie': 14608.0}


pc = ParcelaCatastral(provincia='Madrid', municipio='Madrid', poligono='1', parcela='1')
# [!] ErrorServidorCatastro: Error del Catastro. Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.

mp = MetaParcela(provincia='Madrid', municipio='Madrid', poligono='1', parcela='1')
# [OK] {'provincia': 'Madrid', 'municipio': 'Madrid', 'poligono': '1', 'parcela': '1', 'parcelas': [<ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7f61b2298040>, <ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7f61b13407f0>, <ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7f61b223a830>, <ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7f61b223a350>, <ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7f61b13400a0>]}

pc = ParcelaCatastral(provincia='Granada', municipio='Guadix', tipo_via='CL', calle='Largacha', numero=6)
# [!] ErrorServidorCatastro: Error del Catastro. Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.


pc = ParcelaCatastral(provincia='Granada', municipio='Guadix', tipo_via='PZ', calle='Catedral', numero=1)
# [OK] {'provincia': 'GRANADA', 'municipio': 'GUADIX', 'calle': 'PZ CATEDRAL', 'numero': '1', 'rc': '8085801VG8288E0001FA', 'url_croquis': 'https://www1.sedecatastro.gob.es/CYCBienInmueble/SECImprimirCroquisYDatos.aspx?refcat=8085801VG8288E0001FA', 'tipo': 'Urbano', 'antiguedad': '1750', 'uso': 'Religioso', 'regiones': [{'descripcion': 'RELIGIOSO', 'superficie': '3308'}], 'centroide': {'x': '37.301262', 'y': '-3.136249'}, 'geometria': [{'x': '37.301298', 'y': '-3.136662'}, {'x': '37.301316', 'y': '-3.136699'}, {'x': '37.301376', 'y': '-3.136711'}, ...], 'superficie': 3308.0}

mp = MetaParcela(provincia='Granada', municipio='Guadix', tipo_via='CL', calle='Largacha', numero=6)
# [OK] {'provincia': 'Granada', 'municipio': 'Guadix', 'calle': 'Largacha', 'numero': 6, 'parcelas': [<ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7ff4441944c0>, <ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7ff44507e770>, <ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7ff444194160>, <ESCatastroLib.models.InfoCatastral.ParcelaCatastral object at 0x7ff44507e110>]}

# Convertir a DataFrame
df = pc.to_dataframe()

# Exportar a JSON
pc.to_json("parcela.json")

# Exportar a CSV
pc.to_csv("parcela.csv")

# Exportar a Shapefile
pc.to_shapefile("parcela.shp")

# Exportar a Parquet
pc.to_parquet("parcela.parquet")

```

# ¿Cómo puedo contribuir?
Sigue las instrucciones de CONTRIBUTING.md y el Código de Conducta.

# Agradecimientos
- Al Catastro por hacer un Endpoint público.
- A GISCE-TI por currarse [una librería similar][1], basándose en los endpoints JSON.
- A mi abuelo y mi tío por pedirme que os eche una mano buscando tierras.
- A [Juanlu Cano][2] por darme la idea de extender el primer concepto en la PyConES para convertirlo en esta librería.
- A [Jaime Gómez-Obregón][3] por animar de forma muuuy indirecta a "hackear las Administraciones públicas".

[1]: https://github.com/gisce/pycatastro
[2]: https://github.com/astrojuanlu
[3]: https://github.com/JaimeObregon
