# Trial Steer

Plataforma de escritorio para la experimentación con controladores laterales y longitudinales de vehículos sobre el simulador Assetto Corsa.

Versión 1.0.1, septiembre de 2026.

Trial Steer ejecuta Pure Pursuit, Stanley y un MPC con modelo bicicleta cinemático bajo las mismas condiciones. Los tres comparten la lectura del simulador, la trazada, el perfil de velocidad, el lazo longitudinal PID, la actuación por vJoy y el registro de corridas. Un lanzador gráfico arma y ejecuta las corridas, gestiona planes aleatorizados con semilla para sintonía, piloto y campaña, y evalúa las corridas guardadas. El paquete incluye además análisis por vuelta y por región de curvatura, y pruebas automáticas que no requieren el simulador.

Es el programa encargado de la ejecución de pruebas del proyecto integral Volante direct drive con Force Feedback, https://github.com/JCamiloD06/Volante-direct-drive-con-Force-Feedback.

## Autores

Francisco Javier Burgos Flórez, Juan Camilo Díaz López y Jesus Alberto Lastra Robles.
Programa de Ingeniería Mecatrónica, Universidad Nacional de Colombia, Sede La Paz.
Contacto, jdiazlop@unal.edu.co y jlastrar@unal.edu.co.

## Estructura

| Ruta | Contenido |
|---|---|
| `P00_control_lateral/abrir_lanzador.py` | Punto de entrada de la interfaz gráfica |
| `P00_control_lateral/ejecutar_corrida.py` | Una corrida con un controlador y un perfil, como proceso aparte |
| `P00_control_lateral/lanzador/` | Interfaz gráfica y gestión de planes |
| `P00_control_lateral/plataforma/` | Lectura de Assetto Corsa, trazada, perfil, lazo longitudinal, vJoy, vuelta, registro, procedencia y apertura del juego |
| `P00_control_lateral/controladores/` | Pure Pursuit, Stanley y MPC cinemático con interfaz común |
| `P00_control_lateral/analisis/` | Métricas por vuelta y región, mapa por velocidad y curvatura, repetibilidad y selección de sintonía |
| `P00_control_lateral/configs/` | Parámetros, rangos de sintonía y plantilla de sesión de Assetto Corsa |
| `P00_control_lateral/pruebas/` | Pruebas automáticas |
| `P00_control_lateral/documentacion/` | Descripción del software, manual técnico, manual de usuario y pruebas de la interfaz |
| `P00_control_lateral/empaquetado/` | Construcción del ejecutable para Windows |
| `Model Predictive Control/Python/monza_fast_lane.csv` | Trazada de referencia de Monza |
| `Model Predictive Control/Python/mpc_monza_Completo_barrido.py` | Script del proyecto del volante que la pestaña MPC completo ejecuta sin modificar |
| `scripts/` | Gráficas de una corrida, figuras y tablas |

La carpeta `Model Predictive Control/Python/` conserva el nombre y la ubicación del proyecto del volante porque el código ubica la trazada y el script del MPC completo por rutas relativas a la raíz. Cambiarla exige cambiar el código.

## Requisitos

Windows, Python 3, las dependencias de `P00_control_lateral/requirements.txt` y matplotlib para las gráficas. Assetto Corsa con la pista Monza y el Alfa Romeo Giulietta QV, y vJoy. Assetto Corsa, vJoy, Steam y las librerías de Python son de terceros y no forman parte de Trial Steer.

## Ejecutable para Windows

El ejecutable se publica en la sección Releases del repositorio como `Trial_Steer_v1.0.1_windows.zip`. Incluye Python y todas las librerías. Se descomprime en una carpeta con permiso de escritura y se abre `Trial_Steer.exe`. Requiere Assetto Corsa y vJoy instalados. El programa encuentra solo la instalación del juego en las bibliotecas de Steam y crea `steam_appid.txt` si falta. Solo con varias instalaciones hay que escribir la elegida en `ruta_ac` de `P00_control_lateral/configs/juego_ac.json`.

Para construirlo desde el código, con PyInstaller instalado.

```
python P00_control_lateral/empaquetado/construir_exe.py
```

## Uso desde el código fuente

Desde la raíz del repositorio.

```
pip install -r P00_control_lateral/requirements.txt
python P00_control_lateral/abrir_lanzador.py
```

Pruebas automáticas, 143 verificaciones en siete archivos que no requieren el simulador.

```
python P00_control_lateral/pruebas/prueba_humo.py
```

Los demás archivos de `P00_control_lateral/pruebas/` se ejecutan igual.

La instalación de Assetto Corsa se detecta sola cuando hay una sola en Steam. Las corridas se guardan en `data/raw/p00/corridas`, que no se versiona.

## Licencia

Ver `LICENSE`.
