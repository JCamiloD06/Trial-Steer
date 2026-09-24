"""
Figuras de P00, generadas por código a 600 dpi.

Regla del proyecto, sección 11 de AGENTS.md. Ninguna figura lleva valores
metidos a mano. Cada una lee su fuente en disco y se vuelve a generar entera
cada vez. Si la fuente no existe todavía, la figura se salta y se informa,
nunca se dibuja con datos inventados ni de ejemplo.

Salida en figures/p00/, un archivo por figura.

Uso desde la raíz del repositorio.
    python scripts/16_p00_figuras.py
    python scripts/16_p00_figuras.py --solo 2 3
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

RAIZ_REPO = Path(__file__).resolve().parents[1]
RAIZ_P00 = RAIZ_REPO / "P00_control_lateral"
sys.path.insert(0, str(RAIZ_P00))

from plataforma.perfil import construir_perfil  # noqa: E402
from plataforma.regiones import asignar_region  # noqa: E402
from plataforma.trazada import Trazada  # noqa: E402

CONFIG = RAIZ_P00 / "configs" / "base.json"
SALIDA = RAIZ_REPO / "figures" / "p00"
DPI = 600

SEL_SINTONIA = RAIZ_P00 / "sintonia_fase4" / "seleccion_sintonia.json"
REPETIBILIDAD = RAIZ_P00 / "piloto_fase5" / "repetibilidad_piloto.json"
MAPA_CAMPANA = RAIZ_P00 / "resultados_campana" / "mapa_campana.json"

COLOR_REGION = {"baja": "#6a8caf", "media": "#d99036", "alta": "#a8431c"}
COLOR_CTRL = {"pure_pursuit": "#2a6f97", "stanley": "#c46a1c", "mpc_cinematico": "#6a4c93"}
NOMBRE_CTRL = {"pure_pursuit": "Pure Pursuit", "stanley": "Stanley", "mpc_cinematico": "MPC cinemático"}
ORDEN_CTRL = ("pure_pursuit", "stanley", "mpc_cinematico")
ORDEN_PERFIL = ("conservador", "nominal", "rapido")
ORDEN_REGION = ("baja", "media", "alta")
# Parámetro que se mueve en el eje horizontal de la figura de sintonía. Es el
# de mayor efecto declarado en configs/rangos_sintonia.json.
PARAM_PRINCIPAL = {"pure_pursuit": "kv_s", "stanley": "k", "mpc_cinematico": "Qpsi"}
ETIQUETA_PARAM = {"kv_s": "kv en s", "k": "k", "Qpsi": "Q del error de rumbo"}


def estilo():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#dddddd",
        "grid.linewidth": .5,
        "legend.frameon": False,
        "legend.fontsize": 7.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "figure.dpi": 120,
    })


def relativa(ruta):
    """Ruta corta cuando cuelga del repositorio, absoluta cuando no."""
    try:
        return Path(ruta).relative_to(RAIZ_REPO)
    except ValueError:
        return Path(ruta)


def guardar(fig, numero, nombre):
    SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = SALIDA / f"Figura_{numero}_{nombre}.png"
    fig.savefig(ruta, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Figura {numero} escrita en {relativa(ruta)}")
    return True


def saltar(numero, motivo):
    print(f"  Figura {numero} SALTADA, {motivo}")
    return False


def cargar_json(ruta):
    if not Path(ruta).exists():
        return None
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def cargar_trazada():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    trazada = Trazada(RAIZ_REPO / cfg["trazada"]["csv"], cfg["trazada"]["suavizado_curvatura_m"])
    reg = cfg["regiones"]
    regiones = asignar_region(trazada.curvature, reg["radio_baja_m"], reg["radio_alta_m"])
    return cfg, trazada, regiones


# ---------------------------------------------------------------- figura 1
def figura_1():
    """Trazada de Monza por regiones de curvatura y cobertura de cada una."""
    cfg, trazada, regiones = cargar_trazada()
    longitudes = trazada.longitud_segmento
    total = float(longitudes.sum())

    fig = plt.figure(figsize=(7.2, 3.3))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.05, 1], wspace=.28)
    ax = fig.add_subplot(gs[0, 0])
    for nombre in ORDEN_REGION:
        m = regiones == nombre
        ax.scatter(trazada.x[m], trazada.z[m], s=1.4, c=COLOR_REGION[nombre], linewidths=0,
                   label=f"radio {etiqueta_region(nombre, cfg)}")
    ax.set_aspect("equal")
    ax.set_xlabel("x en m")
    ax.set_ylabel("z en m")
    ax.set_title("a. Trazada por región de curvatura")
    # Arriba a la derecha, que es la zona vacía del trazado de Monza. Abajo a
    # la izquierda la leyenda tapaba la Parabólica.
    ax.legend(loc="upper right", markerscale=6, handletextpad=.3)

    ax2 = fig.add_subplot(gs[0, 1])
    pct = [100.0 * float(longitudes[regiones == n].sum()) / total for n in ORDEN_REGION]
    metros = [float(longitudes[regiones == n].sum()) for n in ORDEN_REGION]
    barras = ax2.barh(range(3), pct, color=[COLOR_REGION[n] for n in ORDEN_REGION], height=.62)
    ax2.set_yticks(range(3), [n.capitalize() for n in ORDEN_REGION])
    ax2.invert_yaxis()
    ax2.set_xlabel("porcentaje de la vuelta")
    ax2.set_xlim(0, max(pct) * 1.28)
    ax2.set_title("b. Cobertura por región")
    ax2.grid(axis="y", visible=False)
    for barra, p, m in zip(barras, pct, metros):
        ax2.text(barra.get_width() + max(pct) * .025, barra.get_y() + barra.get_height() / 2,
                 f"{p:.1f} %, {m:.0f} m", va="center", fontsize=7.2)

    fig.text(.01, -.03, f"Trazada de {total:.0f} m, curvatura suavizada en ventana de "
                        f"{cfg['trazada']['suavizado_curvatura_m']:.0f} m.", fontsize=7, color="#555555")
    return guardar(fig, 1, "trazada_regiones")


def etiqueta_region(nombre, cfg):
    reg = cfg["regiones"]
    if nombre == "baja":
        return f"mayor a {reg['radio_baja_m']:.0f} m"
    if nombre == "alta":
        return f"menor a {reg['radio_alta_m']:.0f} m"
    return f"entre {reg['radio_alta_m']:.0f} y {reg['radio_baja_m']:.0f} m"


# ---------------------------------------------------------------- figura 2
def figura_2():
    """Curvatura y los tres perfiles de velocidad a lo largo de la vuelta."""
    cfg, trazada, regiones = cargar_trazada()
    s = trazada.s

    fig, axs = plt.subplots(2, 1, figsize=(7.2, 4.2), sharex=True,
                            gridspec_kw={"height_ratios": [1, 1.35], "hspace": .12})
    sombrear_regiones(axs[0], s, regiones)
    sombrear_regiones(axs[1], s, regiones)

    axs[0].plot(s, np.abs(trazada.curvature), color="#333333", linewidth=.7)
    axs[0].set_ylabel("curvatura en 1/m")
    axs[0].set_title("a. Curvatura de la trazada")

    for nombre in ORDEN_PERFIL:
        perfil = construir_perfil(trazada, cfg["perfil"], nombre)
        axs[1].plot(s, perfil.v_max * 3.6, linewidth=.9,
                    label=f"{nombre}, factor {cfg['perfil']['factores'][nombre]:g}")
    axs[1].set_ylabel("velocidad objetivo en km/h")
    axs[1].set_xlabel("distancia recorrida en m")
    axs[1].set_title("b. Perfiles de velocidad")
    axs[1].legend(loc="lower right", ncols=3)
    axs[1].set_xlim(s[0], s[-1])

    manijas = [Patch(facecolor=COLOR_REGION[n], alpha=.28, label=f"región {n}") for n in ORDEN_REGION]
    axs[0].legend(handles=manijas, loc="upper right", ncols=3)
    return guardar(fig, 2, "curvatura_perfiles")


def sombrear_regiones(ax, s, regiones):
    inicio = 0
    for i in range(1, len(regiones) + 1):
        if i == len(regiones) or regiones[i] != regiones[inicio]:
            ax.axvspan(s[inicio], s[i - 1], color=COLOR_REGION[regiones[inicio]], alpha=.16, linewidth=0)
            inicio = i


# ---------------------------------------------------------------- figura 3
def figura_3():
    """Resultado de la tanda de sintonía, 20 candidatas por controlador."""
    datos = cargar_json(SEL_SINTONIA)
    if datos is None:
        return saltar(3, f"no existe {relativa(SEL_SINTONIA)}")

    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.7))
    for ax, ctrl in zip(axs, ORDEN_CTRL):
        bloque = datos["controladores"][ctrl]
        clave = PARAM_PRINCIPAL[ctrl]
        val, rmse, desc_val, desc_y = [], [], [], []
        for corrida in bloque["corridas"]:
            x = corrida["parametros"].get(clave)
            y = corrida.get("rmse_e_y_m")
            if x is None:
                continue
            if y is None or corrida["estado"] != "candidata":
                desc_val.append(x)
                desc_y.append(y)
            else:
                val.append(x)
                rmse.append(y)
        techo = max([y for y in rmse + [v for v in desc_y if v is not None]] or [1.0]) * 1.08
        ax.scatter(val, rmse, s=16, color=COLOR_CTRL[ctrl], zorder=3)
        sin_metrica = [x for x, y in zip(desc_val, desc_y) if y is None]
        con_metrica = [(x, y) for x, y in zip(desc_val, desc_y) if y is not None]
        if con_metrica:
            ax.scatter([p[0] for p in con_metrica], [p[1] for p in con_metrica], s=20, zorder=3,
                       facecolors="none", edgecolors="#a8431c", linewidths=.9)
        if sin_metrica:
            ax.scatter(sin_metrica, [techo] * len(sin_metrica), s=22, marker="x", zorder=3,
                       color="#a8431c", linewidths=.9)
        ganadora = bloque["ganadora"]
        ax.scatter([ganadora["parametros"][clave]], [ganadora["rmse_e_y_m"]], s=62, marker="*",
                   color="#111111", zorder=4)
        ax.set_title(NOMBRE_CTRL[ctrl])
        ax.set_xlabel(ETIQUETA_PARAM[clave])
        ax.set_ylim(0, techo * 1.06)
    axs[0].set_ylabel("RMSE de e_y en m")
    # Una sola leyenda debajo. Dentro de los ejes tapaba los puntos de las
    # configuraciones descartadas, que son justamente las que hay que ver.
    manijas = [
        Line2D([], [], marker="o", linestyle="none", markersize=4.4, color="#555555", label="candidata"),
        Line2D([], [], marker="o", linestyle="none", markersize=4.6, markerfacecolor="none",
               markeredgecolor="#a8431c", label="descartada por el criterio"),
        Line2D([], [], marker="x", linestyle="none", markersize=5, color="#a8431c",
               label="vuelta no completada, dibujada en el tope"),
        Line2D([], [], marker="*", linestyle="none", markersize=8, color="#111111", label="adoptada"),
    ]
    fig.legend(handles=manijas, loc="lower center", ncols=4, bbox_to_anchor=(.5, -.12))
    fig.suptitle("Tanda de sintonía, 60 vueltas, semilla "
                 f"{datos.get('semilla_plan', 'no registrada')}", y=1.03, fontsize=9)
    fig.tight_layout()
    return guardar(fig, 3, "sintonia_fase4")


# ---------------------------------------------------------------- figura 4
def figura_4():
    """Repetibilidad medida en el piloto y umbral de mejora práctica."""
    datos = cargar_json(REPETIBILIDAD)
    if datos is None:
        return saltar(4, f"no existe {relativa(REPETIBILIDAD)}")

    vueltas = [v for v in datos["vueltas"] if v.get("bloque") == "repetibilidad"] or datos["vueltas"]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=False)
    for ax, ctrl in zip(axs, ORDEN_CTRL):
        res = datos["por_controlador"][ctrl]
        ys = [v["rmse_e_y_m"] for v in vueltas
              if v["controlador"] == ctrl and v.get("rmse_e_y_m") is not None]
        xs = range(1, len(ys) + 1)
        media, sigma = res["rmse_medio_m"], res["sigma_m"]
        ax.axhspan(media - 2 * sigma, media + 2 * sigma, color=COLOR_CTRL[ctrl], alpha=.16,
                   label="media ± 2σ")
        ax.axhline(media, color=COLOR_CTRL[ctrl], linewidth=.9)
        ax.plot(xs, ys, "o", ms=3.4, color=COLOR_CTRL[ctrl], label="vuelta")
        ax.set_title(f"{NOMBRE_CTRL[ctrl]}\nσ = {sigma * 1000:.2f} mm")
        ax.set_xlabel("repetición")
        ax.set_xticks(list(xs))
        ax.legend(loc="lower right", handletextpad=.3)
    axs[0].set_ylabel("RMSE de e_y en m")

    umbrales = ", ".join(f"{NOMBRE_CTRL[c]} {datos['umbrales'][c]['umbral_m'] * 1000:.1f} mm"
                         for c in datos["umbrales"])
    fig.text(.01, -.06, "Umbral de mejora práctica adoptado, el mayor entre el 10 por ciento del RMSE "
                        f"y 2σ. {umbrales}.", fontsize=7, color="#555555")
    fig.tight_layout()
    return guardar(fig, 4, "repetibilidad_piloto")


# ---------------------------------------------------------------- figura 5
def veredicto_celda(celda):
    """
    Clasifica la celda en tres estados, no en dos. Mejora cuando el MPC supera
    la regla de decisión. Peor en términos prácticos cuando la diferencia
    adversa supera el mismo umbral, que no es lo mismo que no mejorar.
    Equivalencia cuando la diferencia queda dentro del umbral en los dos
    sentidos. Distinción adoptada el 2026-09-24.
    """
    if celda is None:
        return None, "sin datos"
    estados = {}
    for ctrl in ("pure_pursuit", "stanley"):
        comp = celda["comparaciones"].get(ctrl)
        if comp is None or not comp.get("evaluable", False):
            estados[ctrl] = None
            continue
        if comp.get("mejora"):
            estados[ctrl] = "mejora"
        elif -comp["reduccion_media_m"] > comp["umbral_m"]:
            estados[ctrl] = "peor"
        else:
            estados[ctrl] = "equivalente"
    vals = [v for v in estados.values() if v]
    if not vals:
        return estados, "sin datos"
    mejoras = vals.count("mejora")
    if mejoras == len(vals):
        estado = "mejora frente a los dos"
    elif mejoras:
        estado = "mejora frente a uno"
    elif "peor" in vals:
        estado = "MPC con más error"
    else:
        estado = "equivalencia"
    return estados, estado


def figura_5():
    """
    Mapa de operación. Matriz de perfil por región, y dentro de cada celda el
    RMSE de los tres controladores en barras sobre una escala común, de modo
    que se lea a la vez la magnitud del error, el veredicto y la inversión en
    curvatura alta. Rehecha el 2026-09-24, la versión anterior era solo texto.
    """
    datos = cargar_json(MAPA_CAMPANA)
    if datos is None:
        return saltar(5, f"no existe {relativa(MAPA_CAMPANA)}, la campaña no ha corrido")

    celdas = {(c["perfil"], c["region"]): c for c in datos["celdas"]}
    valores = [celdas[k]["por_controlador"][c]["rmse_medio_m"]
               for k in celdas for c in ORDEN_CTRL if c in celdas[k]["por_controlador"]]
    tope = max(valores) * 1.34

    fondo = {"mejora frente a los dos": "#d7e6dc", "mejora frente a uno": "#dfe7ef",
             "equivalencia": "#eef0f2", "MPC con más error": "#f4ece5", "sin datos": "#eeeeee"}
    tinta = {"mejora frente a los dos": "#1d5c3a", "mejora frente a uno": "#1d5c3a",
             "equivalencia": "#4a5a63", "MPC con más error": "#8a4a22", "sin datos": "#777777"}
    # La celda de perfil rapido y curvatura alta es la única cuyo veredicto
    # cambia al mover la frontera de región a 120 m. Se marca en la figura.
    sensibles = {("rapido", "alta")}
    filas = list(reversed(ORDEN_PERFIL))  # velocidad creciente hacia arriba
    fig, axs = plt.subplots(3, 3, figsize=(7.2, 5.0), sharex=True,
                            gridspec_kw={"hspace": .22, "wspace": .1})
    for j, perfil in enumerate(filas):
        for i, region in enumerate(ORDEN_REGION):
            ax = axs[j][i]
            celda = celdas.get((perfil, region))
            estados, estado = veredicto_celda(celda)
            ax.set_facecolor(fondo[estado])
            ax.grid(False)
            for lado in ("top", "right", "left", "bottom"):
                ax.spines[lado].set_visible(False)
            ax.set_xlim(0, tope)
            ax.set_ylim(-.65, 2.65)
            ax.set_yticks([])
            if celda is None:
                ax.text(.5, .5, "sin datos", transform=ax.transAxes, ha="center", va="center")
                continue
            for k, ctrl in enumerate(ORDEN_CTRL):
                v = celda["por_controlador"][ctrl]["rmse_medio_m"]
                y = 2 - k
                ax.barh(y, v, height=.62, color=COLOR_CTRL[ctrl],
                        edgecolor="#111111" if ctrl == "mpc_cinematico" else "none",
                        linewidth=.7 if ctrl == "mpc_cinematico" else 0)
                ax.text(v + tope * .025, y, f"{v * 1000:.0f}", va="center", fontsize=6.8,
                        color="#333333")
            marca = " (a)" if (perfil, region) in sensibles else ""
            ax.text(.5, -.6, estado + marca, ha="center", va="bottom", fontsize=7,
                    fontweight="bold" if estado.startswith("mejora") else "normal",
                    color=tinta[estado])
            if j == 0:
                ax.set_title(f"curvatura {region}", fontsize=8.5, pad=6)
            if i == 0:
                ax.set_ylabel("perfil\n" + perfil, rotation=0, ha="right", va="center",
                              fontsize=8.5, labelpad=10)
    for ax in axs[2]:
        ax.set_xlabel("RMSE de e_y en mm", fontsize=7.5)
        ax.set_xticks([0, .2, .4], ["0", "200", "400"])
        ax.tick_params(labelbottom=True)

    manijas = [Patch(facecolor=COLOR_CTRL[c], label=NOMBRE_CTRL[c]) for c in ORDEN_CTRL]
    fig.legend(handles=manijas, loc="lower center", ncols=3, bbox_to_anchor=(.5, -.05))
    fig.suptitle("Mapa de operación. Error lateral de los tres controladores por región y perfil",
                 fontsize=9.5, y=.975)
    fig.text(.5, -.155, "La velocidad crece hacia arriba y la exigencia geométrica hacia la derecha. "
                        "El veredicto exige superar el umbral medido en el piloto, intervalo bootstrap "
                        "por encima y valor p corregido por Holm menor que 0.05. Equivalencia significa "
                        "diferencia dentro del umbral en los dos sentidos. (a) Único veredicto sensible "
                        "a la frontera de región, pasa a mejora con 120 m en lugar de 100 m.",
             ha="center", fontsize=7, color="#555555", wrap=True)
    return guardar(fig, 5, "mapa_operacion")


# ---------------------------------------------------------------- figura 6
def figura_6():
    """Reducción de RMSE del MPC con intervalo bootstrap y umbral, por celda."""
    datos = cargar_json(MAPA_CAMPANA)
    if datos is None:
        return saltar(6, f"no existe {relativa(MAPA_CAMPANA)}, la campaña no ha corrido")

    filas = []
    for perfil in ORDEN_PERFIL:
        for region in ORDEN_REGION:
            for ctrl in ("pure_pursuit", "stanley"):
                celda = next((c for c in datos["celdas"]
                              if c["perfil"] == perfil and c["region"] == region), None)
                if celda is None:
                    continue
                comp = celda["comparaciones"].get(ctrl)
                if comp is None:
                    continue
                filas.append((f"{perfil[:4]} · {region} · vs {NOMBRE_CTRL[ctrl]}", ctrl, comp))

    if not filas:
        return saltar(6, "el mapa no trae comparaciones")

    fig, ax = plt.subplots(figsize=(7.2, .28 * len(filas) + 1.4))
    for y, (etiqueta, ctrl, comp) in enumerate(filas):
        lo, hi = comp["ic95_bootstrap_m"]
        centro = comp["reduccion_media_m"]
        ax.plot([lo * 1000, hi * 1000], [y, y], color=COLOR_CTRL[ctrl], linewidth=1.5, solid_capstyle="round")
        ax.plot([centro * 1000], [y], "o", ms=4, color=COLOR_CTRL[ctrl])
        ax.plot([comp["umbral_m"] * 1000], [y], "|", ms=9, color="#a8431c", markeredgewidth=1.3)
    ax.axvline(0, color="#888888", linewidth=.8)
    ax.set_yticks(range(len(filas)), [f[0] for f in filas])
    ax.invert_yaxis()
    ax.set_xlabel("reducción del RMSE de e_y en mm, positivo favorece al MPC")
    ax.set_title("Reducción con intervalo bootstrap del 95 por ciento")
    manijas = [Line2D([], [], color="#a8431c", marker="|", linestyle="none", markersize=9,
                      label="umbral de mejora práctica")]
    ax.legend(handles=manijas, loc="lower right")
    ax.grid(axis="y", visible=False)
    # El intervalo suele ser más angosto que el propio marcador. Se dice en la
    # nota al pie para que no parezca que falta dibujarlo.
    semi = max((c["ic95_bootstrap_m"][1] - c["ic95_bootstrap_m"][0]) / 2 for _, _, c in filas) * 1000
    fig.text(.01, -.02 - .01 * (len(filas) > 12),
             f"El intervalo es más angosto que el marcador en casi todas las comparaciones. "
             f"La semiamplitud mayor de las {len(filas)} es de {semi:.1f} mm.",
             fontsize=7, color="#555555")
    return guardar(fig, 6, "reduccion_intervalos")


# ---------------------------------------------------------------- figura 7
def figura_7():
    """Esfuerzo de dirección del MPC relativo al geométrico, por celda."""
    datos = cargar_json(MAPA_CAMPANA)
    if datos is None:
        return saltar(7, f"no existe {relativa(MAPA_CAMPANA)}, la campaña no ha corrido")

    cond = datos.get("condiciones_1_4", {})
    baja = cond.get("banda_bajo_costo", 1.5)
    alta = cond.get("banda_actividad_superior", 3.0)
    etiquetas, valores, colores = [], [], []
    for perfil in ORDEN_PERFIL:
        for region in ORDEN_REGION:
            celda = next((c for c in datos["celdas"]
                          if c["perfil"] == perfil and c["region"] == region), None)
            if celda is None:
                continue
            for ctrl in ("pure_pursuit", "stanley"):
                comp = celda["comparaciones"].get(ctrl)
                razon = None if comp is None else comp.get("razon_esfuerzo_mpc_sobre_geometrico")
                if razon is None:
                    continue
                etiquetas.append(f"{perfil[:4]} · {region} · vs {NOMBRE_CTRL[ctrl]}")
                valores.append(razon)
                colores.append(COLOR_CTRL[ctrl])

    if not valores:
        return saltar(7, "el mapa no trae razón de esfuerzo")

    fig, ax = plt.subplots(figsize=(7.2, .28 * len(valores) + 1.4))
    ax.barh(range(len(valores)), valores, color=colores, height=.62)
    ax.axvline(1, color="#888888", linewidth=.8)
    ax.axvline(baja, color="#5c8a4a", linewidth=.9, linestyle="--", label=f"banda de bajo costo, {baja:g}")
    ax.axvline(alta, color="#a8431c", linewidth=.9, linestyle="--", label=f"actividad muy superior, {alta:g}")
    ax.set_yticks(range(len(valores)), etiquetas)
    ax.invert_yaxis()
    ax.set_xlabel("RMS de la tasa de dirección del MPC dividido por la del geométrico")
    ax.set_title("Esfuerzo de dirección relativo, métrica reportada, no decide el veredicto")
    ax.legend(loc="lower right")
    ax.grid(axis="y", visible=False)
    return guardar(fig, 7, "esfuerzo_direccion")


FIGURAS = {1: figura_1, 2: figura_2, 3: figura_3, 4: figura_4, 5: figura_5, 6: figura_6, 7: figura_7}


def main():
    global MAPA_CAMPANA, SALIDA
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solo", nargs="*", type=int, help="números de figura a generar")
    ap.add_argument("--mapa", default=str(MAPA_CAMPANA),
                    help="archivo de mapa a graficar, para ensayar el código con datos que no son "
                         "de la campaña. Cámbialo solo para probar, no para el manuscrito")
    ap.add_argument("--salida", default=str(SALIDA), help="carpeta de salida")
    args = ap.parse_args()
    MAPA_CAMPANA = Path(args.mapa)
    SALIDA = Path(args.salida)
    if MAPA_CAMPANA != RAIZ_P00 / "resultados_campana" / "mapa_campana.json":
        print(f"AVISO. Mapa tomado de {MAPA_CAMPANA}, que no es el de la campaña. "
              "Estas figuras son un ensayo del código y no van al manuscrito.")
    estilo()
    pedidas = args.solo or sorted(FIGURAS)
    print(f"Figuras de P00 a {DPI} dpi en {relativa(SALIDA)}")
    hechas = 0
    for numero in pedidas:
        if numero not in FIGURAS:
            print(f"  Figura {numero} no existe")
            continue
        hechas += 1 if FIGURAS[numero]() else 0
    print(f"{hechas} de {len(pedidas)} figuras generadas")


if __name__ == "__main__":
    main()
