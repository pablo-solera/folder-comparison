"""Servicio para operaciones de archivos"""

import shutil
from pathlib import Path
from typing import Iterator


class FileService:
    """Maneja operaciones de archivos del sistema"""

    @staticmethod
    def walk_files(root_path: Path) -> Iterator[Path]:
        """Itera sobre todos los archivos en un directorio"""
        for item in root_path.rglob("*"):
            if item.is_file():
                yield item

    @staticmethod
    def copy_file(source: Path, destination: Path) -> None:
        """Copia un archivo asegurando que existe el directorio destino"""
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
