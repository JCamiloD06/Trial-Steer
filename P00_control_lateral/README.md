# Trial Steer v1.0.1

Software científico de escritorio para ejecutar, registrar y analizar experimentos de control lateral y longitudinal de vehículos sobre el simulador Assetto Corsa.

Versión registrada Trial Steer v1.0.1, código fuente congelado el 24 de septiembre de 2026.

## Autores

Francisco Javier Burgos Flórez, Juan Camilo Díaz López y Jesus Alberto Lastra Robles.
Programa de Ingeniería Mecatrónica, Universidad Nacional de Colombia, Sede La Paz.
Contacto, jdiazlop@unal.edu.co y jlastrar@unal.edu.co.
Repositorio, https://github.com/JCamiloD06/Trial-Steer

## Descripción

Trial Steer ejecuta tres controladores laterales, Pure Pursuit, Stanley y un control predictivo basado en modelo (MPC) con modelo bicicleta cinemático, bajo las mismas condiciones. Los tres comparten la lectura del estado del vehículo desde la memoria compartida del simulador, la trazada de referencia, el perfil de velocidad, el lazo longitudinal PID, la actuación por el dispositivo virtual vJoy y el registro de cada corrida. Lo único que cambia entre corridas es el controlador lateral y sus parámetros.

Es el programa encargado de la ejecución de pruebas del proyecto integral Volante direct drive con Force Feedback.

## Características principales

* Lanzador gráfico con corridas individuales, planes aleatorizados con semilla para sintonía y campaña, plan por bloques para el piloto y tandas encadenadas.
* Ciclo de control de 50 ms en un proceso separado de la ventana.
* Apertura automática del simulador con plantilla de sesión, respaldo de su configuración y detección de la instalación en las bibliotecas de Steam.
* Registro por corrida con telemetría de 70 columnas, perfil usado y manifiesto con configuración, versiones y huellas SHA256 del código.
* Verificación de la plataforma sobre una corrida guardada.
* Análisis por vuelta y por región de curvatura, mapa por velocidad y curvatura con pruebas estadísticas.
* Pruebas automáticas que no requieren el simulador.

## Controladores implementados

* Pure Pursuit, con distancia de anticipación que crece con la velocidad, en `controladores/pure_pursuit.py`.
* Stanley, sin anticipación de curvatura, con los errores del eje delantero, en `controladores/stanley.py`.
* MPC con modelo bicicleta cinemático lineal en los errores, resuelto con OSQP en cada ciclo, en `controladores/mpc_cinematico.py`.

Los tres heredan de `ControladorLateral` en `controladores/base.py`. El lazo longitudinal PID, el perfil de velocidad y los límites de dirección son comunes a los tres.

## Requisitos

Para el ejecutable de Windows no hace falta instalar Python. Se necesitan Windows de 64 bits, Steam con Assetto Corsa, la pista Monza y el Alfa Romeo Giulietta QV, y el controlador vJoy.

Para ejecutar desde el código fuente se necesita además Python 3.14 con las dependencias de `requirements.txt`, y matplotlib para las gráficas del MPC completo.

## Instalación y ejecución

Con el ejecutable, se descomprime `Trial_Steer_v1.0.1_windows.zip`, publicado en la sección Releases del repositorio, y se abre `Trial_Steer.exe`.

Desde el código fuente, en la raíz del repositorio.

```
python -m pip install -r P00_control_lateral/requirements.txt
python P00_control_lateral/abrir_lanzador.py
```

Pruebas automáticas, 144 verificaciones en siete archivos.

```
python P00_control_lateral/pruebas/prueba_humo.py
```

Construcción del ejecutable, con PyInstaller instalado.

```
python P00_control_lateral/empaquetado/construir_exe.py
```

El programa encuentra solo la instalación de Assetto Corsa cuando hay una sola en Steam. Con varias, se escribe la elegida en `ruta_ac` de `configs/juego_ac.json`.

## Convención de signos

Marco de la trazada, ángulos medidos con atan2 de z sobre x. ψ es la orientación de la carrocería, heading de Assetto Corsa más un desfase de 90 grados medido. δ positivo hace crecer ψ y corresponde a comando positivo de vJoy. e_y positivo significa vehículo a la izquierda de la trazada y eψ es ψ menos la orientación de la trazada.

## Estructura del código

| Ruta | Contenido |
|---|---|
| `abrir_lanzador.py` | Punto de entrada de la interfaz gráfica |
| `ejecutar_corrida.py` | Una corrida con un controlador y un perfil, como proceso aparte |
| `version.py` | Nombre, versión y fecha de congelamiento |
| `lanzador/` | Interfaz gráfica y gestión de planes |
| `plataforma/` | Lectura del simulador, trazada, perfil, lazo longitudinal, vJoy, vuelta, abandono, registro, procedencia y apertura del juego |
| `controladores/` | Pure Pursuit, Stanley y MPC cinemático con interfaz común |
| `analisis/` | Métricas, mapa por velocidad y curvatura, repetibilidad, selección de sintonía e identificación de plantas |
| `configs/` | Parámetros, rangos de sintonía y plantilla de sesión de Assetto Corsa |
| `pruebas/` | Pruebas automáticas |
| `empaquetado/` | Punto de entrada y construcción del ejecutable |
| `documentacion/` | Fuentes de los tres documentos, herramientas de capturas y de prueba de la interfaz, y sus informes |

## Dependencias

numpy 2.5.3, scipy 1.18.1, osqp 1.1.3 y pyvjoy 1.0.1, fijadas en `requirements.txt`, y matplotlib para las gráficas. El ejecutable las incluye. Son de terceros y conservan sus licencias, ver `TERCEROS.md`.

## Datos que genera

Cada corrida se guarda en `data/raw/p00/corridas/` con `telemetria.csv`, `perfil.csv` y `manifiesto.json`. Los respaldos de la configuración del juego quedan en `data/raw/p00/respaldos_cfg_ac` y el registro de cada preparación en `data/raw/p00/preparaciones_ac`.

## Nombre del directorio y referencias internas

El directorio `P00_control_lateral` conserva la denominación histórica usada durante el desarrollo, cuando el software se escribió para el estudio P00 de comparación de controladores laterales. Se mantiene en la versión 1.0.1 por compatibilidad, porque el código calcula sus rutas a partir de esa estructura. Por la misma razón las corridas se guardan en `data/raw/p00`.

Algunos comentarios del código y notas de los archivos de configuración citan decisiones de diseño con códigos como decisión 1.2 o I4, y fechas de verificación. Esos códigos remiten a los registros de desarrollo del proyecto de investigación, que no forman parte de este paquete. Se conservan porque documentan de dónde sale cada valor. El script previo `Model Predictive Control/Python/mpc_monza_Completo_barrido.py` se incluye sin modificaciones, porque `plataforma/procedencia.py` verifica su huella SHA256 y la pestaña MPC completo lo ejecuta tal cual. Sus comentarios internos citan los registros del proyecto anterior en el que se escribió.

## Procedencia y componentes de terceros

El código de este directorio es obra de los autores. Las piezas de lectura de memoria compartida, construcción de la trazada, perfil de velocidad, PID, conformador de pedal y salida a vJoy provienen de un script previo de los mismos autores, `Model Predictive Control/Python/mpc_monza_Completo_barrido.py`, y se integraron y reorganizaron en Trial Steer. `plataforma/procedencia.py` guarda la huella de ese script.

Assetto Corsa, Steam, vJoy, la trazada de Monza derivada de los archivos del juego y las librerías de Python son de terceros y no forman parte de la obra. El detalle, con licencias y atribuciones, está en `TERCEROS.md`.

## Limitaciones

Funciona solo en Windows con Assetto Corsa y vJoy. La configuración incluida cubre una pista, Monza, y un vehículo, el Alfa Romeo Giulietta QV. El modelo de predicción del MPC es cinemático, sin dinámica de llantas.

## Licencia

Ver `LICENSE`.
