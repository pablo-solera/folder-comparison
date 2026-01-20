"""Excepciones personalizadas del proyecto"""


class FolderComparisonError(Exception):
    """Excepción base para errores de comparación"""

    pass


class InvalidFolderError(FolderComparisonError):
    """Error cuando una carpeta no es válida"""

    pass


class CopyOperationError(FolderComparisonError):
    """Error durante operación de copia"""

    pass
