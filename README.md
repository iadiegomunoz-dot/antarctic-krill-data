# Antarctic Krill Data

Datos antarticos para modelado de krill (*Euphausia superba*).

## Datasets

| Dataset | Estado | Registros | Periodo |
|---------|--------|-----------|---------|
| KrillBase | Completo | 14,736 | 1926-2016 |
| SAM Index | Completo | 316 | 2000-2026 |
| ENSO MEI | Completo | 315 | 2000-2026 |
| Sea Ice | Completo | 15,684 | 1979-2024 |
| Fotoperiodo | Completo | 1,104 | 2001-2024 |

## Estructura

```
data/
  ├── krillbase/          - Muestra de datos (primeras 1000 filas)
  ├── enso_mei/           - Indice ENSO MEI.v2
  ├── sam_index/          - Southern Annular Mode
  ├── sea_ice_nsidc/      - Muestra de datos de hielo
  └── fotoperiodo/        - Horas de luz calculadas
scripts/                  - Scripts de descarga
```

## Uso

Datos en formato CSV listos para analisis con pandas/R.
