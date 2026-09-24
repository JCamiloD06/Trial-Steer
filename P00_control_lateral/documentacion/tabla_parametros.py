"""
Tabla de todos los parámetros de configuración de Trial Steer para el Manual técnico.

Código auxiliar nuevo, no modifica ningún script existente. Lee configs/base.json
y configs/juego_ac.json, toma el valor de cada parámetro del archivo y le asigna
la descripción y la unidad de DESCRIPCIONES. Si un parámetro del archivo no
tiene descripción, o una descripción no corresponde a ningún parámetro, el
script falla, para que ningún parámetro quede sin nombrar.

Escribe fuentes/fragmentos/parametros.md, que construir_documentos.py inserta.

Uso desde la raíz del repositorio.
    python P00_control_lateral/documentacion/tabla_parametros.py
"""
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
RAIZ_P00 = DIR.parent

DESCRIPCIONES = {
    "base.json": {
        "ts_s": ("s", "Periodo nominal del ciclo de control"),
        "trazada.csv": ("", "Archivo de la trazada de referencia, relativo a la raíz"),
        "trazada.suavizado_curvatura_m": ("m", "Ventana de la media móvil de la curvatura"),
        "regiones.radio_baja_m": ("m", "Radio por encima del cual un tramo es de curvatura baja"),
        "regiones.radio_alta_m": ("m", "Radio igual o menor al cual un tramo es de curvatura alta"),
        "vehiculo.modelo_esperado": ("", "Modelo de vehículo que la corrida exige en el simulador"),
        "vehiculo.desfase_heading_rad": ("rad", "Desfase entre el heading del simulador y la orientación de la carrocería"),
        "vehiculo.indices_delanteras": ("", "Posiciones de las llantas delanteras en los arreglos de contacto"),
        "vehiculo.indices_traseras": ("", "Posiciones de las llantas traseras en los arreglos de contacto"),
        "vehiculo.L_min_m": ("m", "Batalla mínima aceptada al medir con los contactos"),
        "vehiculo.L_max_m": ("m", "Batalla máxima aceptada al medir con los contactos"),
        "vehiculo.distancia_max_centro_m": ("m", "Distancia máxima entre el centro de los ejes y la posición del simulador"),
        "vehiculo.desalineacion_max_rad": ("rad", "Diferencia máxima entre la línea de ejes y la orientación"),
        "vehiculo.forzar_respaldo": ("", "Usa siempre el traslado de respaldo en lugar de los contactos"),
        "vehiculo.respaldo.L_m": ("m", "Batalla del traslado de respaldo"),
        "vehiculo.respaldo.fraccion_punto_desde_trasero": ("", "Fracción de la batalla entre el eje trasero y la posición del simulador"),
        "direccion.delta_max_rad": ("rad", "Ángulo de rueda máximo"),
        "direccion.tasa_max_rad_s": ("rad/s", "Tasa máxima de cambio del ángulo de rueda"),
        "direccion.rueda_rad_eje_completo": ("rad", "Ángulo de rueda con el eje de vJoy en su extremo"),
        "direccion.signo_vjoy": ("", "Signo entre el ángulo de rueda y el eje de vJoy"),
        "direccion.velocidad_minima_direccion_kmh": ("km/h", "Velocidad por debajo de la cual la dirección se retiene"),
        "direccion.velocidad_plena_direccion_kmh": ("km/h", "Velocidad desde la cual la dirección entra completa"),
        "perfil.ay_max_ms2": ("m/s²", "Aceleración lateral máxima del perfil base"),
        "perfil.ax_frenado_max_ms2": ("m/s²", "Deceleración máxima de frenado del perfil base"),
        "perfil.grip_usage_factor": ("", "Fracción usada de la aceleración lateral máxima"),
        "perfil.grip_usage_brake": ("", "Fracción usada de la deceleración de frenado"),
        "perfil.v_max_recta_ms": ("m/s", "Velocidad máxima en recta"),
        "perfil.suavizado_perfil_m": ("m", "Ventana de suavizado del perfil, cero lo desactiva"),
        "perfil.preview_m": ("m", "Distancia base de anticipación de la velocidad objetivo"),
        "perfil.preview_speed_gain": ("s", "Aumento de la anticipación por unidad de velocidad"),
        "perfil.factores.conservador": ("", "Factor del perfil conservador sobre el perfil base"),
        "perfil.factores.nominal": ("", "Factor del perfil nominal sobre el perfil base"),
        "perfil.factores.rapido": ("", "Factor del perfil rápido sobre el perfil base"),
        "longitudinal.kp": ("1/(km/h)", "Ganancia proporcional del PID de velocidad"),
        "longitudinal.ki": ("1/(km/h s)", "Ganancia integral del PID de velocidad"),
        "longitudinal.kd": ("s/(km/h)", "Ganancia derivativa del PID de velocidad"),
        "longitudinal.limite_integral": ("km/h s", "Límite de la integral del error de velocidad"),
        "longitudinal.pedal.throttle_rise_s": ("s", "Tiempo de subida completa del acelerador"),
        "longitudinal.pedal.throttle_fall_s": ("s", "Tiempo de bajada completa del acelerador"),
        "longitudinal.pedal.brake_rise_s": ("s", "Tiempo de subida completa del freno"),
        "longitudinal.pedal.brake_fall_s": ("s", "Tiempo de bajada completa del freno"),
        "controladores.pure_pursuit.L0_m": ("m", "Distancia de anticipación base de Pure Pursuit"),
        "controladores.pure_pursuit.kv_s": ("s", "Aumento de la anticipación de Pure Pursuit con la velocidad"),
        "controladores.stanley.k": ("", "Ganancia del término de error lateral de Stanley"),
        "controladores.stanley.epsilon_ms": ("m/s", "Término que evita la división por velocidad nula en Stanley"),
        "controladores.mpc_cinematico.N": ("pasos", "Horizonte de predicción del MPC"),
        "controladores.mpc_cinematico.Qy": ("", "Peso del error lateral en el costo del MPC"),
        "controladores.mpc_cinematico.Qpsi": ("", "Peso del error angular en el costo del MPC"),
        "controladores.mpc_cinematico.Rdelta": ("", "Peso de la diferencia con el ángulo de la curva"),
        "controladores.mpc_cinematico.Rddelta": ("", "Peso del cambio del ángulo entre pasos"),
        "controladores.mpc_cinematico.tiempo_max_s": ("s", "Tiempo máximo del solucionador OSQP por ciclo"),
        "abandono.velocidad_min_kmh": ("km/h", "Velocidad bajo la cual el vehículo se considera detenido"),
        "abandono.tiempo_quieto_s": ("s", "Tiempo detenido que provoca el abandono"),
        "abandono.ruedas_fuera_min": ("llantas", "Número de llantas fuera de pista que cuenta para el abandono"),
        "abandono.tiempo_ruedas_fuera_s": ("s", "Tiempo con llantas fuera que provoca el abandono"),
        "abandono.velocidad_arranque_kmh": ("km/h", "Velocidad desde la cual se vigila el abandono"),
        "vuelta.ventana_estabilizacion_s": ("s", "Ventana previa al cruce en la que se guarda el máximo error lateral"),
        "vuelta.tolerancia_velocidad_cruce_kmh": ("km/h", "Diferencia aceptada entre velocidad y objetivo en el primer cruce"),
        "vuelta.pos_cruce_alta": ("", "Posición normalizada desde la que se espera el cruce de meta"),
        "vuelta.pos_cruce_baja": ("", "Posición normalizada que confirma el cruce de meta"),
        "vuelta.tiempo_limite_s": ("s", "Tiempo máximo de la corrida completa"),
        "metricas.punto_error_lateral": ("", "Punto del vehículo para la métrica principal, cg es la posición del simulador"),
        "metricas.punto_robustez": ("", "Punto del vehículo para la métrica de robustez, tras es el eje trasero"),
        "criterio_mapa.factibilidad.max_pct_ciclos_sobre_periodo": ("%", "Porcentaje máximo de ciclos con cómputo sobre el periodo"),
        "criterio_mapa.factibilidad.max_vueltas_fallidas_por_celda": ("vueltas", "Vueltas fallidas por encima de las cuales la celda no es evaluable"),
        "criterio_mapa.decision_de_mejora.metrica": ("", "Métrica de la decisión de mejora del mapa"),
        "criterio_mapa.esfuerzo_reportado.metrica": ("", "Métrica del esfuerzo de dirección reportado"),
        "criterio_mapa.esfuerzo_reportado.banda_bajo_costo": ("", "Razón de esfuerzo hasta la cual la mejora es de bajo costo"),
        "criterio_mapa.esfuerzo_reportado.banda_actividad_superior": ("", "Razón de esfuerzo desde la cual la actividad es muy superior"),
        "salida.directorio_corridas": ("", "Carpeta de las corridas, relativa a la raíz"),
    },
    "juego_ac.json": {
        "ruta_ac": ("", "Carpeta de instalación de Assetto Corsa"),
        "steam_appid": ("", "Identificador de Steam que se escribe en steam_appid.txt"),
        "directorio_cfg_juego": ("", "Carpeta de configuración del juego que recibe la plantilla"),
        "plantilla": ("", "Carpeta de la plantilla de sesión"),
        "directorio_respaldos": ("", "Carpeta de los respaldos de la configuración del juego"),
        "directorio_preparaciones": ("", "Carpeta del registro de cada preparación"),
        "esperado.track": ("", "Pista que la preparación exige"),
        "esperado.carModel": ("", "Vehículo que la preparación exige"),
        "posicion_salida": ("", "Posición normalizada de la salida"),
        "tolerancia_posicion_salida": ("", "Tolerancia de la posición de salida"),
        "velocidad_max_salida_kmh": ("km/h", "Velocidad máxima para considerar el vehículo detenido en la salida"),
        "ventana.titulo": ("", "Título de la ventana del juego"),
        "ventana.tamano_referencia": ("píxeles", "Tamaño de la ventana en que se midieron los botones"),
        "ventana.botones.conducir": ("píxeles", "Posición del botón del volante en el menú"),
        "tiempo_max_carga_s": ("s", "Tiempo máximo de carga de la sesión"),
        "tiempo_max_cierre_s": ("s", "Tiempo máximo de cierre del juego"),
        "clic_conducir.espera_inicial_s": ("s", "Espera antes del primer clic en el volante del menú"),
        "clic_conducir.espera_s": ("s", "Espera entre clics"),
        "clic_conducir.maximo": ("clics", "Número máximo de clics automáticos"),
        "clic_conducir.espera_manual_s": ("s", "Espera máxima al clic manual del usuario"),
        "prueba_control.freno": ("", "Freno de prueba enviado por vJoy"),
        "prueba_control.tolerancia": ("", "Diferencia aceptada entre el freno enviado y el leído"),
        "prueba_control.tiempo_max_s": ("s", "Tiempo máximo de la prueba de control"),
        "id_vjoy": ("", "Número del dispositivo vJoy"),
    },
}


def hojas(d, pre=""):
    for k, v in d.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict):
            yield from hojas(v, pre + k + ".")
        else:
            yield pre + k, v


def formato(v):
    if isinstance(v, bool):
        return "sí" if v else "no"
    if isinstance(v, float):
        return f"{v:.6g}"
    if isinstance(v, list):
        return " ".join(str(x) for x in v)
    texto = str(v).replace("\\", "/")
    return f"`{texto}`" if ("/" in texto or ":" in texto) else texto


def main():
    partes = []
    faltan = []
    for archivo, desc in DESCRIPCIONES.items():
        datos = json.loads((RAIZ_P00 / "configs" / archivo).read_text(encoding="utf-8"))
        filas = list(hojas(datos))
        faltan += [f"{archivo} {k}" for k, _ in filas if k not in desc]
        sobran = set(desc) - {k for k, _ in filas}
        faltan += [f"{archivo} {k} sin parámetro" for k in sobran]
        clave = "parametros_base" if archivo == "base.json" else "parametros_juego"
        partes.append((archivo, clave, filas, desc))
    if faltan:
        print("Parámetros sin descripción o descripciones sobrantes")
        print("\n".join(faltan))
        sys.exit(1)
    texto = []
    for archivo, clave, filas, desc in partes:
        titulo = ("Parámetros de configs/base.json, comunes a todas las corridas." if archivo == "base.json" else
                  "Parámetros de configs/juego_ac.json, apertura y preparación del simulador.")
        texto.append(f": Tabla [[tab:{clave}]]. {titulo}\n")
        texto.append("| Parámetro | Valor | Unidad | Descripción |\n|------------|--------|----|------------|")
        for k, v in filas:
            unidad, d = desc[k]
            texto.append(f"| `{k}` | {formato(v)} | {unidad} | {d} |")
        texto.append("")
    destino = DIR / "fuentes" / "fragmentos" / "parametros.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(texto) + "\n", encoding="utf-8")
    print(f"{sum(len(p[2]) for p in partes)} parámetros descritos en {destino.name}")


if __name__ == "__main__":
    main()
