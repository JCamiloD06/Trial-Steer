"""
Qué archivos forman la distribución de Trial Steer.

La misma regla la usan el constructor del ejecutable, empaquetado/construir_exe.py,
y el empaquetado del código fuente, documentacion/empaquetar_codigo.py, para que
el zip registrado y la carpeta del ejecutable contengan lo mismo.

Se incluyen el código, las configuraciones, las pruebas, la documentación en
texto y las herramientas de documentación y prueba de la interfaz. Se excluyen
los datos y resultados de estudios, los planes generados, los cachés de Python,
las salidas de construcción y los documentos e imágenes, que se entregan aparte.
"""
from pathlib import Path

RAIZ_P00 = Path(__file__).resolve().parents[1]
RAIZ_REPO = RAIZ_P00.parent

EXCLUIR_CARPETAS = {"__pycache__", "piloto_fase5", "resultados_campana", "sintonia_fase4", "sintonia_pid",
                    "dist", "build", "entrega", "revision_pdf", "figuras", "figuras_numeradas"}
EXCLUIR_EN_CONFIGS = {"plan_campana.json", "plan_piloto.json", "plan_sintonia.json", "sintonia", "piloto"}
EXTENSIONES_DOCUMENTACION = {".py", ".ps1", ".json", ".md"}
# En la raíz de documentacion/ solo entran estas herramientas. Cualquier otro archivo que aparezca ahí
# queda fuera hasta que se revise y se agregue a la lista.
HERRAMIENTAS_DOCUMENTACION = {
    "actualizar_con_word.ps1", "capturas_lanzador.py", "construir_documentos.py", "datos_portada.json",
    "empaquetar_codigo.py", "generar_figuras_doc.py", "metadatos_docx.py", "prueba_botones.py", "prueba_exe_ac.py",
    "prueba_generar_planes.py", "resultados_doc.py", "resumen_pruebas.py", "tabla_parametros.py"}
# Obra previa de los mismos autores que el software usa desde su ruta original. La trazada la lee la
# plataforma, el script de barrido lo ejecuta la pestaña MPC completo y su huella la compara procedencia.py,
# y el guion de gráficas lo ejecuta el botón Generar gráficas.
EXTRAS = [RAIZ_REPO / "Model Predictive Control" / "Python" / "monza_fast_lane.csv",
          RAIZ_REPO / "Model Predictive Control" / "Python" / "mpc_monza_Completo_barrido.py",
          RAIZ_REPO / "scripts" / "08_graficas_corrida.py"]


def incluir(ruta):
    ruta = Path(ruta)
    if not ruta.is_file() or ruta.suffix in (".pyc", ".pyo") or ruta.name.startswith("~$"):
        return False
    rel = ruta.relative_to(RAIZ_P00)
    if any(p in EXCLUIR_CARPETAS for p in rel.parts):
        return False
    if rel.parts[0] == "configs" and len(rel.parts) > 1 and rel.parts[1] in EXCLUIR_EN_CONFIGS:
        return False
    if rel.parts[0] == "documentacion":
        if ruta.suffix not in EXTENSIONES_DOCUMENTACION:
            return False
        if len(rel.parts) == 2 and rel.name not in HERRAMIENTAS_DOCUMENTACION:
            return False
    return True


def archivos():
    """Rutas absolutas de todos los archivos de la distribución, en orden."""
    return sorted(p for p in RAIZ_P00.rglob("*") if incluir(p)) + [p for p in EXTRAS if p.exists()]
