# Especificación de PyInstaller para TrialSteer.
# Dos ejecutables que comparten las mismas librerías. TrialSteer.exe abre la
# ventana sin consola y TrialSteer_consola.exe ejecuta los procesos hijos.
# Uso desde esta carpeta, python construir_exe.py
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules

ocultos = ["osqp.ext_builtin", "osqp.builtin", "osqp.interface", "pyvjoy._sdk", "pyvjoy._wrapper",
           "pyvjoy.vjoydevice", "pyvjoy.constants", "pyvjoy.exceptions"]
ocultos += collect_submodules("scipy.sparse")

a = Analysis(["TrialSteer.py"], pathex=[], binaries=collect_dynamic_libs("osqp"), datas=[],
             hiddenimports=ocultos, excludes=["pytest", "IPython", "PyQt5", "PySide6"], noarchive=False)
pyz = PYZ(a.pure)
ventana = EXE(pyz, a.scripts, [], exclude_binaries=True, name="TrialSteer", console=False,
              upx=False)
consola = EXE(pyz, a.scripts, [], exclude_binaries=True, name="TrialSteer_consola", console=True,
              upx=False)
coll = COLLECT(ventana, consola, a.binaries, a.datas, strip=False, upx=False, name="TrialSteer")
