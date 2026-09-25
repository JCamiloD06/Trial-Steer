"""
Qué archivos forman la distribución de TrialSteer.

La usa el constructor del ejecutable, empaquetado/construir_exe.py, para
copiar junto al ejecutable el mismo código fuente del repositorio.

Entran el README, la licencia, la lista de componentes de terceros, las
dependencias, la carpeta TrialSteer y los tres archivos externos que el
programa usa. Quedan fuera los datos que el programa escribe al usarse, los
planes que genera, los cachés de Python y las salidas de construcción.
"""
from pathlib import Path

RAIZ_APP = Path(__file__).resolve().parents[1]
RAIZ_REPO = RAIZ_APP.parent

RAIZ_ARCHIVOS = ["README.md", "LICENSE", "TERCEROS.md", "requirements.txt"]
EXCLUIR_CARPETAS = {"__pycache__", "dist", "build"}
EXCLUIR_EN_CONFIGS = {"plan_campana.json", "plan_piloto.json", "plan_sintonia.json", "sintonia", "piloto"}
# La trazada la lee la plataforma, el script de barrido lo ejecuta la pestaña
# MPC completo y el de gráficas lo ejecuta el botón Generar gráficas.
EXTERNOS = ["Model Predictive Control/Python/monza_fast_lane.csv",
            "Model Predictive Control/Python/mpc_monza_Completo_barrido.py",
            "scripts/graficas_corrida.py"]


def incluir(ruta):
    ruta = Path(ruta)
    if not ruta.is_file() or ruta.suffix in (".pyc", ".pyo") or ruta.name.startswith("~$"):
        return False
    rel = ruta.relative_to(RAIZ_APP)
    if any(p in EXCLUIR_CARPETAS for p in rel.parts):
        return False
    if rel.parts[0] == "configs" and len(rel.parts) > 1 and rel.parts[1] in EXCLUIR_EN_CONFIGS:
        return False
    return True


def archivos():
    """Rutas absolutas de todos los archivos de la distribución, en orden."""
    return ([RAIZ_REPO / n for n in RAIZ_ARCHIVOS]
            + sorted(p for p in RAIZ_APP.rglob("*") if incluir(p))
            + [RAIZ_REPO / n for n in EXTERNOS])
