# logica.py
import os
import shutil
from datetime import datetime


class FolderComparator:
    """
    Clase encargada de comparar carpetas y copiar archivos nuevos.
    Totalmente independiente de UI.
    """

    def __init__(self, carpeta_base, carpeta_comparar, carpeta_destino):
        self.carpeta_base = carpeta_base
        self.carpeta_comparar = carpeta_comparar
        self.carpeta_destino = carpeta_destino
        self.registros = []
        self.copiados = 0

    def validar_carpetas(self):
        """Verifica que todas las carpetas existan."""
        return all(
            map(os.path.isdir, [self.carpeta_base, self.carpeta_comparar, self.carpeta_destino])
        )

    def generar_destino(self):
        """Genera la carpeta destino con nombre basado en la fecha y la carpeta comparada."""
        nombre_comparar = os.path.basename(self.carpeta_comparar.rstrip(os.sep))
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nombre_carpeta_destino = f"{nombre_comparar}_{fecha_actual}"
        destino_final = os.path.join(self.carpeta_destino, nombre_carpeta_destino)
        os.makedirs(destino_final, exist_ok=True)
        return destino_final

    def copiar_archivos(self, progreso_callback=None):
        """
        Copia los archivos nuevos de carpeta_comparar a carpeta_destino
        comparando con carpeta_base. Se puede pasar un callback de progreso.
        """
        destino_final = self.generar_destino()
        self.registros.clear()
        self.copiados = 0

        total = sum(len(files) for _, _, files in os.walk(self.carpeta_comparar))
        contador = 0

        for root_dir, _, files in os.walk(self.carpeta_comparar):
            for file in files:
                contador += 1
                if progreso_callback:
                    progreso_callback(contador, total)

                ruta_origen = os.path.join(root_dir, file)
                ruta_relativa = os.path.relpath(ruta_origen, self.carpeta_comparar)
                ruta_base = os.path.join(self.carpeta_base, ruta_relativa)
                ruta_destino = os.path.join(destino_final, ruta_relativa)

                if not os.path.exists(ruta_base):
                    os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
                    if not os.path.exists(ruta_destino):
                        shutil.copy2(ruta_origen, ruta_destino)
                        msg = f"✓ Copiado: {ruta_relativa}"
                        self.copiados += 1
                    else:
                        msg = f"⊘ Ignorado (ya existe en destino): {ruta_relativa}"
                else:
                    msg = f"⊘ Ignorado (existe en base): {ruta_relativa}"

                self.registros.append(msg)

        # Guardar log
        log_path = os.path.join(destino_final, "registro_copia.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.registros))

        return self.copiados, destino_final, log_path, self.registros
