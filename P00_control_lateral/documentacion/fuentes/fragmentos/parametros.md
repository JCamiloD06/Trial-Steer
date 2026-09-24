: Tabla [[tab:parametros_base]]. Parámetros de configs/base.json, comunes a todas las corridas.

| Parámetro | Valor | Unidad | Descripción |
|------------|--------|----|------------|
| `ts_s` | 0.05 | s | Periodo nominal del ciclo de control |
| `trazada.csv` | `Model Predictive Control/Python/monza_fast_lane.csv` |  | Archivo de la trazada de referencia, relativo a la raíz |
| `trazada.suavizado_curvatura_m` | 15 | m | Ventana de la media móvil de la curvatura |
| `regiones.radio_baja_m` | 500 | m | Radio por encima del cual un tramo es de curvatura baja |
| `regiones.radio_alta_m` | 100 | m | Radio igual o menor al cual un tramo es de curvatura alta |
| `vehiculo.modelo_esperado` | alfa_romeo_giulietta_qv |  | Modelo de vehículo que la corrida exige en el simulador |
| `vehiculo.desfase_heading_rad` | 1.5708 | rad | Desfase entre el heading del simulador y la orientación de la carrocería |
| `vehiculo.indices_delanteras` | 0 1 |  | Posiciones de las llantas delanteras en los arreglos de contacto |
| `vehiculo.indices_traseras` | 2 3 |  | Posiciones de las llantas traseras en los arreglos de contacto |
| `vehiculo.L_min_m` | 2 | m | Batalla mínima aceptada al medir con los contactos |
| `vehiculo.L_max_m` | 3.5 | m | Batalla máxima aceptada al medir con los contactos |
| `vehiculo.distancia_max_centro_m` | 3 | m | Distancia máxima entre el centro de los ejes y la posición del simulador |
| `vehiculo.desalineacion_max_rad` | 0.174533 | rad | Diferencia máxima entre la línea de ejes y la orientación |
| `vehiculo.forzar_respaldo` | no |  | Usa siempre el traslado de respaldo en lugar de los contactos |
| `vehiculo.respaldo.L_m` | 2.7 | m | Batalla del traslado de respaldo |
| `vehiculo.respaldo.fraccion_punto_desde_trasero` | 0.43 |  | Fracción de la batalla entre el eje trasero y la posición del simulador |
| `direccion.delta_max_rad` | 0.403 | rad | Ángulo de rueda máximo |
| `direccion.tasa_max_rad_s` | 0.523599 | rad/s | Tasa máxima de cambio del ángulo de rueda |
| `direccion.rueda_rad_eje_completo` | 0.403 | rad | Ángulo de rueda con el eje de vJoy en su extremo |
| `direccion.signo_vjoy` | 1 |  | Signo entre el ángulo de rueda y el eje de vJoy |
| `direccion.velocidad_minima_direccion_kmh` | 5 | km/h | Velocidad por debajo de la cual la dirección se retiene |
| `direccion.velocidad_plena_direccion_kmh` | 30 | km/h | Velocidad desde la cual la dirección entra completa |
| `perfil.ay_max_ms2` | 6.5 | m/s² | Aceleración lateral máxima del perfil base |
| `perfil.ax_frenado_max_ms2` | 10.25 | m/s² | Deceleración máxima de frenado del perfil base |
| `perfil.grip_usage_factor` | 0.8 |  | Fracción usada de la aceleración lateral máxima |
| `perfil.grip_usage_brake` | 0.6 |  | Fracción usada de la deceleración de frenado |
| `perfil.v_max_recta_ms` | 50 | m/s | Velocidad máxima en recta |
| `perfil.suavizado_perfil_m` | 0 | m | Ventana de suavizado del perfil, cero lo desactiva |
| `perfil.preview_m` | 20 | m | Distancia base de anticipación de la velocidad objetivo |
| `perfil.preview_speed_gain` | 0.35 | s | Aumento de la anticipación por unidad de velocidad |
| `perfil.factores.conservador` | 0.8 |  | Factor del perfil conservador sobre el perfil base |
| `perfil.factores.nominal` | 0.9 |  | Factor del perfil nominal sobre el perfil base |
| `perfil.factores.rapido` | 1 |  | Factor del perfil rápido sobre el perfil base |
| `longitudinal.kp` | 0.0984882 | 1/(km/h) | Ganancia proporcional del PID de velocidad |
| `longitudinal.ki` | 0.0757601 | 1/(km/h s) | Ganancia integral del PID de velocidad |
| `longitudinal.kd` | 0 | s/(km/h) | Ganancia derivativa del PID de velocidad |
| `longitudinal.limite_integral` | 13.1996 | km/h s | Límite de la integral del error de velocidad |
| `longitudinal.pedal.throttle_rise_s` | 0.6 | s | Tiempo de subida completa del acelerador |
| `longitudinal.pedal.throttle_fall_s` | 0.35 | s | Tiempo de bajada completa del acelerador |
| `longitudinal.pedal.brake_rise_s` | 0.45 | s | Tiempo de subida completa del freno |
| `longitudinal.pedal.brake_fall_s` | 0.3 | s | Tiempo de bajada completa del freno |
| `controladores.pure_pursuit.L0_m` | 2.18282 | m | Distancia de anticipación base de Pure Pursuit |
| `controladores.pure_pursuit.kv_s` | 0.475382 | s | Aumento de la anticipación de Pure Pursuit con la velocidad |
| `controladores.stanley.k` | 2.03743 |  | Ganancia del término de error lateral de Stanley |
| `controladores.stanley.epsilon_ms` | 1 | m/s | Término que evita la división por velocidad nula en Stanley |
| `controladores.mpc_cinematico.N` | 20 | pasos | Horizonte de predicción del MPC |
| `controladores.mpc_cinematico.Qy` | 1 |  | Peso del error lateral en el costo del MPC |
| `controladores.mpc_cinematico.Qpsi` | 33.1676 |  | Peso del error angular en el costo del MPC |
| `controladores.mpc_cinematico.Rdelta` | 8.14727 |  | Peso de la diferencia con el ángulo de la curva |
| `controladores.mpc_cinematico.Rddelta` | 3.09206 |  | Peso del cambio del ángulo entre pasos |
| `controladores.mpc_cinematico.tiempo_max_s` | 0.04 | s | Tiempo máximo del solucionador OSQP por ciclo |
| `abandono.velocidad_min_kmh` | 5 | km/h | Velocidad bajo la cual el vehículo se considera detenido |
| `abandono.tiempo_quieto_s` | 8 | s | Tiempo detenido que provoca el abandono |
| `abandono.ruedas_fuera_min` | 3 | llantas | Número de llantas fuera de pista que cuenta para el abandono |
| `abandono.tiempo_ruedas_fuera_s` | 3 | s | Tiempo con llantas fuera que provoca el abandono |
| `abandono.velocidad_arranque_kmh` | 30 | km/h | Velocidad desde la cual se vigila el abandono |
| `vuelta.ventana_estabilizacion_s` | 2 | s | Ventana previa al cruce en la que se guarda el máximo error lateral |
| `vuelta.tolerancia_velocidad_cruce_kmh` | 10 | km/h | Diferencia aceptada entre velocidad y objetivo en el primer cruce |
| `vuelta.pos_cruce_alta` | 0.8 |  | Posición normalizada desde la que se espera el cruce de meta |
| `vuelta.pos_cruce_baja` | 0.2 |  | Posición normalizada que confirma el cruce de meta |
| `vuelta.tiempo_limite_s` | 420 | s | Tiempo máximo de la corrida completa |
| `metricas.punto_error_lateral` | cg |  | Punto del vehículo para la métrica principal, cg es la posición del simulador |
| `metricas.punto_robustez` | tras |  | Punto del vehículo para la métrica de robustez, tras es el eje trasero |
| `criterio_mapa.factibilidad.max_pct_ciclos_sobre_periodo` | 1 | % | Porcentaje máximo de ciclos con cómputo sobre el periodo |
| `criterio_mapa.factibilidad.max_vueltas_fallidas_por_celda` | 2 | vueltas | Vueltas fallidas por encima de las cuales la celda no es evaluable |
| `criterio_mapa.decision_de_mejora.metrica` | rmse_e_y |  | Métrica de la decisión de mejora del mapa |
| `criterio_mapa.esfuerzo_reportado.metrica` | razon_rms_tasa_mpc_sobre_geometrico |  | Métrica del esfuerzo de dirección reportado |
| `criterio_mapa.esfuerzo_reportado.banda_bajo_costo` | 1.5 |  | Razón de esfuerzo hasta la cual la mejora es de bajo costo |
| `criterio_mapa.esfuerzo_reportado.banda_actividad_superior` | 3 |  | Razón de esfuerzo desde la cual la actividad es muy superior |
| `salida.directorio_corridas` | `data/raw/p00/corridas` |  | Carpeta de las corridas, relativa a la raíz |

: Tabla [[tab:parametros_juego]]. Parámetros de configs/juego_ac.json, apertura y preparación del simulador.

| Parámetro | Valor | Unidad | Descripción |
|------------|--------|----|------------|
| `ruta_ac` | `C:/Program Files (x86)/Steam/steamapps/common/assettocorsa` |  | Carpeta de instalación de Assetto Corsa |
| `steam_appid` | 244210 |  | Identificador de Steam que se escribe en steam_appid.txt |
| `directorio_cfg_juego` | `~/Documents/Assetto Corsa/cfg` |  | Carpeta de configuración del juego que recibe la plantilla |
| `plantilla` | `configs/sesion_ac` |  | Carpeta de la plantilla de sesión |
| `directorio_respaldos` | `data/raw/p00/respaldos_cfg_ac` |  | Carpeta de los respaldos de la configuración del juego |
| `directorio_preparaciones` | `data/raw/p00/preparaciones_ac` |  | Carpeta del registro de cada preparación |
| `esperado.track` | monza |  | Pista que la preparación exige |
| `esperado.carModel` | alfa_romeo_giulietta_qv |  | Vehículo que la preparación exige |
| `posicion_salida` | 0.8564 |  | Posición normalizada de la salida |
| `tolerancia_posicion_salida` | 0.005 |  | Tolerancia de la posición de salida |
| `velocidad_max_salida_kmh` | 1 | km/h | Velocidad máxima para considerar el vehículo detenido en la salida |
| `ventana.titulo` | Assetto Corsa |  | Título de la ventana del juego |
| `ventana.tamano_referencia` | 1024 768 | píxeles | Tamaño de la ventana en que se midieron los botones |
| `ventana.botones.conducir` | 49 174 | píxeles | Posición del botón del volante en el menú |
| `tiempo_max_carga_s` | 90 | s | Tiempo máximo de carga de la sesión |
| `tiempo_max_cierre_s` | 30 | s | Tiempo máximo de cierre del juego |
| `clic_conducir.espera_inicial_s` | 2 | s | Espera antes del primer clic en el volante del menú |
| `clic_conducir.espera_s` | 3 | s | Espera entre clics |
| `clic_conducir.maximo` | 2 | clics | Número máximo de clics automáticos |
| `clic_conducir.espera_manual_s` | 120 | s | Espera máxima al clic manual del usuario |
| `prueba_control.freno` | 0.3 |  | Freno de prueba enviado por vJoy |
| `prueba_control.tolerancia` | 0.05 |  | Diferencia aceptada entre el freno enviado y el leído |
| `prueba_control.tiempo_max_s` | 4 | s | Tiempo máximo de la prueba de control |
| `id_vjoy` | 1 |  | Número del dispositivo vJoy |

