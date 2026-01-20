"""
Folder Comparison Tool
Compara carpetas y copia archivos nuevos automáticamente
"""

__version__ = "1.0.0"
__author__ = "Pablo"

from .core.comparator import FolderComparator
from .models.comparison_result import ComparisonResult

__all__ = ["FolderComparator", "ComparisonResult"]
