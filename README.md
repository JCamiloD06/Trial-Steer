# TrialSteer v1.0.1

Software de escritorio para ejecutar, registrar y evaluar corridas de controladores laterales y longitudinales de vehículos sobre el simulador Assetto Corsa.

TrialSteer ejecuta tres controladores laterales, Pure Pursuit, Stanley y un control predictivo basado en modelo (MPC) con modelo bicicleta cinemático, bajo las mismas condiciones. Los tres comparten la lectura del estado del vehículo desde la memoria compartida del simulador, la trazada de referencia, el perfil de velocidad, el lazo longitudinal PID, la actuación por el dispositivo virtual vJoy y el registro de cada corrida. Incluye además la ejecución del MPC completo de dirección y velocidad con sus gráficas.

## Autores

Francisco Javier Burgos Flórez, Juan Camilo Díaz López y Jesús Alberto Lastra Robles.
Programa de Ingeniería Mecatrónica, Universidad Nacional de Colombia, Sede La Paz.
Contacto, jdiazlop@unal.edu.co y jlastrar@unal.edu.co.

## Requisitos

* Windows 10 u 11 de 64 bits.
* Assetto Corsa instalado con Steam, con la pista Monza y el vehículo Alfa Romeo Giulietta QV.
* El controlador vJoy instalado, con el dispositivo 1 activo.
* Para ejecutar desde el código fuente, Python 3.14 con las dependencias de `requirements.txt`. El ejecutable ya las incluye.

## Instalación

Con el ejecutable, se descarga `TrialSteer_v1.0.1_windows.zip` de la sección Releases del repositorio, se descomprime en una carpeta con permiso de escritura y se abre `TrialSteer.exe`. `TrialSteer_consola.exe` lo usa el programa para las corridas y no se abre a mano.

Desde el código fuente, en la raíz del repositorio.

```
python -m pip install -r requirements.txt
python TrialSteer/abrir_lanzador.py
```

Para construir el ejecutable, con PyInstaller instalado.

```
python TrialSteer/empaquetado/construir_exe.py
```

El programa encuentra solo la instalación de Assetto Corsa cuando hay una sola en las bibliotecas de Steam, y crea `steam_appid.txt` en la carpeta del juego si falta. Con varias instalaciones se escribe la elegida en `ruta_ac` de `TrialSteer/configs/juego_ac.json`.

## Uso

La ventana tiene dos pestañas principales, Prueba de controladores y MPC completo.

### Una corrida

1. En la pestaña Corrida se eligen la fase, el controlador, el perfil de velocidad, la sesión y una etiqueta. La fase prueba sirve para corridas sueltas.
2. Se pulsa Iniciar corrida. El programa abre Assetto Corsa con la plantilla de sesión de `TrialSteer/configs/sesion_ac`, respalda antes la configuración del juego, pulsa el volante del menú y arranca la vuelta.
3. La salida del proceso aparece en Salida en vivo. La corrida termina sola al completar la vuelta medida, por abandono automático o al pulsar Detener y guardar, y en todos los casos guarda el registro.
4. Al terminar, el resumen aparece en Resumen de la última corrida.

Restaurar configuración del juego devuelve la carpeta de configuración de Assetto Corsa al estado previo a la plantilla.

### Planes de corridas

* Tanda de sintonía genera con semilla un plan de búsqueda aleatoria dentro de los rangos de `TrialSteer/configs/rangos_sintonia.json` y corre sus vueltas en tanda.
* Piloto genera un plan por bloques con los parámetros de `TrialSteer/configs/parametros_piloto.json`, primero el ajuste del perfil base, luego la repetibilidad y al final el bloque del tiempo límite.
* Plan de campaña genera una sola vez con semilla el orden aleatorio de controladores y perfiles por sesión. Usar siguiente carga la siguiente corrida pendiente y Correr la sesión corre en tanda las pendientes.

Los planes no se sobrescriben. Cada corrida del plan queda marcada como hecha o pendiente según las carpetas de corridas guardadas.

### Verificación de la plataforma

Se elige una corrida guardada, se pulsa Evaluar y la pestaña muestra los puntos de verificación de la plataforma, entre ellos el vehículo leído, la física ampliada, la batalla medida, el periodo de control, las saturaciones y la constante de la cadena de dirección.

### MPC completo

Iniciar MPC completo ejecuta `Model Predictive Control/Python/mpc_monza_Completo_barrido.py`. Activar MPC equivale a pulsar Enter cuando el vehículo está listo. Al terminar, Generar gráficas crea las cinco figuras de la corrida con `scripts/graficas_corrida.py`.

## Datos que genera

Cada corrida se guarda en `datos/corridas/<id>` con `telemetria.csv`, `perfil.csv` y `manifiesto.json`. El manifiesto registra la configuración usada, las versiones de las librerías y las huellas SHA256 del código. Los respaldos de la configuración del juego quedan en `datos/respaldos_cfg_ac`, el registro de cada preparación en `datos/preparaciones_ac` y el avance de las tandas en `datos/tandas`. Las corridas del MPC completo se guardan en `Model Predictive Control/Python/runs`.

## Convención de signos

Marco de la trazada, con ángulos medidos con atan2 de z sobre x. ψ es la orientación de la carrocería, heading de Assetto Corsa más un desfase de 90 grados medido. δ positivo hace crecer ψ y corresponde a comando positivo de vJoy. e_y positivo significa vehículo a la izquierda de la trazada y eψ es ψ menos la orientación de la trazada.

## Estructura del código

| Ruta | Contenido |
|---|---|
| `TrialSteer/abrir_lanzador.py` | Punto de entrada de la interfaz gráfica |
| `TrialSteer/ejecutar_corrida.py` | Una corrida con un controlador y un perfil, como proceso aparte |
| `TrialSteer/version.py` | Nombre, versión y fecha de congelamiento |
| `TrialSteer/lanzador/` | Interfaz gráfica, planes y lectura de corridas guardadas |
| `TrialSteer/plataforma/` | Lectura del simulador, trazada, perfil, lazo longitudinal, vJoy, vuelta, abandono, registro, procedencia y apertura del juego |
| `TrialSteer/controladores/` | Pure Pursuit, Stanley y MPC cinemático con interfaz común |
| `TrialSteer/configs/` | Parámetros, rangos de sintonía, parámetros del piloto y plantilla de sesión de Assetto Corsa |
| `TrialSteer/empaquetado/` | Punto de entrada y construcción del ejecutable |
| `Model Predictive Control/Python/` | Trazada de Monza y script del MPC completo |
| `scripts/graficas_corrida.py` | Gráficas de una corrida del MPC completo |

## Limitaciones

Funciona solo en Windows con Assetto Corsa y vJoy. La configuración incluida cubre una pista, Monza, y un vehículo, el Alfa Romeo Giulietta QV. El modelo de predicción del MPC lateral es cinemático, sin dinámica de llantas.

## Componentes de terceros

Assetto Corsa, Steam, vJoy, la trazada de Monza derivada de los archivos del juego y las librerías de Python son de terceros y no forman parte de la obra. El detalle, con licencias y atribuciones, está en `TERCEROS.md`.

## Licencia

Ver `LICENSE`.
