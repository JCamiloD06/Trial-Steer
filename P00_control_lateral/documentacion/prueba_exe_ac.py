"""
Prueba con Assetto Corsa de los botones que abren el simulador.

Código auxiliar nuevo, no modifica ningún script existente. Pensado para
correr con el ejecutable sobre la carpeta de la distribución, de modo que las
corridas quedan dentro de esa carpeta y no en los datos del estudio.

Pasos.
    1. Iniciar corrida con Pure Pursuit, fase prueba, sesión 0, hasta completar la vuelta.
    2. Iniciar corrida con Stanley y Detener y guardar a los 60 s.
    3. Iniciar MPC completo, Detener y guardar a los 90 s de activado y Generar gráficas.
    4. Cerrar la ventana.

Los diálogos se contestan solos. Solo se acepta cerrar y reabrir el juego
cuando el carro no está en la salida. Todo lo demás se contesta con No.

Uso.
    Trial_Steer_consola.exe prueba_exe_ac.py --raiz <carpeta P00_control_lateral de la distribución>
"""
import argparse
import json
import sys
import time
import traceback
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", required=True)
ap.add_argument("--salida", default="")
ARGS = ap.parse_args()
RAIZ_P00 = Path(ARGS.raiz).resolve()
sys.path.insert(0, str(RAIZ_P00))

from tkinter import messagebox  # noqa: E402

from lanzador import app as mod_app  # noqa: E402

DIALOGOS, ERRORES, PASOS = [], [], []


def log(texto):
    print(f"{time.strftime('%H:%M:%S')} {texto}", flush=True)


def registrar(tipo, respuesta=None):
    def f(*a, **k):
        titulo = a[0] if a else ""
        mensaje = a[1] if len(a) > 1 else ""
        r = respuesta(titulo, mensaje) if callable(respuesta) else respuesta
        DIALOGOS.append(f"{tipo}, {titulo}, {mensaje[:140]}, respuesta {r}")
        log(f"diálogo {tipo}, {titulo}, {mensaje[:140]}, respuesta {r}")
        return r
    return f


for n in ("showinfo", "showerror", "showwarning"):
    setattr(messagebox, n, registrar(n, "ok"))
messagebox.askyesno = registrar("askyesno", lambda t, m: t == "Assetto Corsa" and "reabrir" in m)


class Guion:
    def __init__(self, v):
        self.v = v
        self.t0 = None
        self.etapa = None

    def paso(self, nombre, ok, detalle=""):
        PASOS.append({"paso": nombre, "ok": bool(ok), "detalle": str(detalle)})
        log(f"{'OK   ' if ok else 'FALLA'} {nombre} {detalle}")

    def configurar(self, ctrl, etiqueta):
        v = self.v
        v.nb_principal.select(0)
        v.nb.select(0)
        v.var_fase.set("prueba")
        v.var_ctrl.set(ctrl)
        v.var_perfil.set("conservador")
        v.var_sesion.set(0)
        v.var_etiqueta.set(etiqueta)
        v.var_id_plan.set("")
        v.var_tmax.set("")

    def corrida_completa(self):
        self.configurar("pure_pursuit", "doc_exe_completa")
        self.v.iniciar()
        self.t0 = None
        self.esperar_corrida(detener_a=None, siguiente=self.corrida_detenida, nombre="Iniciar corrida hasta completar la vuelta")

    def corrida_detenida(self):
        self.configurar("stanley", "doc_exe_detenida")
        self.v.iniciar()
        self.t0 = None
        self.esperar_corrida(detener_a=60.0, siguiente=self.mpc, nombre="Detener y guardar en una corrida")

    def esperar_corrida(self, detener_a, siguiente, nombre):
        v = self.v

        def vigilar():
            if v.preparando:
                v.after(1000, vigilar)
                return
            if v.proceso is not None:
                if self.t0 is None:
                    self.t0 = time.time()
                    log(f"{nombre}, corrida en curso")
                if detener_a is not None and time.time() - self.t0 > detener_a and v.archivo_detener:
                    log("se pulsa Detener y guardar")
                    v.detener()
                    detener_hecho[0] = True
                v.after(1000, vigilar)
                return
            carpeta = v.carpeta_ultima
            if carpeta and Path(carpeta).exists():
                man = json.loads((Path(carpeta) / "manifiesto.json").read_text(encoding="utf-8"))
                completada = man["resumen"].get("vuelta_completada")
                notas = man.get("notas", [])
                if detener_a is None:
                    self.paso(nombre, completada, f"{Path(carpeta).name}, tiempo {man['resumen'].get('tiempo_vuelta_s')}")
                else:
                    self.paso(nombre, detener_hecho[0] and any("lanzador" in n for n in notas),
                              f"{Path(carpeta).name}, notas {notas}")
            else:
                self.paso(nombre, False, "sin carpeta de corrida")
            v.after(3000, siguiente)

        detener_hecho = [False]
        v.after(1000, vigilar)

    def mpc(self):
        v = self.v
        v.nb_principal.select(1)
        v.iniciar_mpc()
        estado = {"t": None, "detenido": False, "graficas": False, "tg": None}

        def vigilar():
            if v.preparando:
                v.after(1000, vigilar)
                return
            if v.proceso_mpc is not None:
                if estado["t"] is None:
                    estado["t"] = time.time()
                    log("MPC completo en curso")
                if not estado["detenido"] and time.time() - estado["t"] > 90:
                    log("se pulsa Detener y guardar del MPC completo")
                    v.detener_mpc()
                    estado["detenido"] = True
                v.after(1000, vigilar)
                return
            if not estado["graficas"]:
                ok = bool(v.carpeta_mpc) and Path(v.carpeta_mpc).exists()
                self.paso("Iniciar MPC completo y Detener y guardar", ok and estado["detenido"],
                          f"carpeta {v.carpeta_mpc}, salvaguarda {v.anti_bloqueos_mpc}")
                if not ok:
                    v.after(1000, self.cerrar)
                    return
                estado["graficas"] = True
                estado["tg"] = time.time()
                v.generar_graficas_mpc()
                v.after(2000, vigilar)
                return
            if str(v.bt_mpc_graficas.cget("state")) == "disabled" and time.time() - estado["tg"] < 180:
                v.after(1000, vigilar)
                return
            figuras = sorted((Path(v.carpeta_mpc) / "figuras").glob("*.png")) if v.carpeta_mpc else []
            self.paso("Generar gráficas", len(figuras) > 0, f"{len(figuras)} figuras")
            v.after(1000, self.cerrar)

        v.after(1000, vigilar)

    def cerrar(self):
        v = self.v
        try:
            v._cerrar()
            self.paso("Cerrar la ventana", True)
        except Exception as e:
            self.paso("Cerrar la ventana", False, e)


def main():
    v = mod_app.Lanzador()
    v.report_callback_exception = lambda e, val, tb: ERRORES.append("".join(traceback.format_exception(e, val, tb)))
    g = Guion(v)
    v.after(2000, g.corrida_completa)
    v.mainloop()
    informe = {"pasos": PASOS, "dialogos": DIALOGOS, "errores": ERRORES, "ejecutable": sys.executable}
    if ARGS.salida:
        Path(ARGS.salida).write_text(json.dumps(informe, indent=2, ensure_ascii=False), encoding="utf-8")
    fallas = [p for p in PASOS if not p["ok"]]
    log(f"pasos {len(PASOS)}, fallas {len(fallas)}, errores de la interfaz {len(ERRORES)}")
    for e in ERRORES:
        print(e)
    sys.exit(1 if fallas or ERRORES or len(PASOS) < 5 else 0)


if __name__ == "__main__":
    main()
