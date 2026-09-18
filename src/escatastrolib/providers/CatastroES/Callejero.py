import requests

from ...errors.ErrorServidorDGC import comprobar_errores

class CallejeroAPIProvider:
    """Provider para consultas al Catastro de España sobre callejero.

    Proporciona métodos para consultar provincias, municipios, calles
    y parcelas a través del servicio web del Catastro.

    Attributes:
        URL_BASE: URL base del servicio de callejero del Catastro.
    """
    URL_BASE = 'https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCallejero.svc/json'

    @comprobar_errores
    def consulta_provincias(self) -> requests.Response:
        peticion = requests.get(f'{self.URL_BASE}/ObtenerProvincias')

        return peticion
    
    @comprobar_errores
    def consulta_municipios(self, provincia: str, municipio: str | None) -> requests.Response:
        peticion = requests.get(f'{self.URL_BASE}/ObtenerMunicipios', 
                                    params={
                                        'provincia' : provincia ,
                                        'municipio': municipio
                                    }
                                )
        return peticion
    
    @comprobar_errores
    def consulta_calles(self, provincia: str, municipio: str, tipo_via: str = '', nombre_calle: str = '') -> requests.Response:
        peticion = requests.get(f'{self.URL_BASE}/ObtenerCallejero',
                                params={
                                    'Provincia': provincia,
                                    'Municipio': municipio,
                                    'NomVia': nombre_calle,
                                    'TipoVia': tipo_via
                                })
        
        return peticion
    
    @comprobar_errores
    def consulta_parcela_por_rc(self, rc: str) -> requests.Response:
        peticion = requests.get(f'{self.URL_BASE}/Consulta_DNPRC', 
                                params={
                                    'RefCat': rc
                                    }
                                )

        return peticion
    
    @comprobar_errores
    def consulta_parcela_por_polpar(self, municipio: str, provincia: str, poligono: int, parcela: int) -> requests.Response:
        peticion = requests.get(f'{self.URL_BASE}/Consulta_DNPPP', 
                                params={
                                        'Provincia':provincia,
                                        'Municipio':municipio,
                                        'Poligono':poligono,
                                        'Parcela':parcela
                                    }
                                )

        return peticion
    
    @comprobar_errores
    def consulta_parcela_por_direccion(self, municipio: str, provincia: str, tipo_via: str, calle: str, numero: str) -> requests.Response:
        peticion = requests.get(f'{self.URL_BASE}/Consulta_DNPLOC', 
                                params={
                                        'Provincia':provincia,
                                        'Municipio':municipio,
                                        'Sigla':tipo_via,
                                        'Calle':calle,
                                        'Numero':numero
                                    }
                                )

        return peticion