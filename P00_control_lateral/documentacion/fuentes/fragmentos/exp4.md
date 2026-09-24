La Tabla [[tab:exp4]] reúne las métricas calculadas por `metricas_vuelta.py` para las tres corridas y la Figura [[fig:exp4]] muestra el error lateral por región.

: Tabla [[tab:exp4]]. Métricas de la vuelta medida de las corridas de demostración en perfil conservador. Error cuadrático medio del error lateral en metros, tiempo de vuelta en segundos y valor eficaz de la tasa de dirección en radianes por segundo.

| Controlador | Vuelta | Región baja | Región media | Región alta | Tiempo de vuelta | Tasa de dirección |
|---|---|---|---|---|---|---|
| Pure Pursuit | 0.139 | 0.123 | 0.197 | 0.038 | 207.94 | 0.0146 |
| Stanley | 0.092 | 0.073 | 0.137 | 0.038 | 207.90 | 0.0257 |
| MPC cinemático | 0.055 | 0.034 | 0.076 | 0.068 | 207.98 | 0.0501 |

![Figura [[fig:exp4]]. Error cuadrático medio del error lateral por región de curvatura en las corridas de demostración, una vuelta por controlador. Generada por `documentacion/resultados_doc.py`.](figuras/fig_exp4_comparacion.png){width=13cm}
