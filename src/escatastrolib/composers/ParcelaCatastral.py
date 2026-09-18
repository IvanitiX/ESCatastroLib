

from typing import Any

from ..models.ParcelaCatastral import ParcelaCatastral

from ..parsers.CatastroES.Callejero.dto import ParcelaCatastralDTO
from ..parsers.CatastroES.INSPIREParcels.dto import INSPIREParcelDTO
from ..parsers.CatastroES.INSPIREBuildings.dto import ConstructionBaseDTO
from ..parsers.CatastroES.Croquis.dto import CroquisDTO
from ..parsers.CatastroES.MapaValoresUrbanos.dto import ValorUrbanoDTO
from ..parsers.CatastroES.MapaValoresRusticos.dto import ValoresRusticosDTO

from .mappers.GeometriaMapper import GeometriaMapper
from .mappers.MunicipioMapper import MunicipioMapper
from .mappers.RegionCatastralMapper import RegionCatastralMapper
from .mappers.ConstructionMapper import ConstructionMapper
from .mappers.DocumentoMapper import DocumentoMapper
from .mappers.ParcelaUrbanaMapper import ParcelaUrbanaMapper
from .mappers.ParcelaRusticaMapper import ParcelaRusticaMapper
from .mappers.ValorUrbanoMapper import ValorUrbanoMapper
from .mappers.ValorRusticoMapper import ValorRusticoMapper


class ParcelaCatastralComposer:
    """Orquestador que ensambla el modelo ParcelaCatastral desde DTOs.

    Coordina la transformación de los diferentes DTOs obtenidos de las APIs
    en el modelo de dominio ``ParcelaCatastral``. Utiliza mappers específicos
    para cada tipo de dato y respeta los flags de configuración para incluir
    o no información opcional (geometrías, valores, regiones, etc.).

    Args:
        include_geometries: Incluir geometría INSPIRE de la parcela.
        include_values: Incluir valoración del suelo (urbana o rústica).
        include_regions: Incluir regiones catastrales.
        include_constructions: Incluir construcciones (edificios, partes, etc.).
        include_documentation: Incluir documentos asociados (croquis).
    """
    def __init__(
        self,
        include_geometries: bool = False,
        include_values: bool = False,
        include_regions: bool = False,
        include_constructions: bool = False,
        include_documentation: bool = False,
    ) -> None:
        self.include_geometries = include_geometries
        self.include_values = include_values
        self.include_regions = include_regions
        self.include_constructions = include_constructions
        self.include_documentation = include_documentation

    def compose(
        self,
        parcela_dto: ParcelaCatastralDTO,
        *,
        completo: bool = False,
        geometria_dto: INSPIREParcelDTO | None = None,
        croquis_dtos: list[CroquisDTO] | None = None,
        valor_urbano_dto: ValorUrbanoDTO | None = None,
        valor_rustico_dto: ValoresRusticosDTO | None = None,
        construcciones_dtos: list[ConstructionBaseDTO] | None = None,
    ) -> ParcelaCatastral:
        """Ensbla un modelo ParcelaCatastral completo desde DTOs.

        Orquesta la transformación de todos los DTOs obtenidos de las APIs
        en el modelo de dominio. Utiliza los mappers correspondientes para
        cada tipo de dato y respeta los flags de configuración.

        Args:
            parcela_dto: DTO con los datos base de la parcela del callejero.
            completo: Si True, marca la parcela como información completa.
            geometria_dto: DTO de geometría INSPIRE de la parcela (opcional).
            croquis_dtos: Lista de DTOs de croquis/documentación (opcional).
            valor_urbano_dto: DTO de valoración urbana del suelo (opcional).
            valor_rustico_dto: DTO de valoración rústica del suelo (opcional).
            construcciones_dtos: Lista de DTOs de construcciones INSPIRE BU
                (ConstructionBaseDTO) (opcional).

        Returns:
            ParcelaCatastral: Modelo de dominio completo con toda la información
                disponible de la parcela.
        """

        municipio = MunicipioMapper.map(parcela_dto.municipio, parcela_dto.provincia)

        geometria = None
        if self.include_geometries and geometria_dto:
            geometria = GeometriaMapper.map(geometria_dto.geometria)

        superficie_plana = geometria_dto.area if geometria_dto else (
            parcela_dto.superficie_finca or 0.0
        )
        superficie_construida = parcela_dto.superficie_economica or 0.0

        valor_m2 = 0.0
        valor_urbano = None
        valor_rustico = None

        if self.include_values:
            if valor_urbano_dto:
                valor_urbano = ValorUrbanoMapper.map(valor_urbano_dto)
                valor_m2 = valor_urbano_dto.val_tipo_m2 or 0.0
            elif valor_rustico_dto:
                valor_rustico = ValorRusticoMapper.map(valor_rustico_dto)

        datos_urbanos = None
        datos_rusticos = None

        if parcela_dto.tipo == "Urbano":
            datos_urbanos = ParcelaUrbanaMapper.map(
                parcela_dto,
                municipio,
                valor_m2,
            )
        else:
            datos_rusticos = ParcelaRusticaMapper.map(parcela_dto, valor_m2)

        regiones = None
        if self.include_regions and parcela_dto.regiones:
            regiones = [RegionCatastralMapper.map(r) for r in parcela_dto.regiones]

        construcciones = None
        if self.include_constructions and construcciones_dtos:
            construcciones = [ConstructionMapper.map(d) for d in construcciones_dtos]

        documentacion = None
        if self.include_documentation and croquis_dtos:
            documentacion = [DocumentoMapper.map(c) for c in croquis_dtos]

        return ParcelaCatastral(
            referencia_catastral=parcela_dto.referenciaCatastral,
            municipio=municipio,
            tipo=parcela_dto.tipo,
            completo=completo,
            superficie_plana=superficie_plana,
            superficie_construida=superficie_construida,
            datos_urbanos=datos_urbanos,
            datos_rusticos=datos_rusticos,
            regiones=regiones,
            construcciones=construcciones,
            geometria=geometria,
            documentacion=documentacion,
            valor_urbano=valor_urbano,
            valor_rustico=valor_rustico,
        )
