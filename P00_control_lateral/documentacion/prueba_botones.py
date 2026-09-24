"""
Prueba de todos los botones y campos del lanzador sin Assetto Corsa.

Código auxiliar nuevo, no modifica ningún script existente. Abre la ventana
real, recorre todos los botones de todas las pestañas y los pulsa. Los
diálogos se contestan solos con No o Cancelar, de modo que ningún botón
genera planes, corre vueltas ni cambia archivos. Registra cada diálogo que
aparece y cualquier excepción de la interfaz.

Los botones que abren el simulador, Iniciar corrida e Iniciar MPC completo,
no se pulsan aquí. Se prueban con vueltas reales en capturas_lanzador.py y
en prueba_exe_ac.py.

Al final compara las huellas de los planes y configuraciones antes y después,
y termina con código distinto de cero si algo falló.

Uso desde la raíz del repositorio, o con el ejecutable.
    python P00_control_lateral/documentacion/prueba_botones.py
    python P00_control_lateral/documentacion/prueba_botones.py --raiz <carpeta P00_control_lateral>
"""
import argparse
import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", default=str(Path(__file__).resolve().parents[1]))
ap.add_argument("--salida", default="")
ARGS = ap.parse_args()
RAIZ_P00 = Path(ARGS.raiz).resolve()
sys.path.insert(0, str(RAIZ_P00))

import tkinter as tk  # noqa: E402
from tkinter import filedialog, messagebox, simpledialog, ttk  # noqa: E402

from lanzador import app as mod_app  # noqa: E402

NO_PULSAR = {"Iniciar corrida", "Iniciar MPC completo"}
DIALOGOS = []
ERRORES = []


def falso(nombre, respuesta):
    def f(*a, **k):
        DIALOGOS.append({"tipo": nombre, "titulo": a[0] if a else k.get("title"),
                         "mensaje": (a[1] if len(a) > 1 else k.get("message", ""))[:160]})
        return respuesta
    return f


for nombre in ("showinfo", "showerror", "showwarning"):
    setattr(messagebox, nombre, falso(nombre, "ok"))
for nombre in ("askyesno", "askokcancel", "askretrycancel"):
    setattr(messagebox, nombre, falso(nombre, False))
messagebox.askyesnocancel = falso("askyesnocancel", None)
messagebox.askquestion = falso("askquestion", "no")
filedialog.askopenfilename = falso("askopenfilename", "")
filedialog.askdirectory = falso("askdirectory", "")
simpledialog.askinteger = falso("askinteger", None)
simpledialog.askstring = falso("askstring", None)


def huellas():
    h = {}
    for r in sorted((RAIZ_P00 / "configs").rglob("*")):
        if r.is_file():
            h[str(r.relative_to(RAIZ_P00))] = hashlib.sha256(r.read_bytes()).hexdigest()
    return h


def botones(widget):
    for w in widget.winfo_children():
        if isinstance(w, (ttk.Button, tk.Button)):
            yield w
        yield from botones(w)


def ruta(w):
    """Pestaña principal e interna a la que pertenece el widget."""
    nombres = []
    padre = w
    while padre is not None:
        maestro = padre.master
        if isinstance(maestro, ttk.Notebook):
            nombres.append(maestro.tab(padre, "text"))
        padre = maestro
    return " / ".join(reversed(nombres))


def main():
    antes = huellas()
    v = mod_app.Lanzador()
    v.report_callback_exception = lambda exc, val, tb: ERRORES.append(
        "".join(traceback.format_exception(exc, val, tb)))
    v.update()
    resultados = []

    # Campos de la pestaña Corrida, cada uno con su rótulo y un valor válido.
    campos = {"Fase": v.var_fase, "Controlador": v.var_ctrl, "Perfil": v.var_perfil, "Sesión": v.var_sesion,
              "Etiqueta": v.var_etiqueta, "Id del plan": v.var_id_plan, "Tiempo máximo s": v.var_tmax,
              "Configuración": v.var_config, "No verificar vehículo, solo pruebas": v.var_sin_verif}
    v.var_fase.set("prueba")
    for fase in mod_app.FASES:
        v.var_fase.set(fase)
        v.update()
    v.var_fase.set("prueba")
    v.var_tmax.set("30")
    try:
        comando = v._argumentos(validar=True)
        resultados.append({"control": "armado del comando en fase prueba", "resultado": "ok",
                           "detalle": " ".join(comando[2:])})
    except Exception as e:
        resultados.append({"control": "armado del comando en fase prueba", "resultado": f"error {e}"})
    for fase in ("campana", "sintonia", "piloto"):
        v.var_fase.set(fase)
        try:
            v._argumentos(validar=True)
            resultados.append({"control": f"validación del Id del plan en fase {fase}", "resultado": "no exige"})
        except ValueError:
            resultados.append({"control": f"validación del Id del plan en fase {fase}", "resultado": "ok, exige"})
    v.var_fase.set("prueba")
    v.var_tmax.set("")

    # Cada pestaña se selecciona y se pulsan todos sus botones.
    for i in range(len(v.nb_principal.tabs())):
        v.nb_principal.select(i)
        v.update()
    for i in range(len(v.nb.tabs())):
        v.nb.select(i)
        v.update()
    arboles = [v.tree_plan, v.tree_sint, v.tree_pil]
    for arbol in arboles:
        hijos = arbol.get_children()
        if hijos:
            arbol.selection_set(hijos[0])
            arbol.focus(hijos[0])
    if v.mapa_verif:
        v.var_corrida_verif.set(next(iter(v.mapa_verif)))

    for b in botones(v):
        texto = b.cget("text")
        lugar = ruta(b)
        estado = str(b.cget("state"))
        if texto in NO_PULSAR:
            resultados.append({"control": f"{lugar} / {texto}", "resultado": "no se pulsa aquí, se prueba con el simulador"})
            continue
        if "seleccionada" in texto:
            # Los botones anteriores recargan la tabla y borran la selección, se vuelve a elegir la primera fila.
            arbol = {"Plan de campaña": v.tree_plan, "Tanda de sintonía": v.tree_sint,
                     "Piloto": v.tree_pil}.get(lugar.split(" / ")[-1])
            if arbol is not None and arbol.get_children():
                arbol.selection_set(arbol.get_children()[0])
                v.update()
        n_dialogos, n_errores = len(DIALOGOS), len(ERRORES)
        if estado == "disabled":
            resultados.append({"control": f"{lugar} / {texto}", "resultado": "deshabilitado en reposo"})
            continue
        try:
            b.invoke()
            v.update()
            time.sleep(0.3)
            v.update()
        except Exception as e:
            ERRORES.append(f"{texto}, {e}")
        nuevos = DIALOGOS[n_dialogos:]
        resultados.append({"control": f"{lugar} / {texto}",
                           "resultado": "error" if len(ERRORES) > n_errores else "ok",
                           "dialogos": [f"{d['tipo']}, {d['titulo']}, {d['mensaje']}" for d in nuevos]})
    # Detener y guardar con una corrida simulada que no responde.
    resultados.append({"control": "rótulos de campos", "resultado": "ok",
                       "detalle": ", ".join(campos)})
    v.update()
    v.destroy()
    despues = huellas()
    cambios = [k for k in set(antes) | set(despues) if antes.get(k) != despues.get(k)]
    informe = {"fecha": time.strftime("%Y-%m-%d %H:%M"), "raiz": str(RAIZ_P00), "python": sys.version,
               "ejecutable": sys.executable, "resultados": resultados, "errores": ERRORES,
               "archivos_de_configuracion_cambiados": cambios}
    for r in resultados:
        print(f"{r['resultado'][:40]:40s} {r['control']}")
        for d in r.get("dialogos", []):
            print(f"{'':40s}   {d}")
    print(f"\nBotones y controles revisados {len(resultados)}, errores {len(ERRORES)}, "
          f"archivos de configuración cambiados {len(cambios)}")
    for e in ERRORES:
        print(e)
    if ARGS.salida:
        Path(ARGS.salida).write_text(json.dumps(informe, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.exit(1 if ERRORES or cambios else 0)


if __name__ == "__main__":
    main()
