from .Municipio import Municipio
from ..utils.territories import territorio_por_provincia, Territorio


class Calle:
    """Wrapper de servicio que valida y busca calles via el cliente catastral.

    Equivalente a la Calle original: busca la calle en el municipio
    y lanza excepciones con sugerencias si no se encuentra.

    Args:
        municipio: Objeto Municipio al que pertenece la calle.
        nombre_calle: Nombre de la calle. Si no se proporciona, lanza excepción.
        tipo_via: Tipo de vía (ej. "CL", "AV"). Opcional.

    Raises:
        Exception: Si no se especifica la calle o si no se encuentra.

    Attributes:
        calle: Nombre de la calle (str).
        tipo_via: Tipo de vía (str).
        municipio: Objeto Municipio.
    """

    def __init__(
        self,
        municipio: Municipio,
        nombre_calle: str | None = None,
        tipo_via: str | None = None,
    ):
        from .Municipio import _instanciar_cliente

        territorio = territorio_por_provincia(municipio.provincia)
        cliente = _instanciar_cliente(territorio)
        resultados = cliente.buscar_calles(
            municipio.provincia, municipio.municipio, tipo_via or "", nombre_calle or ""
        )

        if resultados:
            if nombre_calle and len(resultados) == 1:
                self.calle = resultados[0].nombreCatastral
                self.tipo_via = resultados[0].tipoViaCatastral
                self.municipio = municipio
            elif nombre_calle:
                nombres = [
                    f"{r.tipoViaCatastral} {r.nombreCatastral}" for r in resultados
                ]
                raise Exception(
                    f"Error al asignar calle. No has especificado la calle "
                    f"completamente, o ese nombre está en varios lados "
                    f"(indica el tipo de vía que aparezca al principio de "
                    f"la vía como PZ o CL). Estas son las calles disponibles "
                    f"con esa búsqueda: {', '.join(nombres)}"
                )
            else:
                nombres = [
                    f"{r.tipoViaCatastral} {r.nombreCatastral}" for r in resultados
                ]
                raise Exception(
                    f"Error al asignar calle. No has especificado la calle. "
                    f"Estas son las calles disponibles: {', '.join(nombres)}"
                )
        else:
            raise Exception(
                "Error al listar calles: Puede que no exista ese municipio."
            )
