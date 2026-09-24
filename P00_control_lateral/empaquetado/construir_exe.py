"""
Construye el ejecutable de Trial Steer con PyInstaller.

Pasos.
    1. PyInstaller arma dist/Trial_Steer con Trial_Steer.exe, Trial_Steer_consola.exe
       y las librerías en _internal.
    2. Se copian junto a los ejecutables los mismos archivos del código fuente
       que van en el zip del registro, con la estructura de carpetas del
       repositorio, porque el código calcula sus rutas a partir de su ubicación.
    3. Se comprime la carpeta en documentacion/entrega/Trial_Steer_v<versión>_windows.zip.

Uso desde la raíz del repositorio.
    python P00_control_lateral/empaquetado/construir_exe.py
"""
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

DIR = Path(__file__).resolve().parent
RAIZ_P00 = DIR.parent
RAIZ_REPO = RAIZ_P00.parent
sys.path.insert(0, str(RAIZ_P00 / "documentacion"))

import empaquetar_codigo as emp  # noqa: E402

DIST = DIR / "dist" / "Trial_Steer"


def main():
    r = subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
                        "--distpath", str(DIR / "dist"), "--workpath", str(DIR / "build"),
                        str(DIR / "trial_steer.spec")], cwd=DIR)
    if r.returncode != 0:
        sys.exit(r.returncode)
    archivos = sorted(p for p in RAIZ_P00.rglob("*") if emp.incluir(p)) + emp.EXTRAS
    for origen in archivos:
        destino = DIST / origen.relative_to(RAIZ_REPO)
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)
    datos = json.loads((RAIZ_P00 / "documentacion" / "datos_portada.json").read_text(encoding="utf-8"))
    (DIST / "LEEME.txt").write_text(
        f"Trial Steer {datos['VERSION']}\n\n"
        "Abrir Trial_Steer.exe. Trial_Steer_consola.exe lo usa el programa para las corridas y no se abre a mano.\n"
        "Requiere Windows, Assetto Corsa con Steam y el controlador vJoy instalados.\n"
        "El programa encuentra solo la instalación del juego en las bibliotecas de Steam y crea steam_appid.txt si falta.\n"
        "Solo si hay varias instalaciones hay que escribir la elegida en ruta_ac de P00_control_lateral/configs/juego_ac.json.\n"
        "Las corridas se guardan en data/raw/p00/corridas dentro de esta carpeta.\n", encoding="utf-8")
    salida = RAIZ_P00 / "documentacion" / "entrega" / f"Trial_Steer_v{datos['VERSION']}_windows.zip"
    with zipfile.ZipFile(salida, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DIST.rglob("*")):
            if p.is_file():
                z.write(p, Path("Trial_Steer") / p.relative_to(DIST))
    print(f"{len(archivos)} archivos de código copiados, ejecutable en {DIST}, "
          f"paquete {salida.name} de {salida.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
