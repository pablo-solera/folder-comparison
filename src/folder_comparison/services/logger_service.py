"""Servicio de logging"""

from pathlib import Path


class LoggerService:
    """Maneja el guardado de logs"""

    @staticmethod
    def save_log(log_path: Path, operations) -> Path:
        """Guarda el log de operaciones en un archivo"""
        with open(log_path, "w", encoding="utf-8") as f:
            for op in operations:
                f.write(f"{op.message}\n")
        return log_path
