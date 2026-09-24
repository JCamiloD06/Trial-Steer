"""
Resultados de las corridas de demostración del Manual de usuario.

Código auxiliar nuevo, no modifica ningún script existente. Lee las corridas
doc_ registradas por capturas_lanzador.py en capturas/corridas_doc.json, les
aplica analisis/metricas_vuelta.py y lanzador/corridas.verificacion_fase3, y
escribe fragmentos de texto en fuentes/fragmentos/ que construir_documentos.py
inserta en el manual. También escribe la figura de comparación a 600 dpi.

Ningún valor se escribe a mano. Todo sale de la telemetría de las corridas.

Uso desde la raíz del repositorio.
    python P00_control_lateral/documentacion/resultados_doc.py
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DIR = Path(__file__).resolve().parent
RAIZ_P00 = DIR.parent
sys.path.insert(0, str(RAIZ_P00))
sys.path.insert(0, str(RAIZ_P00 / "analisis"))

from analisis import metricas_vuelta  # noqa: E402
from lanzador import corridas as mod_corridas  # noqa: E402

FRAG = DIR / "fuentes" / "fragmentos"
FIG = DIR / "figuras"
NOMBRES = {"pure_pursuit": "Pure Pursuit", "stanley": "Stanley", "mpc_cinematico": "MPC cinemático"}


def f(x, nd=3):
    return "sin dato" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{nd}f}"


def columna(carpeta, nombre, solo_medida=True):
    with open(Path(carpeta) / "telemetria.csv", newline="", encoding="utf-8") as fh:
        filas = [r for r in csv.DictReader(fh) if not solo_medida or r["fase_vuelta"] == "medida"]
    datos = []
    for r in filas:
        try:
            datos.append(float(r[nombre]))
        except (TypeError, ValueError):
            datos.append(np.nan)
    return np.array(datos)


def recortar_capturas():
    """Quita el borde negro que PrintWindow deja alrededor de la ventana."""
    from PIL import Image
    for ruta in sorted((DIR / "capturas").glob("*.png")):
        img = np.asarray(Image.open(ruta).convert("RGB")).astype(int)
        oscuro = img.sum(axis=2) < 30
        filas = np.where(oscuro.mean(axis=1) < 0.9)[0]
        cols = np.where(oscuro.mean(axis=0) < 0.9)[0]
        if filas.size and cols.size and (filas[0] > 0 or cols[0] > 0 or filas[-1] + 1 < img.shape[0]
                                         or cols[-1] + 1 < img.shape[1]):
            recorte = img[filas[0]: filas[-1] + 1, cols[0]: cols[-1] + 1]
            Image.fromarray(recorte.astype(np.uint8)).save(ruta, dpi=(96, 96))


def main():
    recortar_capturas()
    corridas = json.loads((DIR / "capturas" / "corridas_doc.json").read_text(encoding="utf-8"))
    with open(RAIZ_P00 / "configs" / "base.json", encoding="utf-8") as fh:
        cfg = json.load(fh)
    FRAG.mkdir(parents=True, exist_ok=True)
    m = {}
    for c in corridas:
        m[c["n"]] = dict(c, met=metricas_vuelta.procesar(c["carpeta"], cfg),
                         man=json.loads((Path(c["carpeta"]) / "manifiesto.json").read_text(encoding="utf-8")))

    def texto_corrida(n):
        d = m[n]
        g = d["met"]["grupos"].get("vuelta", {})
        res = d["man"]["resumen"]
        nombre = Path(d["carpeta"]).name
        completada = "se completó" if d["met"]["vuelta_completada"] else "no se completó"
        return (f"La corrida quedó guardada en la carpeta {nombre}. La vuelta medida {completada} en "
                f"{f(d['met']['tiempo_vuelta_s'], 2)} s, con {d['man']['ciclos']} ciclos registrados en total y "
                f"periodo medio de {f(res.get('periodo_ms_media'), 1)} ms. En la vuelta medida el error cuadrático "
                f"medio del error lateral en la posición del vehículo fue de {f(g.get('rmse_e_y_cg_m'))} m, el tiempo "
                f"de cómputo medio del controlador fue de {f(g.get('tc_ms_media'))} ms con percentil 95 de "
                f"{f(g.get('tc_ms_p95'))} ms, y hubo {g.get('eventos_salida_pista')} salidas de pista.")

    for n in (1, 2):
        if n in m:
            (FRAG / f"exp{n}.md").write_text(texto_corrida(n) + "\n", encoding="utf-8")
    if 3 in m:
        d = m[3]
        tsol = columna(d["carpeta"], "ctrl_extra1")
        it = columna(d["carpeta"], "ctrl_iteraciones")
        resp = columna(d["carpeta"], "ctrl_respaldo")
        extra = (f" En la vuelta medida el solucionador OSQP tardó una mediana de {f(np.nanmedian(tsol))} ms, "
                 f"con percentil 95 de {f(np.nanpercentile(tsol, 95))} ms y máximo de {f(np.nanmax(tsol))} ms, "
                 f"usó una mediana de {np.nanmedian(it):.0f} iteraciones y recurrió a la secuencia de respaldo en "
                 f"{int(np.nansum(resp))} de {len(resp)} ciclos.")
        (FRAG / "exp3.md").write_text(texto_corrida(3) + extra + "\n", encoding="utf-8")

    filas_tabla = []
    for n in (1, 2, 3):
        if n not in m:
            continue
        d = m[n]
        g = d["met"]["grupos"]
        filas_tabla.append(
            f"| {NOMBRES[d['controlador']]} | {f(g['vuelta'].get('rmse_e_y_cg_m'))} | "
            f"{f(g['baja'].get('rmse_e_y_cg_m'))} | {f(g['media'].get('rmse_e_y_cg_m'))} | "
            f"{f(g['alta'].get('rmse_e_y_cg_m'))} | {f(d['met']['tiempo_vuelta_s'], 2)} | "
            f"{f(g['vuelta'].get('rms_tasa_delta_rad_s'), 4)} |")
    if filas_tabla:
        tabla = ("La Tabla [[tab:exp4]] reúne las métricas calculadas por `metricas_vuelta.py` para las tres "
                 "corridas y la Figura [[fig:exp4]] muestra el error lateral por región.\n\n"
                 ": Tabla [[tab:exp4]]. Métricas de la vuelta medida de las corridas de demostración en perfil "
                 "conservador. Error cuadrático medio del error lateral en metros, tiempo de vuelta en segundos y "
                 "valor eficaz de la tasa de dirección en radianes por segundo.\n\n"
                 "| Controlador | Vuelta | Región baja | Región media | Región alta | Tiempo de vuelta | Tasa de dirección |\n"
                 "|---|---|---|---|---|---|---|\n" + "\n".join(filas_tabla) + "\n\n"
                 "![Figura [[fig:exp4]]. Error cuadrático medio del error lateral por región de curvatura en las "
                 "corridas de demostración, una vuelta por controlador. Generada por "
                 "`documentacion/resultados_doc.py`.](figuras/fig_exp4_comparacion.png){width=13cm}\n")
        (FRAG / "exp4.md").write_text(tabla, encoding="utf-8")
        fig, ax = plt.subplots(figsize=(6.2, 3.4))
        regiones = ("vuelta", "baja", "media", "alta")
        ancho = 0.26
        colores = {"pure_pursuit": "#9DB7D5", "stanley": "#E0A33B", "mpc_cinematico": "#003E7E"}
        for i, n in enumerate(k for k in (1, 2, 3) if k in m):
            d = m[n]
            valores = [d["met"]["grupos"][r].get("rmse_e_y_cg_m") or 0.0 for r in regiones]
            ax.bar(np.arange(4) + (i - 1) * ancho, valores, ancho, label=NOMBRES[d["controlador"]],
                   color=colores[d["controlador"]])
        ax.set_xticks(np.arange(4), ["Vuelta", "Región baja", "Región media", "Región alta"])
        ax.set_ylabel("RMSE del error lateral (m)")
        ax.legend(frameon=False, fontsize=8)
        ax.grid(True, axis="y", linewidth=0.3, alpha=0.6)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        fig.savefig(FIG / "fig_exp4_comparacion.png", dpi=600, bbox_inches="tight", facecolor="white")
        fig.savefig(FIG / "fig_exp4_comparacion.tif", dpi=600, bbox_inches="tight", facecolor="white",
                    pil_kwargs={"compression": "tiff_lzw"})
        plt.close(fig)

    if 2 in m and 5 in m:
        a, b = m[2], m[5]
        ga, gb = a["met"]["grupos"]["vuelta"], b["met"]["grupos"]["vuelta"]
        va = np.nanmean(columna(a["carpeta"], "v_kmh"))
        vb = np.nanmean(columna(b["carpeta"], "v_kmh"))
        texto = (f"Con Stanley en perfil nominal la corrida quedó en la carpeta {Path(b['carpeta']).name}. "
                 f"La velocidad media en la vuelta medida pasó de {f(va, 1)} km/h en perfil conservador a "
                 f"{f(vb, 1)} km/h en perfil nominal, el tiempo de vuelta pasó de {f(a['met']['tiempo_vuelta_s'], 2)} s "
                 f"a {f(b['met']['tiempo_vuelta_s'], 2)} s y el error cuadrático medio del error lateral pasó de "
                 f"{f(ga.get('rmse_e_y_cg_m'))} m a {f(gb.get('rmse_e_y_cg_m'))} m. El único cambio entre las dos "
                 f"corridas fue el campo *Perfil*.")
        (FRAG / "exp5.md").write_text(texto + "\n", encoding="utf-8")

    if 1 in m:
        items = mod_corridas.verificacion_fase3(m[1]["carpeta"], cfg)
        cumple = sum(1 for i in items if i["cumple"] is True)
        no = [i["nombre"] for i in items if i["cumple"] is False]
        info = sum(1 for i in items if i["cumple"] is None)
        valores = {i["nombre"]: i["valor"] for i in items}
        def cuenta(k, uno, varios):
            return f"{k} {uno if k == 1 else varios}"

        texto = (f"La evaluación de la corrida del experimento 1 reportó {len(items)} puntos, "
                 f"{cuenta(cumple, 'que cumple', 'que cumplen')}, {cuenta(len(no), 'que no cumple', 'que no cumplen')} "
                 f"y {cuenta(info, 'informativo', 'informativos')}. "
                 + (f"No {'cumple' if len(no) == 1 else 'cumplen'} {', '.join(p.lower() for p in no)}. " if no else "")
                 + f"La batalla medida fue {valores.get('Batalla medida', 'sin dato')}, el periodo medio "
                 f"{valores.get('Periodo medio', 'sin dato')} y la constante de la cadena de dirección "
                 f"reidentificada {valores.get('Constante de la cadena de dirección', 'sin dato')}."
                 + (" Este punto aplica un filtro simple sobre una sola vuelta y su criterio pide revisar la "
                    "calibración cuando la diferencia supera 15 por ciento. La identificación de referencia de la "
                    "constante se hace con `analisis/identificar_direccion.py`, que usa filtros adicionales e "
                    "intervalos por bloques. Una diferencia como esta es una señal para repetir esa identificación, "
                    "no una medición concluyente. El punto no conforme corresponde a una comprobación diagnóstica "
                    "de calibración, no impide la ejecución ni invalida la corrida, y se mantiene en el manual "
                    "para ilustrar cómo se interpreta la pestaña."
                    if "Constante de la cadena de dirección" in no else ""))
        (FRAG / "exp6.md").write_text(texto + "\n", encoding="utf-8")
    resumen = {n: {"carpeta": d["carpeta"], "tiempo_vuelta_s": d["met"]["tiempo_vuelta_s"],
                   "rmse_e_y_cg_m": d["met"]["grupos"].get("vuelta", {}).get("rmse_e_y_cg_m")} for n, d in m.items()}
    print(json.dumps(resumen, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
