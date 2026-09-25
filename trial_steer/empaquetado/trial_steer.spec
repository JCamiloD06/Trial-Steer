# Especificación de PyInstaller para Trial Steer.
# Dos ejecutables que comparten las mismas librerías. Trial_Steer.exe abre la
# ventana sin consola y Trial_Steer_consola.exe ejecuta los procesos hijos.
# Uso desde esta carpeta, python construir_exe.py
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules

ocultos = ["osqp.ext_builtin", "osqp.builtin", "osqp.interface", "pyvjoy._sdk", "pyvjoy._wrapper",
           "pyvjoy.vjoydevice", "pyvjoy.constants", "pyvjoy.exceptions"]
ocultos += collect_submodules("scipy.sparse")

a = Analysis(["trial_steer.py"], pathex=[], binaries=collect_dynamic_libs("osqp"), datas=[],
             hiddenimports=ocultos, excludes=["pytest", "IPython", "PyQt5", "PySide6"], noarchive=False)
pyz = PYZ(a.pure)
ventana = EXE(pyz, a.scripts, [], exclude_binaries=True, name="Trial_Steer", console=False,
              upx=False)
consola = EXE(pyz, a.scripts, [], exclude_binaries=True, name="Trial_Steer_consola", console=True,
              upx=False)
coll = COLLECT(ventana, consola, a.binaries, a.datas, strip=False, upx=False, name="Trial_Steer")
