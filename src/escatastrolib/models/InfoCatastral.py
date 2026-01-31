import requests
import json
import xmltodict
from datetime import datetime

from shapely import Point
from typing import Union
from pyproj import Transformer

from ..utils.statics import URL_BASE_CALLEJERO, URL_BASE_GEOGRAFIA, URL_BASE_CROQUIS_DATOS, URL_BASE_MAPA_VALORES_URBANOS, URL_BASE_MAPA_VALORES_RUSTICOS, URL_BASE_WFS_EDIFICIOS, CULTIVOS
from ..utils.utils import comprobar_errores, listar_sistemas_referencia, lon_lat_from_coords_dict, lat_lon_from_coords_dict, distancia_entre_dos_puntos_geograficos 
from ..utils.exceptions import ErrorServidorCatastro
from ..utils import converters
from .Calle import Calle, Municipio

class ParcelaCatastral:
    """
    Clase que representa una parcela catastral.
    Args:
        rc (str, optional): La referencia catastral de la parcela. Defaults to None. Puede ir solo.

        provincia (int|str, optional): El código o nombre de la provincia. Defaults to None. Se usa para buscar por dirección o parcela.
        municipio (int|str, optional): El código o nombre del municipio. Defaults to None. Se usa para buscar por dirección o parcela.
        poligono (int, optional): El número del polígono. Defaults to None. Se usa para buscar por parcela.
        parcela (int, optional): El número de la parcela. Defaults to None. Se usa para buscar por parcela.
        tipo_via (str, optional): El tipo de vía de la dirección. Defaults to None. Se usa para buscar por dirección.
        calle (str, optional): El nombre de la calle de la dirección. Defaults to None. Se usa para buscar por dirección.
        numero (str, optional): El número de la dirección. Defaults to None. Se usa para buscar por dirección.
    Raises:
        ValueError: Se lanza si no se proporciona suficiente información para realizar la búsqueda o si la RC corresponde a una MetaParcela.
        ErrorServidorCatastro: Se lanza si hay un error en el servidor del Catastro.
    Attributes:
        rc (str): La referencia catastral de la parcela.
        provincia (int|str): El código o nombre de la provincia.
        municipio (int|str): El código o nombre del municipio.
        poligono (int): El número del polígono. Sólo se da en terrenos Rústicos.
        parcela (int): El número de la parcela. Sólo se da en terrenos Rústicos.
        tipo_via (str): El tipo de vía de la dirección. Sólo se da en terrenos Urbanos.
        calle (str): El nombre de la calle de la dirección. Sólo se da en terrenos Urbanos.
        numero (str): El número de la dirección. Sólo se da en terrenos Urbanos.
        url_croquis (str): La URL del croquis de la parcela.
        tipo (str): El tipo de la parcela (Urbano o Rústico).
        antiguedad (str): La antigüedad de la parcela (solo para parcelas urbanas).
        uso (str): El uso de la parcela (solo para parcelas urbanas).
        nombre_paraje (str): El nombre del paraje (solo para parcelas rústicas).
        regiones (list): Una lista de regiones de la parcela, cada una con una descripción y superficie.
        centroide (dict): Las coordenadas del centroide de la parcela.
        geometria (list): Una lista de puntos que representan la geometría de la parcela.
    """

    def __create_regions(self, info_cadastre: dict):
        self.regiones = []
        if self.tipo == 'Urbano':
            iterator = list(info_cadastre.values())[0].get('bico').get('lcons')
        elif self.tipo == 'Rústico':
            iterator = list(info_cadastre.values())[0].get('bico').get('lspr')
        for region in iterator:
            if self.tipo == 'Rústico':
                self.regiones.append({
                        'descripcion': region.get('dspr').get('dcc'),
                        'superficie': region.get('dspr').get('ssp')
                    })
            elif self.tipo == 'Urbano':
                self.regiones.append({
                        'descripcion': region.get('lcd'),
                        'superficie': region.get('dfcons').get('stl')
                    })


    def __create_geometry(self, projection: str = 'EPSG:4326'):
        geometry_request = requests.get(f'{URL_BASE_GEOGRAFIA}',
                                        params={
                                            'service':'wfs',
                                            'version':'2',
                                            'request':'getfeature',
                                            'STOREDQUERIE_ID':'GetParcel',
                                            'refcat': self.rc,
                                            'srsname': projection
                                        })

        geometry = xmltodict.parse(geometry_request.content)
        geoposition = geometry.get('FeatureCollection').get('member').get('cp:CadastralParcel').get('cp:referencePoint').get('gml:Point').get('gml:pos').split(' ')
        self.centroide = {
            'x': geoposition[1],
            'y': geoposition[0]
        }
        parcel_geometry = geometry.get('FeatureCollection').get('member').get('cp:CadastralParcel').get('cp:geometry').get('gml:MultiSurface').get('gml:surfaceMember').get('gml:Surface').get('gml:patches').get('gml:PolygonPatch').get('gml:exterior').get('gml:LinearRing').get('gml:posList').get('#text').split(' ')
        self.geometria = [
            {
                'x': parcel_geometry[2*idx+1],
                'y': parcel_geometry[2*idx]
            } for idx in range(len(parcel_geometry)//2)
        ]
        self.superficie_total = float(geometry.get('FeatureCollection').get('member').get('cp:CadastralParcel').get('cp:areaValue').get('#text')) 

    def __create_from_rc(self, rc: str, projection: str):
        """Create an instance of InfoCatastral from a RC (Referencia Catastral) string."""
        req1 = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPRC',
                            params={'RefCat': rc})
        
        if len(req1.content) > 0:
            try:
                info_cadastre = json.loads(req1.content)
            except:
                raise ErrorServidorCatastro(mensaje=f"El servidor no devuelve un JSON. Mensaje en bruto: {req1.content}")
            if comprobar_errores(info_cadastre):
                cudnp = info_cadastre.get("consulta_dnprcResult", {}).get("control", {}).get("cudnp", 1)
            
                if cudnp > 1:
                    raise ErrorServidorCatastro(mensaje="Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.")
                else:
                    self.rc = ''.join(info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('idbi').get('rc').values())
                    self.url_croquis = requests.get(URL_BASE_CROQUIS_DATOS, params={'refcat': self.rc}).url
                    self.municipio = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('nm')
                    self.provincia = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('np')
                    self.tipo = 'Rústico' if info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('idbi').get('cn') == 'RU' else 'Urbano'
                    if self.tipo == 'Urbano':
                        self.calle = f"{info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('locs').get('lous').get('lourb').get('dir').get('tv')} {info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('locs').get('lous').get('lourb').get('dir').get('nv')}"
                        self.numero = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('locs').get('lous').get('lourb').get('dir').get('pnp')
                        self.antiguedad = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('debi').get('ant')
                        self.uso = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('debi').get('luso')
                    elif self.tipo == 'Rústico':
                        self.parcela = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('locs').get('lors').get('lorus').get('cpp').get('cpa')
                        self.poligono = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('locs').get('lors').get('lorus').get('cpp').get('cpo')
                        self.nombre_paraje = info_cadastre.get('consulta_dnprcResult').get('bico').get('bi').get('dt').get('locs').get('lors').get('lorus').get('npa')
                    
                    self.__create_regions(info_cadastre)
                    self.__create_geometry(projection)

                    self.superficie_construida = sum(float(region.get('superficie')) for region in self.regiones)
                    self.superficie = sum(float(region.get('superficie')) for region in self.regiones)
        else:
            raise ErrorServidorCatastro("El servidor ha devuelto una respuesta vacia")

    def __create_from_parcel(self, provincia: Union[str,None], municipio: Union[str,None], poligono: Union[str,None], parcela: Union[str,None], projection: str):
        """Create an instance of InfoCatastral from a parcela string."""
        req = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPPP',
                           params={
                               'Provincia': provincia,
                               'Municipio': municipio,
                               'Poligono': poligono,
                               'Parcela': parcela
                           })
        if len(req.content) > 0:
            try:
                info_cadastre = json.loads(req.content)
            except:
                raise ErrorServidorCatastro(mensaje=f"El servidor no devuelve un JSON. Mensaje en bruto: {req1.content}")
            if comprobar_errores(info_cadastre):
                cudnp = info_cadastre.get("consulta_dnpppResult", {}).get("control", {}).get("cudnp", 1)

                if cudnp > 1:
                    raise ErrorServidorCatastro(mensaje="Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.")
                else:
                    self.rc = ''.join(info_cadastre.get('consulta_dnpppResult').get('bico').get('bi').get('idbi').get('rc').values())
                    self.__create_from_rc(self.rc, projection)
        else:
            raise ErrorServidorCatastro("El servidor ha devuelto una respuesta vacia")

    def __create_from_address(self, provincia: Union[str,None], municipio: Union[str,None], tipo_via: Union[str,None], calle: Union[str,None], numero: Union[str,None], projection: str):
        """Create an instance of InfoCatastral from an address string."""
        info_calle = Calle(
            municipio=Municipio(
                provincia=provincia,
                municipio=municipio
            ),
            tipo_via=tipo_via,
            nombre_calle=calle
        )

        if info_calle:
            req = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPLOC',
                               params={
                                   'Provincia': info_calle.municipio.provincia,
                                   'Municipio': info_calle.municipio.municipio,
                                   'Sigla': info_calle.tipo_via,
                                   'Calle': info_calle.calle,
                                   'Numero': numero
                               })
            
            if req.status_code == 200 and len(req.content) > 0 and comprobar_errores(req.json()):
                try:
                    info_cadastre = json.loads(req1.content)
                except:
                    raise ErrorServidorCatastro(mensaje=f"El servidor no devuelve un JSON. Mensaje en bruto: {req1.content}")
                cudnp = info_cadastre.get("consulta_dnplocResult", {}).get("control", {}).get("cudnp", 1)

                if cudnp > 1:
                    raise ErrorServidorCatastro(mensaje="Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.")
                else:
                    if 'lrcdnp' in info_cadastre.get('consulta_dnplocResult'):
                        self.rc = ''.join(info_cadastre.get('consulta_dnplocResult').get('lrcdnp').get('rcdnp')[0].get('rc').values())
                    elif 'bico' in info_cadastre.get('consulta_dnplocResult'):
                        self.rc = ''.join(info_cadastre.get('consulta_dnplocResult').get('bico').get('bi').get('idbi').get('rc').values())
                    self.__create_from_rc(self.rc, projection)
            elif 'lerr' in json.loads(req.content).get('consulta_dnplocResult') and json.loads(req.content)['consulta_dnplocResult']['lerr'][0]['cod'] == '43':
                info_cadastre = json.loads(req.content)
                raise Exception(f"Ese número no existe. Prueba con alguno de estos: {[num.get('num').get('pnp') for num in info_cadastre.get('consulta_dnplocResult').get('numerero').get('nump')]}")
            else:
                raise ErrorServidorCatastro("El servidor ha devuelto una respuesta vacia")

                
        else:
            raise Exception('La calle no existe.')

    def __init__(self, rc: Union[str,None] = None, provincia: Union[str,None] = None, municipio: Union[int,str,None] = None, poligono: Union[int,None] = None, parcela: Union[int,None] = None, tipo_via: Union[str,None] = None, calle: Union[str,None] = None, numero: Union[str,None] = None, projection: str = 'EPSG:4326'):
        if projection not in listar_sistemas_referencia():
            raise ValueError(f"El sistema de referencia {projection} no existe. Los sistemas de referencia disponibles son: {listar_sistemas_referencia()}")
        if rc:
            self.rc = rc
            self.__create_from_rc(rc, projection)
        elif provincia and municipio and poligono and parcela:
            self.provincia = provincia
            self.municipio = municipio
            self.poligono = poligono
            self.parcela = parcela
            self.__create_from_parcel(provincia, municipio, poligono, parcela, projection)
        elif provincia and municipio and tipo_via and calle and numero:
            self.provincia = provincia
            self.municipio = municipio
            self.calle = calle
            self.numero = numero
            self.__create_from_address(provincia, municipio, tipo_via, calle, numero, projection)
        else:
            raise ValueError("No se ha proporcionado suficiente información para realizar la búsqueda")
        
    @property
    def distancias_aristas(self):
        """
            Calcula las distancias entre dos puntos de la geometría, par a par.
        """
        if self.geometria:
            distancias = []
            for idx in range(0, len(self.geometria)):
                idx_0 = len(self.geometria)-1 if idx == 0 else idx-1
                idx_f=idx
                distancias.append(distancia_entre_dos_puntos_geograficos(
                    lat_lon_from_coords_dict(self.geometria[idx_0]),
                    lat_lon_from_coords_dict(self.geometria[idx_f])
                ))
            return distancias
        else: 
            return None

    @property
    def perimetro(self):
        """
            Calcula el perímetro de la geometría
        """
        distancias = self.distancias_aristas
        if distancias:
            return sum(distancias)
        else: 
            return None

    def valor_catastral_urbano_m2(self, anio):
        if self.tipo == 'Rústico':
            return 0
        
        req = requests.get(f'{URL_BASE_MAPA_VALORES_URBANOS}',
                               params={
                                   "huso":"4326",
                                   "x":self.centroide['x'],
                                   "y":self.centroide['y'],
                                   "anyoZV":anio,
                                   "suelo": "N",
                                   "tipo_mapa":"vivienda"
                               })

        values_map = converters.gpd.read_file(req.content)
        centroide_point = Point(self.centroide['x'],self.centroide['y'])
        selected_polygon = values_map[values_map.geometry.covers(centroide_point)]

        return selected_polygon['Ptipo1'].iloc[0].get('val_tipo_m2')
    
    @property
    def numero_plantas(self):
        """
        Obtiene el número de plantas de un edificio a partir de su
        referencia catastral usando el WFS INSPIRE de Catastro.

        Criterio:
        - Se consultan las BuildingPart
        - Se toma el máximo número de plantas sobre rasante
        - Se devuelve también el máximo bajo rasante

        Parameters
        ----------
        refcat : str
            Referencia catastral completa (ej: '9795702WG1499N0001AY')
        timeout : int
            Timeout de la petición HTTP en segundos

        Returns
        -------
        dict
            {
                'refcat': str,
                'parts': int,
                'max_above_ground': int | None,
                'max_below_ground': int,
                'total_floors': int | None,
                'parts_detail': list
            }
        """

        if self.tipo == 'Rústico':
            return 0

        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "STOREDQUERIE_ID": "GetBuildingPartByParcel",
            "REFCAT": self.rc,
            "srsname": "EPSG:4326"
        }

        response = requests.get(URL_BASE_WFS_EDIFICIOS, params=params)
        response.raise_for_status()

        data = xmltodict.parse(response.content)

        feature_collection = data.get("gml:FeatureCollection", {})
        members = feature_collection.get("gml:featureMember", [])

        if isinstance(members, dict):
            members = [members]

        above_floors = []
        below_floors = []
        parts_detail = []

        for member in members:
            bp = member.get("bu-ext2d:BuildingPart")
            if not bp:
                continue

            part_id = bp.get("@gml:id")

            above = bp.get("bu-ext2d:numberOfFloorsAboveGround")
            below = bp.get("bu-ext2d:numberOfFloorsBelowGround")

            above_i = int(above) if above is not None else None
            below_i = int(below) if below is not None else 0

            if above_i is not None:
                above_floors.append(above_i)
            below_floors.append(below_i)

            parts_detail.append({
                "id": part_id,
                "floors_above_ground": above_i,
                "floors_below_ground": below_i
            })

        return {
            "plantas": max(above_floors) if above_floors else None,
            "sotanos": max(below_floors) if below_floors else 0,
            "total": (
                max(above_floors) + max(below_floors)
                if above_floors else None
            )
        }
    
    def valor_catastral_rustico_m2(self, anio:str):
        """
        Obtiene los valores catastrales de tierras a partir de una referencia catastral.

        Args:
            referencia_catastral (str): Referencia catastral de la parcela.

        Returns:
            dict: Datos de la parcela con región y módulos €/ha, o None si no se encuentran.
        """

        if self.tipo == "Urbano":
            return {}

        geometria = self.geometria

        # Transformar geometría EPSG:4381 → EPSG:3857
        transformer = Transformer.from_crs("EPSG:4381", "EPSG:3857", always_xy=True)
        xs_3857 = []
        ys_3857 = []
        for p in geometria:
            x, y = transformer.transform(p["x"], p["y"])
            xs_3857.append(x)
            ys_3857.append(y)

        # BBOX EPSG:3857
        bbox = f"{min(xs_3857)},{min(ys_3857)},{max(xs_3857)},{max(ys_3857)}"

        params = {
            "SERVICE": "WMS",
            "VERSION": "1.3.0",
            "REQUEST": "GetFeatureInfo",
            "LAYERS": f"IAMIR{int(str(anio)[-2:])-1}:athiamir{int(str(anio)[-2:])-1}",
            "QUERY_LAYERS": f"IAMIR{int(str(anio)[-2:])-1}:athiamir{int(str(anio)[-2:])-1}",
            "STYLES": "",
            "CRS": "EPSG:3857",
            "SRS": "EPSG:3857",
            "BBOX": bbox,
            "WIDTH": 101,
            "HEIGHT": 101,
            "FORMAT": "image/png",
            "TRANSPARENT": "true",
            "I": 55,
            "J": 55,
            "INFO_FORMAT": "application/json"
        }

        r = requests.get(URL_BASE_MAPA_VALORES_RUSTICOS, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        if not data.get("features"):
            return None

        props = data["features"][0]["properties"]

        modulos = {
            "region": props.get("REGIONAL"),
            "nombre_region": props.get("NOMBRE"),
            "modulos_€/ha": {}
        }

        for cod, desc in CULTIVOS.items():
            val = props.get(cod)
            if isinstance(val, (int, float)) and val > 0:
                modulos["modulos_€/ha"][desc] = val

        return {
            "region": modulos["region"],
            "nombre_region": modulos["nombre_region"],
            "modulos_€/ha": modulos["modulos_€/ha"]
        }
        

    def to_dataframe(self):
        """
        Convierte la parcela en un DataFrame de pandas.

        Returns:
            pd.DataFrame: Un DataFrame que contiene los datos de la parcela.
        """
        return converters.to_geodataframe([self])
    
    def to_json(self, filename: Union[str,None] = None) -> str:
        """
        Convierte la parcela en un JSON.

        Args:
            filename (Union[str,None], optional): Nombre del archivo donde guardar el JSON. Defaults to None.

        Returns:
            str: Una cadena JSON que contiene los datos de la parcela.
        """
        return converters.to_json([self], filename)
    
    def to_csv(self, filename: Union[str,None] = None) -> str:
        """
        Convierte la parcela en un CSV.

        Args:
            filename (Union[str,None], optional): Nombre del archivo donde guardar el CSV. Defaults to None.

        Returns:
            str: Una cadena CSV que contiene los datos de la parcela.
        """
        return converters.to_csv([self], filename)
    
    def to_shapefile(self, filename: str):
        """
        Guarda la parcela como un archivo Shapefile.

        Args:
            filename (str): El nombre del archivo Shapefile a guardar.
        """
        converters.to_shapefile([self], filename)

    def to_parquet(self, filename: str):
        """
        Guarda la parcela como un archivo Parquet.

        Args:
            filename (str): El nombre del archivo Parquet a guardar.
        """
        converters.to_parquet([self], filename)
        
class MetaParcela:
    """
    Clase que representa una MetaParcela, es decir, una gran parcela catastral con 
    varias referencias catastrales (Parcelas Catastrales más pequeñas).

    Args:
        rc (Union[str,None]): La referencia catastral de la MetaParcela.

        provincia (int|Union[str,None]): El nombre de la provincia donde se encuentra la MetaParcela.
        municipio (int|Union[str,None]): El nombre del municipio donde se encuentra la MetaParcela.
        poligono (Union[int,None]): El número de polígono de la MetaParcela. Sólo se usa para buscar por parcela.
        parcela (Union[int,None]): El número de parcela de la MetaParcela. Sólo se usa para buscar por parcela.
        tipo_via (Union[str,None]): El tipo de vía de la dirección de la MetaParcela. Sólo se usa para buscar por dirección.
        calle (Union[str,None]): El nombre de la calle de la dirección de la MetaParcela. Sólo se usa para buscar por dirección.
        numero (Union[str,None]): El número de la dirección de la MetaParcela. Sólo se usa para buscar por dirección.
    Attributes:
        rc (str): La referencia catastral de la MetaParcela.
        parcelas (list): Una lista de ParcelaCatastral que representan las parcelas que componen la MetaParcela.

    """

    def __create_from_rc(self, rc: str):
        """Create an instance of InfoCatastral from a RC (Referencia Catastral) string."""
        req1 = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPRC',
                            params={'RefCat': rc})

        if len(req1.content) > 0:
            info_cadastre = json.loads(req1.content)
            if comprobar_errores(info_cadastre):
                self.parcelas = []
                num_parcelas = info_cadastre.get("consulta_dnprcResult", {}).get("control", {}).get("cudnp", 1)
                for idx in range(num_parcelas):
                    rc = ''.join(info_cadastre.get('consulta_dnprcResult').get('lrcdnp').get('rcdnp')[idx].get('rc').values())
                self.parcelas.append(ParcelaCatastral(rc=rc))
        else:
            raise ErrorServidorCatastro("El servidor ha devuelto una respuesta vacia")
                

    def __create_from_parcel(self, provincia: Union[str,None], municipio: Union[str,None], poligono: Union[str,None], parcela: Union[str,None]):
        """Create an instance of InfoCatastral from a parcela string."""
        req = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPPP',
                           params={
                               'Provincia': provincia,
                               'Municipio': municipio,
                               'Poligono': poligono,
                               'Parcela': parcela
                           })
        if len(req.content) > 0:
            info_cadastre = json.loads(req.content)
            if comprobar_errores(info_cadastre):
                self.parcelas = []
                num_parcelas = info_cadastre.get("consulta_dnpppResult", {}).get("control", {}).get("cudnp", 1)
                for idx in range(num_parcelas):
                    rc = ''.join(info_cadastre.get('consulta_dnpppResult').get('lrcdnp').get('rcdnp')[idx].get('rc').values())
                    self.parcelas.append(ParcelaCatastral(rc=rc))
        else:
            raise ErrorServidorCatastro("El servidor ha devuelto una respuesta vacia")

    def __create_from_address(self, provincia: Union[str,None], municipio: Union[str,None], tipo_via: Union[str,None], calle: Union[str,None], numero: Union[str,None]):
        """Create an instance of InfoCatastral from an address string."""
        info_calle = Calle(
            municipio=Municipio(
                provincia=provincia,
                municipio=municipio
            ),
            tipo_via=tipo_via,
            nombre_calle=calle
        )

        if info_calle:
            req = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPLOC',
                               params={
                                   'Provincia': info_calle.municipio.provincia,
                                   'Municipio': info_calle.municipio.municipio,
                                   'Sigla': info_calle.tipo_via,
                                   'Calle': info_calle.calle,
                                   'Numero': numero
                               })
            
            if req.status_code == 200 and len(req.content) > 0 and comprobar_errores(req.json()):
                info_cadastre = json.loads(req.content)
                self.parcelas = []
                num_parcelas = info_cadastre.get("consulta_dnplocResult", {}).get("control", {}).get("cudnp", 1)
                for idx in range(num_parcelas):
                    rc = ''.join(info_cadastre.get('consulta_dnplocResult').get('lrcdnp').get('rcdnp')[idx].get('rc').values())
                    self.parcelas.append(ParcelaCatastral(rc=rc))
            else:
                raise ErrorServidorCatastro("El servidor ha devuelto una respuesta vacia")
                
        else:
            raise Exception('La calle no existe.')

    def __init__(self, rc: Union[str,None] = None, provincia: Union[int,str,None] = None, municipio: Union[int,str,None] = None, poligono: Union[int,None] = None, parcela: Union[int,None] = None, tipo_via: Union[str,None] = None, calle: Union[str,None] = None, numero: Union[str,None] = None):
        if rc:
            self.rc = rc
            self.__create_from_rc(rc)
        elif provincia and municipio and poligono and parcela:
            self.provincia = provincia
            self.municipio = municipio
            self.poligono = poligono
            self.parcela = parcela
            self.__create_from_parcel(provincia, municipio, poligono, parcela)
        elif provincia and municipio and tipo_via and calle and numero:
            self.provincia = provincia
            self.municipio = municipio
            self.calle = calle
            self.numero = numero
            self.__create_from_address(provincia, municipio, tipo_via, calle, numero)
        else:
            raise ValueError("No se ha proporcionado suficiente información para realizar la búsqueda")
        

    def to_dataframe(self):
        """
        Convierte la MetaParcela en un DataFrame de pandas.

        Returns:
            pd.DataFrame: Un DataFrame que contiene las parcelas de la MetaParcela.
        """
        return converters.to_geodataframe(self.parcelas)
    
    def to_json(self, filename: Union[str,None] = None) -> str:
        """
        Convierte la MetaParcela en un JSON.

        Args:
            filename (Union[str,None], optional): Nombre del archivo donde guardar el JSON. Defaults to None.

        Returns:
            str: Una cadena JSON que contiene las parcelas de la MetaParcela.
        """
        return converters.to_json(self.parcelas, filename)
    
    def to_csv(self, filename: Union[str,None] = None) -> str:
        """
        Convierte la MetaParcela en un CSV.

        Args:
            filename (Union[str,None], optional): Nombre del archivo donde guardar el CSV. Defaults to None.

        Returns:
            str: Una cadena CSV que contiene las parcelas de la MetaParcela.
        """
        return converters.to_csv(self.parcelas, filename)
    
    def to_shapefile(self, filename: str):
        """
        Guarda la MetaParcela como un archivo Shapefile.

        Args:
            filename (str): El nombre del archivo Shapefile a guardar.
        """
        converters.to_shapefile(self.parcelas, filename)

    def to_parquet(self, filename: str):
        """
        Guarda la MetaParcela como un archivo Parquet.

        Args:
            filename (str): El nombre del archivo Parquet a guardar.
        """
        converters.to_parquet(self.parcelas, filename)
        
