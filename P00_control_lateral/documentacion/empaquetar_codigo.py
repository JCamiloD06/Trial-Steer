"""
Empaqueta el código fuente de Trial Steer en un zip para el registro ante la DNDA.

Código auxiliar, no modifica ningún archivo. Solo lee y copia.

Qué entra lo decide empaquetado/contenido.py, la misma regla del ejecutable.
Conserva la estructura de carpetas del repositorio, porque el código calcula
sus rutas a partir de la ubicación de cada archivo. Comprueba al final que el
zip no contenga archivos compilados de Python.

Junto al zip escribe un listado con la huella SHA256 y el número de líneas de
cada archivo incluido.

Uso desde la raíz del repositorio.
    python P00_control_lateral/documentacion/empaquetar_codigo.py
"""
import hashlib
import sys
import time
import zipfile
from pathlib import Path

DIR = Path(__file__).resolve().parent
RAIZ_P00 = DIR.parent
sys.path.insert(0, str(RAIZ_P00))
sys.path.insert(0, str(RAIZ_P00 / "empaquetado"))

import contenido  # noqa: E402
import version  # noqa: E402

SALIDA = DIR / "entrega"
# Compatibilidad con construir_exe.py de versiones anteriores, que importaba estos nombres de aquí.
incluir = contenido.incluir
EXTRAS = contenido.EXTRAS


def sha256(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def lineas(ruta):
    if ruta.suffix not in (".py", ".json", ".ini", ".md", ".txt", ".csv", ".ps1", ".spec"):
        return None
    return len(ruta.read_text(encoding="utf-8", errors="replace").splitlines())


def main():
    base = f"Trial_Steer_v{version.VERSION}"
    archivos = contenido.archivos()
    SALIDA.mkdir(exist_ok=True)
    destino = SALIDA / f"Codigo_fuente_{base}.zip"
    filas = []
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for r in archivos:
            nombre_zip = r.relative_to(contenido.RAIZ_REPO).as_posix()
            z.write(r, nombre_zip)
            filas.append((nombre_zip, sha256(r), lineas(r)))
    compilados = [n for n in zipfile.ZipFile(destino).namelist() if n.endswith((".pyc", ".pyo")) or "__pycache__" in n]
    if compilados:
        sys.exit(f"El zip contiene archivos compilados, {compilados[:5]}")
    total_py = sum(n for a, _, n in filas if a.endswith(".py") and n)
    propio_py = sum(n for a, _, n in filas if a.endswith(".py") and a.startswith("P00_control_lateral/") and n)
    listado = [f"Código fuente de {version.NOMBRE} {version.VERSION}, congelado el {version.FECHA_CONGELAMIENTO}",
               f"Generado el {time.strftime('%Y-%m-%d %H:%M')} por documentacion/empaquetar_codigo.py",
               f"Archivos {len(filas)}, archivos Python {sum(1 for a, _, _ in filas if a.endswith('.py'))}, "
               f"líneas de Python {total_py}",
               f"Líneas de Python de P00_control_lateral {propio_py}, el resto es obra previa de los mismos autores",
               "Sin archivos compilados de Python ni carpetas __pycache__",
               "",
               "archivo | sha256 | lineas"]
    listado += [f"{a} | {h} | {n if n is not None else ''}" for a, h, n in filas]
    (SALIDA / f"Listado_codigo_fuente_{base}.txt").write_text("\n".join(listado) + "\n", encoding="utf-8")
    print(f"{destino.name}, {len(filas)} archivos, {total_py} líneas de Python, "
          f"{destino.stat().st_size / 1024:.0f} KB, sin archivos compilados")


if __name__ == "__main__":
    main()
