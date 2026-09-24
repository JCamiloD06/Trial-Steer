"""
Capturas reales del lanzador y corridas de demostración para el Manual de usuario.

Código auxiliar nuevo, no modifica ningún script existente. Abre la ventana
real del lanzador, Lanzador de lanzador/app.py, y la maneja desde dentro del
mismo proceso con sus variables y métodos, como lo haría un usuario.

Restricciones que respeta.
    Todas las corridas son de fase prueba, sesión 0 y etiqueta que empieza por doc_.
    No pulsa Generar plan, Usar siguiente, Correr la sesión ni Repetir seleccionada.
    Las pestañas de planes solo se capturan en su estado actual.

Las capturas se toman con PrintWindow de Windows sobre la ventana del
lanzador, que no le quita el foco al simulador.

Uso desde la raíz del repositorio, con el simulador cerrado.
    python P00_control_lateral/documentacion/capturas_lanzador.py
    python P00_control_lateral/documentacion/capturas_lanzador.py --solo-capturas
"""
import argparse
import ctypes
import json
import sys
import time
from ctypes import wintypes
from pathlib import Path

from PIL import Image

DIR = Path(__file__).resolve().parent
RAIZ_P00 = DIR.parent
sys.path.insert(0, str(RAIZ_P00))

from lanzador import app as mod_app  # noqa: E402

CAPTURAS = DIR / "capturas"
REGISTRO = DIR / "capturas" / "corridas_doc.json"

EXPERIMENTOS = [
    {"n": 1, "controlador": "pure_pursuit", "perfil": "conservador", "etiqueta": "doc_pp_conservador"},
    {"n": 2, "controlador": "stanley", "perfil": "conservador", "etiqueta": "doc_st_conservador"},
    {"n": 3, "controlador": "mpc_cinematico", "perfil": "conservador", "etiqueta": "doc_mpc_conservador"},
    {"n": 5, "controlador": "stanley", "perfil": "nominal", "etiqueta": "doc_st_nominal"},
]
SEGUNDOS_SALIDA_EN_VIVO = 150.0

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
                ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)]


def log(texto):
    print(f"{time.strftime('%H:%M:%S')} {texto}", flush=True)


def capturar(ventana, nombre):
    """Imagen de la ventana completa con PrintWindow, aunque otra ventana la tape."""
    ventana.update_idletasks()
    ventana.update()
    hwnd = int(ventana.wm_frame(), 16)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    w, h = rect.right - rect.left, rect.bottom - rect.top
    hdc = user32.GetWindowDC(hwnd)
    mem = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(mem, bmp)
    user32.PrintWindow(hwnd, mem, 2)
    bih = BITMAPINFOHEADER()
    bih.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bih.biWidth, bih.biHeight, bih.biPlanes, bih.biBitCount = w, -h, 1, 32
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mem, bmp, 0, h, buf, ctypes.byref(bih), 0)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mem)
    user32.ReleaseDC(hwnd, hdc)
    img = Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB")
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    img.save(CAPTURAS / nombre, dpi=(96, 96))
    log(f"captura {nombre} {w}x{h}")


class Guion:
    def __init__(self, ventana, solo_capturas):
        self.v = ventana
        self.solo = solo_capturas
        self.pendientes = list(EXPERIMENTOS)
        self.actual = None
        self.t_proceso = None
        self.vivo_hecho = False
        self.resultados = []

    def esperar(self, ms, funcion):
        self.v.after(ms, funcion)

    def estaticas(self):
        v = self.v
        v.nb_principal.select(0)
        v.nb.select(0)
        capturar(v, "01_lanzador_inicio.png")
        for indice, nombre in ((1, "06_plan_campana.png"), (2, "07_tanda_sintonia.png"), (3, "08_piloto.png")):
            v.nb.select(indice)
            self.v.update()
            time.sleep(0.5)
            capturar(v, nombre)
        v.nb_principal.select(1)
        self.v.update()
        time.sleep(0.5)
        capturar(v, "10_mpc_completo.png")
        v.nb_principal.select(0)
        v.nb.select(0)
        v.var_fase.set("prueba")
        v.var_sesion.set(0)
        capturar(v, "02_pestana_corrida.png")
        if self.solo:
            self.fin()
        else:
            self.esperar(500, self.siguiente)

    def configurar(self, e):
        v = self.v
        v.nb_principal.select(0)
        v.nb.select(0)
        v.var_fase.set("prueba")
        v.var_ctrl.set(e["controlador"])
        v.var_perfil.set(e["perfil"])
        v.var_sesion.set(0)
        v.var_etiqueta.set(e["etiqueta"])
        v.var_id_plan.set("")
        v.var_tmax.set("")
        v.var_sin_verif.set(False)
        v.var_config.set(str(mod_app.CONFIG_BASE))

    def siguiente(self):
        if not self.pendientes:
            self.verificacion()
            return
        e = self.pendientes.pop(0)
        self.actual = e
        self.configurar(e)
        self.v.update()
        if e["n"] == 1:
            capturar(self.v, "03_configuracion_corrida.png")
        log(f"experimento {e['n']}, {e['controlador']} {e['perfil']} {e['etiqueta']}")
        self.v._argumentos(validar=True)
        self.v.txt_log.delete("1.0", "end")
        # Igual que la tanda del lanzador, reinicia la sesión del juego antes de cada vuelta.
        self.v._iniciar_preparacion(reiniciar=True, destino="p00")
        self.t_proceso = None
        self.vivo_hecho = False
        self.esperar(1000, self.vigilar)

    def vigilar(self):
        v = self.v
        if v.preparando:
            self.esperar(1000, self.vigilar)
            return
        if v.proceso is not None:
            if self.t_proceso is None:
                self.t_proceso = time.time()
                log("corrida en curso")
            if (self.actual["n"] == 1 and not self.vivo_hecho
                    and time.time() - self.t_proceso > SEGUNDOS_SALIDA_EN_VIVO):
                capturar(v, "04_salida_en_vivo.png")
                self.vivo_hecho = True
            self.esperar(1000, self.vigilar)
            return
        if self.t_proceso is None:
            log("la preparación terminó sin corrida, se detiene el guion")
            self.fin()
            return
        carpeta = v.carpeta_ultima
        log(f"experimento {self.actual['n']} terminado, carpeta {carpeta}")
        self.resultados.append(dict(self.actual, carpeta=carpeta))
        if self.actual["n"] == 1:
            capturar(v, "05_resumen_corrida.png")
        if carpeta is None:
            self.fin()
            return
        self.esperar(3000, self.siguiente)

    def verificacion(self):
        v = self.v
        v.nb.select(4)
        v.refrescar_verificacion()
        primera = next((r["carpeta"] for r in self.resultados if r["n"] == 1), None)
        clave = next((k for k, c in v.mapa_verif.items() if primera and Path(c) == Path(primera)), None)
        if clave:
            v.var_corrida_verif.set(clave)
            v.evaluar()
            v.update()
            time.sleep(0.5)
            capturar(v, "09_verificacion_fase3.png")
        else:
            log("no se encontró la corrida del experimento 1 en la lista de verificación")
        self.fin()

    def fin(self):
        if self.resultados:
            REGISTRO.write_text(json.dumps(self.resultados, indent=2, ensure_ascii=False), encoding="utf-8")
        log("guion terminado")
        self.v.after(1000, self.v.destroy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-capturas", action="store_true")
    args = ap.parse_args()
    ventana = mod_app.Lanzador()
    ventana.geometry("1180x840+0+0")
    guion = Guion(ventana, args.solo_capturas)
    ventana.after(2500, guion.estaticas)
    ventana.mainloop()


if __name__ == "__main__":
    main()
