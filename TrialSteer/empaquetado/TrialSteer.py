"""
Punto de entrada del ejecutable de TrialSteer.

El lanzador abre cada corrida como un proceso aparte con el intérprete de
Python, sys.executable, y le pasa un script. Dentro del ejecutable no hay un
python.exe, así que este archivo hace que el propio ejecutable cumpla ese
papel. Según los argumentos,
    sin argumentos          abre el lanzador
    -u script.py args       ejecuta el script, como python -u
    script.py args          ejecuta el script
    -c código args          ejecuta el código, como python -c

Los scripts se ejecutan desde sus archivos .py junto al ejecutable, no desde
copias congeladas, para que las rutas que el código calcula a partir de su
propia ubicación apunten a la carpeta de la distribución, donde se guardan
las corridas, los respaldos y las preparaciones.

La ventana se abre con TrialSteer.exe, sin consola. Los procesos hijos usan
TrialSteer_consola.exe, con consola, porque la corrida escribe su salida en
la consola y el MPC completo solo guarda al recibir Ctrl+C de consola.
"""
import os
import runpy
import sys
from pathlib import Path

# Importaciones explícitas para que el empaquetador incluya todo lo que usan
# los scripts que se ejecutan desde disco. No se usan aquí.
import argparse, collections, csv, ctypes, dataclasses, gc, glob, hashlib, json, math, mmap  # noqa: E401,F401
import platform, queue, shutil, signal, subprocess, tempfile, threading, time, winreg, zipfile  # noqa: E401,F401
import tkinter, tkinter.ttk, tkinter.filedialog, tkinter.messagebox, tkinter.simpledialog  # noqa: E401,F401
import numpy, scipy, scipy.sparse, scipy.optimize, osqp  # noqa: E401,F401
import matplotlib  # noqa: E402,F401
matplotlib.use("Agg")
import matplotlib.pyplot  # noqa: E402,F401
try:
    import pyvjoy  # noqa: F401
except Exception:
    pyvjoy = None

CONGELADO = getattr(sys, "frozen", False)
BASE = Path(sys.executable).resolve().parent if CONGELADO else Path(__file__).resolve().parents[2]


def ejecutar_script(ruta, argumentos):
    ruta = Path(ruta).resolve()
    sys.argv = [str(ruta)] + argumentos
    sys.path.insert(0, str(ruta.parent))
    runpy.run_path(str(ruta), run_name="__main__")


def utf8():
    """
    Salida en UTF-8. El ejecutable ignora PYTHONIOENCODING, que el lanzador pone
    a sus procesos hijos, y la consola de Windows usa cp1252, donde no existen
    ψ ni δ. Sin esto la corrida se cae en la primera línea de salida.
    """
    for flujo in (sys.stdout, sys.stderr):
        if flujo is not None and hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8", errors="replace")


def main():
    utf8()
    args = sys.argv[1:]
    if CONGELADO:
        consola = BASE / "TrialSteer_consola.exe"
        if consola.exists():
            sys.executable = str(consola)
    while args and args[0] in ("-u", "-B", "-E"):
        args = args[1:]
    if args and args[0] == "-c":
        codigo = args[1] if len(args) > 1 else ""
        sys.argv = ["-c"] + args[2:]
        sys.path.insert(0, os.getcwd())
        exec(compile(codigo, "<-c>", "exec"), {"__name__": "__main__"})
        return
    if args and args[0].lower().endswith(".py"):
        ejecutar_script(args[0], args[1:])
        return
    os.chdir(BASE)
    ejecutar_script(BASE / "TrialSteer" / "abrir_lanzador.py", [])


if __name__ == "__main__":
    main()
