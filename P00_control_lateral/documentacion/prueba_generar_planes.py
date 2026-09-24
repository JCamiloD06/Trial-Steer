"""
Prueba de la generación de planes y de la carga de corridas desde los planes.

Código auxiliar nuevo, no modifica ningún script existente. Solo se ejecuta
sobre una copia sin planes, por ejemplo la carpeta del ejecutable, nunca sobre
el repositorio, porque los planes del estudio no se sobrescriben. Si encuentra
un plan existente se detiene sin tocar nada.

Pulsa Generar plan en las pestañas de campaña, sintonía y piloto contestando
Sí y una semilla fija, y después Usar siguiente, Usar seleccionada y Repetir
seleccionada, que solo cargan la corrida en la pestaña Corrida.

Uso.
    Trial_Steer_consola.exe prueba_generar_planes.py --raiz <carpeta P00_control_lateral de la copia>
"""
import argparse
import sys
import traceback
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", required=True)
ap.add_argument("--salida", default="")
ARGS = ap.parse_args()
RAIZ_P00 = Path(ARGS.raiz).resolve()
sys.path.insert(0, str(RAIZ_P00))

from tkinter import messagebox, simpledialog  # noqa: E402

from lanzador import app as mod_app  # noqa: E402

REGISTRO = []
for nombre in ("showinfo", "showerror", "showwarning"):
    setattr(messagebox, nombre, lambda *a, n=nombre, **k: REGISTRO.append(f"{n}, {a[0] if a else ''}, {a[1][:120] if len(a) > 1 else ''}"))
messagebox.askyesno = lambda *a, **k: REGISTRO.append(f"askyesno Sí, {a[0]}") or True
simpledialog.askinteger = lambda *a, **k: REGISTRO.append(f"askinteger 12345, {a[0]}") or 12345


def main():
    planes = [RAIZ_P00 / "configs" / n for n in ("plan_campana.json", "plan_sintonia.json", "plan_piloto.json")]
    if any(p.exists() for p in planes):
        print("Hay planes en esta carpeta. La prueba solo corre sobre una copia sin planes.")
        sys.exit(2)
    errores = []
    v = mod_app.Lanzador()
    v.report_callback_exception = lambda e, val, tb: errores.append("".join(traceback.format_exception(e, val, tb)))
    v.update()
    pasos = [("Generar plan de campaña", v.generar_plan), ("Usar siguiente", v.usar_siguiente),
             ("Generar plan de sintonía", v.generar_plan_sintonia), ("Generar plan de piloto", v.generar_plan_piloto)]
    for nombre, funcion in pasos:
        antes = len(REGISTRO)
        try:
            funcion()
            v.update()
        except Exception:
            errores.append(traceback.format_exc())
        print(f"{nombre}, campos {v.var_fase.get()} {v.var_ctrl.get()} {v.var_perfil.get()} "
              f"sesión {v.var_sesion.get()} plan {v.var_id_plan.get()}")
        for r in REGISTRO[antes:]:
            print("   ", r)
    for arbol, funcion, nombre in ((v.tree_sint, v.usar_seleccionada_sintonia, "Usar seleccionada de sintonía"),
                                   (v.tree_pil, v.repetir_seleccionada_piloto, "Repetir seleccionada de piloto")):
        hijos = arbol.get_children()
        if hijos:
            arbol.selection_set(hijos[0])
        antes = len(REGISTRO)
        try:
            funcion()
            v.update()
        except Exception:
            errores.append(traceback.format_exc())
        print(f"{nombre}, filas {len(hijos)}, campos {v.var_fase.get()} {v.var_ctrl.get()} "
              f"{v.var_perfil.get()} plan {v.var_id_plan.get()} config {Path(v.var_config.get()).name}")
        for r in REGISTRO[antes:]:
            print("   ", r)
    print("Planes creados", [p.name for p in planes if p.exists()])
    if ARGS.salida:
        import json
        Path(ARGS.salida).write_text(json.dumps({"planes": [p.name for p in planes if p.exists()],
                                                 "errores": len(errores), "dialogos": REGISTRO},
                                                indent=2, ensure_ascii=False), encoding="utf-8")
    v.destroy()
    print(f"Errores {len(errores)}")
    for e in errores:
        print(e)
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
