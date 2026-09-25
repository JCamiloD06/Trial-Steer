"""
Construye el ejecutable de Trial Steer con PyInstaller.

Pasos.
    1. PyInstaller arma dist/Trial_Steer con Trial_Steer.exe, Trial_Steer_consola.exe
       y las librerías en _internal.
    2. Se copian junto a los ejecutables los archivos de empaquetado/contenido.py,
       con la estructura de carpetas del repositorio, porque el código calcula sus rutas a partir de su ubicación.
    3. Se comprime la carpeta en empaquetado/dist/Trial_Steer_v<versión>_windows.zip.

Solo usa archivos del propio repositorio, de modo que funciona también a
partir del zip del código fuente.

Uso desde la raíz del repositorio, con PyInstaller instalado.
    python trial_steer/empaquetado/construir_exe.py
"""
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

DIR = Path(__file__).resolve().parent
RAIZ_APP = DIR.parent
sys.path.insert(0, str(RAIZ_APP))
sys.path.insert(0, str(DIR))

import contenido  # noqa: E402
import version  # noqa: E402

DIST = DIR / "dist" / "Trial_Steer"
LEEME = f"""{version.NOMBRE} {version.VERSION}

Abrir Trial_Steer.exe. Trial_Steer_consola.exe lo usa el programa para las corridas y no se abre a mano.
Requiere Windows, Assetto Corsa con Steam y el controlador vJoy instalados.
El programa encuentra solo la instalación del juego en las bibliotecas de Steam y crea steam_appid.txt si falta.
Solo si hay varias instalaciones hay que escribir la elegida en ruta_ac de trial_steer/configs/juego_ac.json.
Las corridas se guardan en datos/corridas dentro de esta carpeta.
Assetto Corsa, Steam, vJoy y las librerías incluidas son de terceros, ver TERCEROS.md.
"""


def main():
    r = subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
                        "--distpath", str(DIR / "dist"),
                        "--workpath", str(Path(tempfile.gettempdir()) / "trial_steer_build"),
                        str(DIR / "trial_steer.spec")], cwd=DIR)
    if r.returncode != 0:
        sys.exit(r.returncode)
    archivos = contenido.archivos()
    for origen in archivos:
        destino = DIST / origen.relative_to(contenido.RAIZ_REPO)
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)
    (DIST / "LEEME.txt").write_text(LEEME, encoding="utf-8-sig")
    salida = DIR / "dist" / f"Trial_Steer_v{version.VERSION}_windows.zip"
    with zipfile.ZipFile(salida, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DIST.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p, Path("Trial_Steer") / p.relative_to(DIST))
    print(f"{len(archivos)} archivos de código copiados, ejecutable en {DIST}, "
          f"paquete {salida.name} de {salida.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
