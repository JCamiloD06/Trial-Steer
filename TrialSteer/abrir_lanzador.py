"""
Abre la ventana de TrialSteer.

Uso desde la raíz del repositorio.
    python TrialSteer/abrir_lanzador.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lanzador.app import main  # noqa: E402

if __name__ == "__main__":
    main()
