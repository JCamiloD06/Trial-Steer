"""
Párrafo de la Descripción del software con el resultado de las pruebas de la
interfaz y del ejecutable.

Código auxiliar nuevo, no modifica ningún script existente. Lee los informes
JSON de pruebas_registro/, escritos por prueba_botones.py, prueba_generar_planes.py
y prueba_exe_ac.py, y escribe fuentes/fragmentos/pruebas_interfaz.md. Si falta
un informe, el párrafo lo dice en lugar de dar un resultado.

Uso desde la raíz del repositorio.
    python P00_control_lateral/documentacion/resumen_pruebas.py
"""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent
REG = DIR / "pruebas_registro"


def leer(nombre):
    ruta = REG / nombre
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


def botones(inf, donde):
    if inf is None:
        return f"La prueba de botones con {donde} no tiene informe."
    r = inf["resultados"]
    pulsados = sum(1 for x in r if x["resultado"] in ("ok", "error"))
    deshab = sum(1 for x in r if x["resultado"] == "deshabilitado en reposo")
    return (f"Con {donde}, `documentacion/prueba_botones.py` revisó {len(r)} botones y controles de las siete "
            f"pestañas, pulsó {pulsados}, encontró {deshab} deshabilitados en reposo, como corresponde cuando no hay "
            f"una corrida en curso, y registró {len(inf['errores'])} errores de la interfaz y "
            f"{len(inf['archivos_de_configuracion_cambiados'])} archivos de configuración modificados.")


def main():
    fuente, exe, planes, ac = (leer("botones_fuente.json"), leer("botones_exe.json"),
                               leer("generar_planes_exe.json"), leer("prueba_exe_ac.json"))
    partes = ["Además de las pruebas automáticas se probó la interfaz completa. Los diálogos se contestaron solos "
              "con No, de modo que ningún botón generó planes ni corrió vueltas sobre los datos del estudio. "
              + botones(fuente, "el código fuente") + " " + botones(exe, "el ejecutable")
              + (" La diferencia entre los dos conteos se debe a que el código fuente tiene los planes del estudio, "
                 "que dejan deshabilitados los botones Generar plan y Añadir bloque tiempo límite, mientras que la "
                 "carpeta del ejecutable se entrega sin planes." if fuente and exe else "")]
    if planes is not None:
        partes.append(f"Sobre una copia del ejecutable sin planes, `documentacion/prueba_generar_planes.py` generó los "
                      f"planes de campaña, sintonía y piloto contestando Sí, cargó una corrida de cada uno en la pestaña "
                      f"*Corrida* y registró {planes['errores']} errores.")
    if ac is not None:
        pasos = ac["pasos"]
        ok = sum(1 for p in pasos if p["ok"])
        nombres = ", ".join(p["paso"] for p in pasos)
        partes.append(f"Con el simulador, `documentacion/prueba_exe_ac.py` ejecutó desde el ejecutable {len(pasos)} pasos, "
                      f"{nombres}. Resultaron correctos {ok} de {len(pasos)}, con {len(ac['errores'])} errores de la interfaz"
                      + (" y sin cierres inesperados." if ok == len(pasos) and not ac["errores"] else "."))
    preps = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(REG.glob("preparacion_*.json"))]
    detectadas = [p for p in preps if str((p.get("rutas") or {}).get("origen", "")).startswith("detectada")]
    if ac is not None and detectadas:
        r = detectadas[0]["rutas"]
        partes.append(f"Esa prueba se hizo sobre una copia del ejecutable cuyo `juego_ac.json` apuntaba a una carpeta "
                      f"inexistente, `{r['ruta_ac_configurada']}`, para reproducir la instalación en otro equipo. En {len(detectadas)} de las "
                      f"{len(preps)} preparaciones registradas el programa detectó el juego en las bibliotecas de Steam "
                      f"y lo abrió desde `{r['ruta_ac']}`.")
    destino = DIR / "fuentes" / "fragmentos" / "pruebas_interfaz.md"
    destino.write_text("\n\n".join(partes) + "\n", encoding="utf-8")
    print(destino.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
