import requests
import json
import xmltodict

from ..utils.statics import URL_BASE_CALLEJERO, URL_BASE_GEOGRAFIA, URL_BASE_CROQUIS_DATOS
from ..utils.utils import comprobar_errores
from ..utils.exceptions import ErrorServidorCatastro
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
        geocentro (dict): Las coordenadas del geocentro de la parcela.
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


    def __create_geometry(self):
        geometry_request = requests.get(f'{URL_BASE_GEOGRAFIA}',
                                        params={
                                            'service':'wfs',
                                            'version':'2',
                                            'request':'getfeature',
                                            'STOREDQUERIE_ID':'GetParcel',
                                            'refcat': self.rc,
                                            'srsname': 'EPSG:4326'
                                        })

        geometry = xmltodict.parse(geometry_request.content)
        geoposition = geometry.get('FeatureCollection').get('member').get('cp:CadastralParcel').get('cp:referencePoint').get('gml:Point').get('gml:pos').split(' ')
        self.geocentro = {
            'x': geoposition[0],
            'y': geoposition[1]
        }
        parcel_geometry = geometry.get('FeatureCollection').get('member').get('cp:CadastralParcel').get('cp:geometry').get('gml:MultiSurface').get('gml:surfaceMember').get('gml:Surface').get('gml:patches').get('gml:PolygonPatch').get('gml:exterior').get('gml:LinearRing').get('gml:posList').get('#text').split(' ')
        self.geometria = [
            {
                'x': parcel_geometry[2*idx],
                'y': parcel_geometry[2*idx+1]
            } for idx in range(len(parcel_geometry)//2)
        ]

    def __create_from_rc(self, rc: str):
        """Create an instance of InfoCatastral from a RC (Referencia Catastral) string."""
        req1 = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPRC',
                            params={'RefCat': rc})
        
        info_cadastre = json.loads(req1.content)
        if comprobar_errores(info_cadastre):
            cudnp = info_cadastre.get("consulta_dnprcResult", {}).get("control", {}).get("cudnp", 1)
        
            if cudnp > 1:
                raise ErrorServidorCatastro(mensaje="Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.")
            else:
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
                self.__create_geometry()

                self.superficie = sum(float(region.get('superficie')) for region in self.regiones)

    def __create_from_parcel(self, provincia: str|None, municipio: str|None, poligono: str|None, parcela: str|None):
        """Create an instance of InfoCatastral from a parcela string."""
        req = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPPP',
                           params={
                               'Provincia': provincia,
                               'Municipio': municipio,
                               'Poligono': poligono,
                               'Parcela': parcela
                           })
        
        info_cadastre = json.loads(req.content)
        if comprobar_errores(info_cadastre):
            cudnp = info_cadastre.get("consulta_dnpppResult", {}).get("control", {}).get("cudnp", 1)

            if cudnp > 1:
                raise ErrorServidorCatastro(mensaje="Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.")
            else:
                self.rc = ''.join(info_cadastre.get('consulta_dnpppResult').get('bico').get('bi').get('idbi').get('rc').values())
                self.__create_from_rc(self.rc)

    def __create_from_address(self, provincia: str|None, municipio: str|None, tipo_via: str|None, calle: str|None, numero: str|None):
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
            
            if req.status_code == 200 and comprobar_errores(req.json()):
                info_cadastre = json.loads(req.content)
                cudnp = info_cadastre.get("consulta_dnplocResult", {}).get("control", {}).get("cudnp", 1)

                if cudnp > 1:
                    raise ErrorServidorCatastro(mensaje="Esta parcela tiene varias referencias catastrales. Usa un objeto MetaParcela.")
                else:
                    if 'lrcdnp' in info_cadastre.get('consulta_dnplocResult'):
                        self.rc = ''.join(info_cadastre.get('consulta_dnplocResult').get('lrcdnp').get('rcdnp')[0].get('rc').values())
                    elif 'bico' in info_cadastre.get('consulta_dnplocResult'):
                        self.rc = ''.join(info_cadastre.get('consulta_dnplocResult').get('bico').get('bi').get('idbi').get('rc').values())
                    self.__create_from_rc(self.rc)
            elif 'lerr' in json.loads(req.content).get('consulta_dnplocResult') and json.loads(req.content)['consulta_dnplocResult']['lerr'][0]['cod'] == '43':
                info_cadastre = json.loads(req.content)
                raise Exception(f"Ese número no existe. Prueba con alguno de estos: {[num.get('num').get('pnp') for num in info_cadastre.get('consulta_dnplocResult').get('numerero').get('nump')]}")

                
        else:
            raise Exception('La calle no existe.')

    def __init__(self, rc: str|None = None, provincia: int|str|None = None, municipio: int|str|None = None, poligono: int|None = None, parcela: int|None = None, tipo_via: str|None = None, calle: str|None = None, numero: str|None = None):
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
        
class MetaParcela:
    """
    Clase que representa una MetaParcela, es decir, una gran parcela catastral con 
    varias referencias catastrales (Parcelas Catastrales más pequeñas).

    Args:
        rc (str|None): La referencia catastral de la MetaParcela.

        provincia (int|str|None): El nombre de la provincia donde se encuentra la MetaParcela.
        municipio (int|str|None): El nombre del municipio donde se encuentra la MetaParcela.
        poligono (int|None): El número de polígono de la MetaParcela. Sólo se usa para buscar por parcela.
        parcela (int|None): El número de parcela de la MetaParcela. Sólo se usa para buscar por parcela.
        tipo_via (str|None): El tipo de vía de la dirección de la MetaParcela. Sólo se usa para buscar por dirección.
        calle (str|None): El nombre de la calle de la dirección de la MetaParcela. Sólo se usa para buscar por dirección.
        numero (str|None): El número de la dirección de la MetaParcela. Sólo se usa para buscar por dirección.
    Attributes:
        rc (str): La referencia catastral de la MetaParcela.
        parcelas (list): Una lista de ParcelaCatastral que representan las parcelas que componen la MetaParcela.

    """

    def __create_from_rc(self, rc: str):
        """Create an instance of InfoCatastral from a RC (Referencia Catastral) string."""
        req1 = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPRC',
                            params={'RefCat': rc})
    
        info_cadastre = json.loads(req1.content)
        if comprobar_errores(info_cadastre):
            self.parcelas = []
            num_parcelas = info_cadastre.get("consulta_dnprcResult", {}).get("control", {}).get("cudnp", 1)
            for idx in range(num_parcelas):
                rc = ''.join(info_cadastre.get('consulta_dnprcResult').get('lrcdnp').get('rcdnp')[idx].get('rc').values())
                self.parcelas.append(ParcelaCatastral(rc=rc))
                

    def __create_from_parcel(self, provincia: str|None, municipio: str|None, poligono: str|None, parcela: str|None):
        """Create an instance of InfoCatastral from a parcela string."""
        req = requests.get(f'{URL_BASE_CALLEJERO}/Consulta_DNPPP',
                           params={
                               'Provincia': provincia,
                               'Municipio': municipio,
                               'Poligono': poligono,
                               'Parcela': parcela
                           })
        
        info_cadastre = json.loads(req.content)
        if comprobar_errores(info_cadastre):
            self.parcelas = []
            num_parcelas = info_cadastre.get("consulta_dnpppResult", {}).get("control", {}).get("cudnp", 1)
            for idx in range(num_parcelas):
                rc = ''.join(info_cadastre.get('consulta_dnpppResult').get('lrcdnp').get('rcdnp')[idx].get('rc').values())
                self.parcelas.append(ParcelaCatastral(rc=rc))

    def __create_from_address(self, provincia: str|None, municipio: str|None, tipo_via: str|None, calle: str|None, numero: str|None):
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
            
            if req.status_code == 200 and comprobar_errores(req.json()):
                info_cadastre = json.loads(req.content)
                self.parcelas = []
                num_parcelas = info_cadastre.get("consulta_dnplocResult", {}).get("control", {}).get("cudnp", 1)
                for idx in range(num_parcelas):
                    rc = ''.join(info_cadastre.get('consulta_dnplocResult').get('lrcdnp').get('rcdnp')[idx].get('rc').values())
                    self.parcelas.append(ParcelaCatastral(rc=rc))
                
        else:
            raise Exception('La calle no existe.')

    def __init__(self, rc: str|None = None, provincia: int|str|None = None, municipio: int|str|None = None, poligono: int|None = None, parcela: int|None = None, tipo_via: str|None = None, calle: str|None = None, numero: str|None = None):
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
        
