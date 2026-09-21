import json
import re
from typing import Any

import requests

from .dto import ParcelaCatastralDTO, CalleDTO, MunicipioDTO, ProvinciaDTO, RegionCatastralDTO
from ...typing import (
    to_bool,
    to_float,
    to_int,
    to_str,
)

class CallejeroParser:
    """Parser base para las respuestas del API de Callejero del Catastro.

    Maneja la validación de respuesta HTTP y la conversión a JSON.
    Las subclases implementan ``_to_dtos()`` para extraer los DTOs
    específicos de cada tipo de consulta.
    """

    def parse(self, response: requests.Response) -> list[Any]:
        """Valida la respuesta HTTP y delega la extracción a ``_to_dtos()``.

        Args:
            response: Objeto requests.Response con la respuesta de la API.

        Returns:
            list: Lista de DTOs extraídos de la respuesta.

        Raises:
            ValueError: Si la respuesta no contiene JSON válido.
            requests.HTTPError: Si el código de estado indica error.
        """
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError as error:
            raise ValueError(
                "La respuesta no contiene un JSON válido"
            ) from error

        if not data:
            return []

        return self._to_dtos(data)
    
    def _to_dtos(self, data: dict[str, Any]) -> list[Any]:
        return []

class CallejeroProvinciaParser(CallejeroParser):
    def parse(self, response: requests.Response) -> list[ProvinciaDTO]:
        return super().parse(response)
    
    def _to_dtos(self, data: dict[str, Any]) -> list[ProvinciaDTO]:
        consulta = data.get('consulta_provincieroResult',{})
        provinciero = consulta.get("provinciero", {})
        provincias = provinciero.get("prov", [])

        if provincias is not None and len(provincias) > 0:
            if isinstance(provincias, dict):
                provincias = [provincias]
            return [ProvinciaDTO(
                codigoProvincia=to_int(provincia.get('cpine')),
                nombreProvincia=to_str(provincia.get('np'))
            ) for provincia in provincias]
        return []


class CallejeroMunicipioParser(CallejeroParser):
    def parse(self, response: requests.Response) -> list[MunicipioDTO]:
        return super().parse(response)
    
    def _to_dtos(self, data: dict[str, Any]) -> list[MunicipioDTO]:
        consulta = data.get('consulta_municipieroResult',{})
        municipiero = consulta.get("municipiero", {})
        municipios = municipiero.get("muni", [])

        if municipios is not None and len(municipios) > 0:
            return [MunicipioDTO(
                nombreMunicipio=to_str(municipio.get('nm'))
            ) for municipio in municipios]
        return []

class CallejeroCalleParser(CallejeroParser):
    def parse(self, response: requests.Response) -> list[CalleDTO]:
        return super().parse(response)
    
    def _to_dtos(self, data: dict[str, Any]) -> list[CalleDTO]:
        consulta = data.get('consulta_callejeroResult',{})
        callejero = consulta.get("callejero", {})
        calles = callejero.get("calle", [])

        if calles is not None and len(calles) > 0:
            return [CalleDTO(
                tipoViaCatastral=to_str(calle.get('dir').get('tv')),
                nombreCatastral=to_str(calle.get('dir').get('nv')),
                tipoViaINE=to_str(calle.get('dirine').get('sine')),
                nombreINE=to_str(calle.get('dirine').get('deine')),
            ) for calle in calles]
        return []

class ParcelaCatastralParser(CallejeroParser):
    """Parser de respuestas de consulta de parcelas catastrales.

    Maneja la extracción de información completa de una parcela desde la API
    del callejero. Soporta dos cardinalidades:
    - Resultado único (``bico``): parcela completa con regiones y detalles.
    - Resultados múltiples (``lrcdnp``): lista resumida de parcelas.

    Detecta automáticamente si la parcela es urbana o rústica y extrae
    los datos específicos accordingly.
    """

    def parse(self, response: requests.Response) -> list[ParcelaCatastralDTO]:
        """Parsea la respuesta de una consulta de parcela catastral.

        Determina automáticamente la cardinalidad del resultado (único o
        múltiples parcelas) y extrae la información correspondiente.

        Args:
            response: Objeto requests.Response con la respuesta de la API.

        Returns:
            list[ParcelaCatastralDTO]: Lista de parcelas extraídas.

        Raises:
            ValueError: Si no hay resultados o la respuesta es inválida.
        """
        return super().parse(response)
    
    def _parse_rc(self, data: dict[str, Any]) -> str:
        return ''.join(data.values())

    def _detectar_tipo(self, data: dict[str, Any]) -> str:
        if data.get('lors',None) is not None:
            return 'Rústico'
        elif data.get('lous', None) is not None:
            return 'Urbano'
        else:
            raise ValueError('Ni rústico ni urbano')

    def _parse_cultivo(self, data: dict[str, Any]) -> dict[str, Any]:
        localizacion_municipal = data.get('lors',{})
        localizacion_adicional = localizacion_municipal.get('lorus',{})

        return {
            'parcela':localizacion_adicional.get('cpp',{}).get('cpa'),
            'poligono':localizacion_adicional.get('cpp',{}).get('cpo'),
            'nombre_paraje': localizacion_adicional.get('npa')
        }

    def _parse_construccion(self, data: dict[str, Any]) -> dict[str, Any]:
        localizacion_municipal = data.get('lous',{})
        localizacion_adicional = localizacion_municipal.get('lourb',{})

        return {
            'calle':f"{localizacion_adicional.get('dir',{}).get('tv')} {localizacion_adicional.get('dir',{}).get('nv')}",
            'numero':localizacion_adicional.get('dir',{}).get('pnp'),
            'escalera': localizacion_adicional.get('loint',{}).get('es'),
            'planta': localizacion_adicional.get('loint',{}).get('pt'),
            'puerta': localizacion_adicional.get('loint',{}).get('pu')
        }

    def _parse_regions(self, data: list[dict[str, Any]], tipo: str) -> list[RegionCatastralDTO]:
       return RegionCatastralParser().parse(data,tipo)
    
    def _dtos_from_single(self, data: dict[str, Any]) -> list[ParcelaCatastralDTO]:
        detalle = data.get('bico',{})
        parcela = detalle.get('bi',{})

        
        rc = self._parse_rc(parcela.get('idbi').get('rc'))
        municipio = MunicipioDTO(nombreMunicipio=parcela.get('dt').get('nm'))
        provincia = ProvinciaDTO(codigoProvincia=parcela.get('dt').get('loine').get('cp'),
                                    nombreProvincia=parcela.get('dt').get('np'))
        superficie_economica = parcela.get('debi').get('sfc')
        antiguedad = parcela.get('debi','').get('ant')
        uso = parcela.get('debi','').get('luso')
        superficie_finca = detalle.get('finca',{}).get('dff',{}).get('ssf')
        superficie_solar = detalle.get('finca',{}).get('dff',{}).get('ss')
        tipo = self._detectar_tipo(parcela.get('dt',{}).get('locs'))
        if tipo == 'Urbano':
            datos_extra = self._parse_construccion(parcela.get('dt',{}).get('locs'))
            lcons = detalle.get('lcons') or []
            regiones = self._parse_regions(lcons, tipo)
        else:
            datos_extra = self._parse_cultivo(parcela.get('dt',{}).get('locs'))
            lspr = detalle.get('lspr') or []
            regiones = self._parse_regions(lspr, tipo)

        return[ParcelaCatastralDTO(
            referenciaCatastral=rc,
            municipio=municipio,
            provincia=provincia,
            tipo=tipo,
            calle=datos_extra.get('calle',None),
            numero=datos_extra.get('numero',None),
            escalera=datos_extra.get('escalera',None),
            planta=datos_extra.get('planta',None),
            puerta=datos_extra.get('puerta',None),
            superficie_economica=superficie_economica,
            superficie_finca = superficie_finca,
            superficie_solar = superficie_solar,
            antiguedad=antiguedad,
            uso= uso,
            parcela=datos_extra.get('parcela',None),
            poligono=datos_extra.get('poligono',None),
            nombre_paraje=datos_extra.get('nombre_paraje',None),
            regiones=regiones,
        ),]

    def _dtos_from_multiple(self, data: dict[str, Any]) -> list[ParcelaCatastralDTO]:
        consulta = data.get('lrcdnp',{})
        lista_parcelas = consulta.get('rcdnp',[])

        lista_parcelas_dto = []

        for parcela in lista_parcelas:
            rc = self._parse_rc(parcela.get('rc'))
            municipio = MunicipioDTO(nombreMunicipio=parcela.get('dt').get('nm'))
            provincia = ProvinciaDTO(codigoProvincia=parcela.get('dt').get('loine').get('cp'),
                                     nombreProvincia=parcela.get('dt').get('np'))
            superficie = parcela.get('debi').get('sfc')
            antiguedad = parcela.get('debi').get('ant')
            uso = parcela.get('debi').get('luso','')
            tipo = self._detectar_tipo(parcela.get('dt').get('locs'))
            if tipo == 'Urbano':
                datos_extra = self._parse_construccion(parcela.get('dt').get('locs'))
            else:
                datos_extra = self._parse_cultivo(parcela.get('dt').get('locs'))

            lista_parcelas_dto.append(ParcelaCatastralDTO(
                referenciaCatastral=rc,
                municipio=municipio,
                provincia=provincia,
                tipo=tipo,
                calle=datos_extra.get('calle',None),
                numero=datos_extra.get('numero',None),
                escalera=datos_extra.get('escalera',None),
                planta=datos_extra.get('planta',None),
                puerta=datos_extra.get('puerta',None),
                superficie_economica=superficie,
                antiguedad=antiguedad,
                uso= uso,
                parcela=datos_extra.get('parcela',None),
                poligono=datos_extra.get('poligono',None),
                nombre_paraje=datos_extra.get('nombre_paraje',None),
                regiones=None
            ))

        return lista_parcelas_dto


    def _to_dtos(self, data: dict[str, Any]) -> list[ParcelaCatastralDTO]:
        cardinalidad = to_int(data.get('control').get('cudnp'))
        if cardinalidad == 1:
            return self._dtos_from_single(data)
        elif cardinalidad > 1:
            return self._dtos_from_multiple(data)
        else:
            raise ValueError("No hay resultados")

class ParcelaCatastralRCParser(ParcelaCatastralParser):
    def _to_dtos(self, data: dict[str, Any]) -> list[ParcelaCatastralDTO]:
        normalized_data = data.get('consulta_dnprcResult')
        return super()._to_dtos(normalized_data)

class ParcelaCatastralPolParParser(ParcelaCatastralParser):
    def _to_dtos(self, data: dict[str, Any]) -> list[ParcelaCatastralDTO]:
        normalized_data = data.get('consulta_dnpppResult')
        return super()._to_dtos(normalized_data)

class ParcelaCatastralDirParser(ParcelaCatastralParser):
    def _to_dtos(self, data: dict[str, Any]) -> list[ParcelaCatastralDTO]:
        normalized_data = data.get('consulta_dnplocResult')
        return super()._to_dtos(normalized_data)
    
class RegionCatastralParser:
    def parse(self, data: list[dict[str, Any]], tipo: str) -> list[RegionCatastralDTO]:
        return self._to_dtos(data, tipo)
    
    def _parse_construccion(self, data: list[dict[str, Any]]) -> list[RegionCatastralDTO]:
        lista_dtos = []

        for construccion in data:
            localizacion_municipal = construccion.get('dt',{})
            localizacion_adicional = localizacion_municipal.get('lourb',{})

            lista_dtos.append(RegionCatastralDTO(
                descripcion=f"{construccion.get('lcd')} - {construccion.get('dvcons',{}).get('dtip','')}",
                superficie=construccion.get('dfcons',{}).get('stl'),
                escalera=localizacion_adicional.get('loint',{}).get('es'),
                planta=localizacion_adicional.get('loint',{}).get('pt'),
                puerta=localizacion_adicional.get('loint',{}).get('pu')
            ))

        return lista_dtos


    def _parse_cultivo(self, data: list[dict[str, Any]]) -> list[RegionCatastralDTO]:
        lista_dtos = []

        for cultivo in data:
            lista_dtos.append(RegionCatastralDTO(
                descripcion=cultivo.get('dspr',{}).get('dcc'),
                superficie=cultivo.get('dspr',{}).get('ssp'),
                escalera=None,
                planta=None,
                puerta=None
            ))

        return lista_dtos
    
    def _to_dtos(self, data: list[dict[str, Any]], tipo: str) -> list[RegionCatastralDTO]:
        if tipo == 'Urbano':
            return self._parse_construccion(data)
        else:
            return self._parse_cultivo(data)
