class ErrorServidorCatastro(Exception):
    """
    Clase de excepción personalizada para errores relacionados con el servidor del Catastro.
    Atributos:
    - mensaje (str): Mensaje de error específico del servidor del Catastro.
    """

    def __init__(self, mensaje=''):
        self.message = f'Error del Catastro. {mensaje}'
        super().__init__(self.message)

def lanzar_excepcion(mensaje_error: str) -> Exception:
    """
    Lanza una excepción personalizada con el mensaje de error proporcionado.
    Args:
        mensaje_error (str): El mensaje de error que se incluirá en la excepción.
    Returns:
        Exception: La excepción personalizada con el mensaje de error.
    """

    return ErrorServidorCatastro(mensaje=mensaje_error)