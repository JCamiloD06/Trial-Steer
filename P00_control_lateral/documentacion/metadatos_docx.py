"""
Metadatos de los tres documentos de Trial Steer.

Código auxiliar. Deja como autores a los tres autores del software, pone título
y asunto, y vacía el campo de última modificación, que Word llena con el nombre
del usuario del equipo al guardar. Se ejecuta después de actualizar la tabla de
contenido con Word, porque Word vuelve a escribir ese campo.

Uso desde la raíz del repositorio.
    python P00_control_lateral/documentacion/metadatos_docx.py
"""
import sys
from pathlib import Path

from docx import Document

DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIR.parent))

import version  # noqa: E402

TITULOS = {"Descripcion_del_Software": "Descripción del software", "Manual_Tecnico": "Manual técnico",
           "Manual_de_Usuario": "Manual de usuario"}


def main():
    for prefijo, titulo in TITULOS.items():
        ruta = DIR / f"{prefijo}_Trial_Steer.docx"
        doc = Document(ruta)
        cp = doc.core_properties
        cp.author = ", ".join(version.AUTORES)
        cp.last_modified_by = ""
        cp.title = f"{version.NOMBRE} v{version.VERSION}, {titulo}"
        cp.subject = f"{version.NOMBRE} v{version.VERSION}"
        cp.comments = ""
        cp.keywords = ""
        cp.category = ""
        doc.save(ruta)
        d = Document(ruta).core_properties
        print(f"{ruta.name} autor {d.author}, última modificación '{d.last_modified_by}', título {d.title}")


if __name__ == "__main__":
    main()
