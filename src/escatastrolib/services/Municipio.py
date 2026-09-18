from ..utils.territories import territorio_por_provincia, Territorio
from ..errors.ErrorServidorDGC import ErrorServidorSedeCatastro


_ORDEN_TRIAL_ERROR = [
    Territorio.ESPANA,
    Territorio.GUIPUZKOA,
    Territorio.ARABA,
]


def _instanciar_cliente(territorio: Territorio, options: dict | None = None):
    options = options or {}
    match territorio:
        case Territorio.ESPANA:
            from ..clients.CatastroES import CatastroESClient
            return CatastroESClient(**options)
        case Territorio.NAVARRA:
            from ..clients.Navarra import NavarraClient
            return NavarraClient(**options)
        case Territorio.GUIPUZKOA:
            from ..clients.Gipuzkoa import GipuzkoaClient
            return GipuzkoaClient(**options)
        case Territorio.ARABA:
            from ..clients.Araba import ArabaClient
            return ArabaClient(**options)
        case Territorio.BIZKAIA:
            from ..clients.Bizkaia import BizkaiaClient
            return BizkaiaClient(**options)
        case _:
            raise ValueError(f"Territorio no soportado: {territorio}")


class Municipio:
    """Wrapper de servicio que valida y busca municipios via el cliente catastral.

    Equivalente al Municipio original: valida que el municipio existe
    y lanza excepciones con sugerencias si no se encuentra.

    Args:
        provincia: Nombre o código de la provincia.
        municipio: Nombre del municipio. Si no se proporciona, lanza excepción.

    Raises:
        Exception: Si no se especifica el municipio o si no se encuentra.

    Attributes:
        municipio: Nombre del municipio (str).
        provincia: Nombre de la provincia (str).
    """

    def __init__(self, provincia: str, municipio: str | None = None):
        territorio = territorio_por_provincia(provincia)
        cliente = _instanciar_cliente(territorio)
        resultados = cliente.buscar_municipios(provincia, municipio or "")

        if not resultados:
            raise Exception(
                f"Error al asignar municipio. No se encontraron municipios "
                f"para la búsqueda: {municipio}"
            )

        if municipio:
            nombres = [r.nombreMunicipio for r in resultados]

            if len(resultados) == 1:
                self.municipio = resultados[0].nombreMunicipio
                self.provincia = provincia
            elif municipio.upper() in nombres:
                self.municipio = municipio.upper()
                self.provincia = provincia
            else:
                raise Exception(
                    f"Error al asignar municipio. No has especificado el "
                    f"municipio completamente. Estos son los municipios "
                    f"disponibles con esa búsqueda: {', '.join(nombres)}"
                )
        else:
            nombres = [r.nombreMunicipio for r in resultados]
            raise Exception(
                f"Error al asignar municipio. No has especificado el "
                f"municipio. Estos son los municipios disponibles: "
                f"{', '.join(nombres)}"
            )
