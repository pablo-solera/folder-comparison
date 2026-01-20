"""Modelos de datos para resultados de comparación"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class FileOperation:
    """Representa una operación en un archivo"""

    relative_path: str
    status: str
    message: str


@dataclass
class ComparisonResult:
    """Resultado de una operación de comparación"""

    files_copied: int = 0
    files_skipped: int = 0
    destination_folder: Path = None
    log_file: Path = None
    operations: List[FileOperation] = field(default_factory=list)

    @property
    def total_processed(self) -> int:
        return self.files_copied + self.files_skipped
