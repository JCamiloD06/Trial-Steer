"""
Procedencia de las piezas copiadas y huellas de archivos.

Las clases de lectura de Assetto Corsa, trazada, perfil de velocidad, PID,
conformador de pedal y salida a vJoy se tomaron de
mpc_monza_Completo_barrido.py, que la pestaña MPC completo ejecuta tal cual.
Este módulo compara la huella actual de ese script y de la trazada con la de
la versión distribuida, y el manifiesto de cada corrida deja constancia.

Las huellas de referencia se calculan con los finales de línea normalizados a
LF, para que no cambien según cómo Git haya extraído los archivos.
"""
import hashlib
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[2]
RAIZ_APP = Path(__file__).resolve().parents[1]

ORIGEN_BARRIDO = RAIZ_REPO / "Model Predictive Control" / "Python" / "mpc_monza_Completo_barrido.py"
SHA256_BARRIDO_REFERENCIA = "26275553a23895015dfdce2e729c304dfb10047d6e0f750e911c99640dae48fb"

TRAZADA_MONZA = RAIZ_REPO / "Model Predictive Control" / "Python" / "monza_fast_lane.csv"
SHA256_TRAZADA_REFERENCIA = "90c6e5a1955e320c0d00f49b490f1adc3abb0af3ac70144f7e7478f750670915"


def sha256(ruta):
    """Huella SHA256 de un archivo, o None si no se puede leer."""
    try:
        h = hashlib.sha256()
        with open(ruta, "rb") as f:
            for bloque in iter(lambda: f.read(65536), b""):
                h.update(bloque)
        return h.hexdigest()
    except OSError:
        return None


def sha256_texto(ruta):
    """Huella SHA256 de un archivo de texto con finales de línea LF, o None."""
    try:
        return hashlib.sha256(Path(ruta).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    except OSError:
        return None


def estado_origen():
    """Compara las huellas actuales de los archivos de origen con las de referencia."""
    actual_barrido = sha256_texto(ORIGEN_BARRIDO)
    actual_trazada = sha256_texto(TRAZADA_MONZA)
    return {
        "barrido_sha256_referencia": SHA256_BARRIDO_REFERENCIA,
        "barrido_sha256_actual": actual_barrido,
        "barrido_sin_cambios": actual_barrido == SHA256_BARRIDO_REFERENCIA,
        "trazada_sha256_referencia": SHA256_TRAZADA_REFERENCIA,
        "trazada_sha256_actual": actual_trazada,
        "trazada_sin_cambios": actual_trazada == SHA256_TRAZADA_REFERENCIA,
    }


def huellas_codigo():
    """Huella de cada archivo de código de Trial Steer, para el manifiesto."""
    huellas = {}
    for ruta in sorted(RAIZ_APP.rglob("*.py")):
        if "__pycache__" in ruta.parts:
            continue
        huellas[str(ruta.relative_to(RAIZ_APP)).replace("\\", "/")] = sha256(ruta)
    return huellas
