# 📋 Estado de Datasets y Tareas Pendientes

**Actualizado:** 2026-04-17 21:50  
**Proyecto:** Modelo XGBoost - Densidad de Krill Antártico
**Repositorio GitHub:** https://github.com/iadiegomunoz-dot/antarctic-krill-data ✅ CREADO

---

## 🎯 RESUMEN EJECUTIVO - Estado Actual

| Estado | Cantidad | Fuentes | Acción Prioritaria |
|--------|----------|---------|-------------------|
| ✅ **Listas** | 6/10 | KRILLBASE, SAM, ENSO, Sea Ice, Fotoperiodo, CMEMS | Usar para modelo base |
| 🔄 **En progreso** | 1/10 | NASA Giovanni (~22%) | **Completar descarga** - Crítico para modelo |
| ❌ **Pendientes** | 3/10 | CCAMLR, CMIP6, Biomasa Acústica | Opcionales/Validación |

**Progreso general: 60%** (6/10 fuentes completas)

**Próxima prioridad:** Completar NASA Giovanni (faltan ~211 archivos CHL y ~253 SST)

---

## 🎯 CHECKLIST DE 10 FUENTES - MARCA CON [x] CUANDO VERIFIQUES

**Instrucciones:** Cambia `[ ]` por `[x]` para marcar cada fuente. Deja `[-]` si está faltante.

### ✅ LISTAS (6/10)
- [x] **1. KRILLBASE** - Variable objetivo (4.3 MB, 14,736 registros, 1926-2016)
- [x] **2. SAM Index** - Southern Annular Mode (316 registros mensuales, 2000-2026)
- [x] **3. ENSO MEI v2** - Índice del Niño (315 registros mensuales, 2000-2026)
- [x] **4. Sea Ice Extent (NSIDC)** - Hielo marino (1.7 MB, 15,684 registros diarios, 1978-2025)
- [x] **5. Fotoperiodo Antártico** - Horas de luz (57 KB, 1,104 registros mensuales, 2001-2024)
- [x] **7. CMEMS** - MLD + SST oceánica (2.1 GB, 300 meses en grilla 0.083°, 2000-2024)

### 🔄 EN PROGRESO (1/10)
- [~] **6. NASA Giovanni** - ⚠️ INCOMPLETO (~22%)
  - CHL: 59/270 archivos descargados (867 MB de ~4 GB)
  - SST: 16/269 archivos descargados
  - Origen: AQUA_MODIS 9km, 2002-2024

### ❌ PENDIENTES (3/10)
- [ ] **8. CCAMLR (CPUE)** - Solo instrucciones. Requiere registro en ccamlr.org (1-2 días)
- [ ] **9. CMIP6** - Solo instrucciones. Proyecciones SSP2-4.5 / SSP5-8.5 (2025-2050)
- [ ] **10. Biomasa Acústica** - Solo scripts ERDDAP. Sin datos descargados aún

---

**Leyenda:** `[x]` = Lista | `[-]` = Faltante | `[ ]` = Sin verificar

**Resumen automático:** Cuando marques todas, copia esta sección y envíala al agente con tu evaluación.

---

## ✅ DATASETS COMPLETOS (Listos para Modelo)

### 1. KRILLBASE - Variable Objetivo

**Archivo:** `krillbase/krillbase_data.csv`  
**Registros:** 14,736 filas | **Tamaño:** 4.3 MB | **Columnas:** 29

**Estructura Detallada:**
| Columna | Tipo | Descripción | Variable Y |
|---------|------|-------------|------------|
| STATION | string | ID único de estación | - |
| LATITUDE | float | Latitud (-90 a -45) | Predictor |
| LONGITUDE | float | Longitud (-180 a 180) | Predictor |
| SEASON | int | Temporada (año de verano austral) | - |
| DATE | date | Fecha del muestreo | - |
| **STANDARDISED_KRILL_UNDER_1M2** | float | **Krill estandarizado por m²** | ✅ **Y** |
| CLIMATOLOGICAL_TEMPERATURE | float | Temp. SST climatológica (°C) | Predictor |
| WATER_DEPTH_MEAN_WITHIN_10KM | float | Profundidad media 10km (m) | Predictor |
| N_OR_S_POLAR_FRONT | categoría | Norte/Sur del Frente Polar | Predictor |
| NET_TYPE | string | Tipo de red usada | Control |
| BOTTOM_SAMPLING_DEPTH_M | float | Profundidad máxima muestreo | Control |

**Período:** 1926-2016 (temporadas de verano austral: Oct-Mar)  
**Respaldo:** Atkinson et al. 2004, 2008 (CCAMLR)  
**Estado:** ✅ LISTO - Variable objetivo cargada

---

### 2. SAM Index (Southern Annular Mode)

**Archivo:** `sam_index/sam_index_procesado.csv`  
**Registros:** 316 filas | **Columnas:** 5

**Estructura:**
```
year, month, SAM_index, SAM_9m_rolling, SAM_12m_rolling
```

| Variable | Descripción | Rango Típico |
|----------|-------------|--------------|
| SAM_index | Índice mensual SAM | -3 a +3 |
| SAM_9m_rolling | Promedio 9 meses | Suavizado |
| SAM_12m_rolling | Promedio 12 meses | Tendencia larga |

**Período:** Enero 2000 - Marzo 2026  
**Fuente:** NOAA CPC  
**Estado:** ✅ LISTO - Predictor principal según Ryabov et al. 2023

---

### 3. ENSO MEI v2

**Archivo:** `enso_mei/mei_enso_procesado.csv`  
**Registros:** 315 filas | **Columnas:** 4

**Estructura:**
```
year, month, MEI_v2, MEI_3m_rolling
```

| Valor MEI | Interpretación |
|-----------|---------------|
| > +0.5 | El Niño (cálido) |
| < -0.5 | La Niña (frío) |
| -0.5 a +0.5 | Neutral |

**Período:** Enero 2000 - Febrero 2026  
**Fuente:** NOAA PSL  
**Estado:** ✅ LISTO - Variabilidad interanual del Pacífico

---

### 4. Sea Ice Extent (NSIDC)

**Archivo:** `sea_ice_nsidc/S_seaice_extent_daily_v4.0.csv`  
**Registros:** 15,684 filas | **Columnas:** 6

**Estructura:**
| Columna | Descripción | Unidad |
|---------|-------------|--------|
| Year | Año | - |
| Month | Mes | - |
| Day | Día | - |
| Extent | Extensión de hielo | 10^6 km² |
| Missing | Área sin datos | 10^6 km² |
| Source Data | Archivo fuente | - |

**Período:** 26 Oct 1978 - 2025 (diario)  
**Fuente:** NSIDC (NASA/NOAA)  
**Estado:** ✅ LISTO - Predictor principal de hábitat krill

---

### 5. Fotoperiodo Antártico

**Archivo:** `fotoperiodo/fotoperiodo_antartico.csv`  
**Registros:** 1,104 filas | **Columnas:** 7

**Estructura:**
```
punto, lat, lon, year, month, daylight_hours, photoperiod_delta
```

**Ubicaciones:**
| Punto | Lat | Lon | Tipo |
|-------|-----|-----|------|
| Antártida_Norte | -55.0 | -45.0 | Periférico |
| Antártida_Centro | -65.0 | -60.0 | Central |
| Mar_Ross | -72.0 | 175.0 | Mar específico |
| Mar_Weddell | -70.0 | -40.0 | Mar específico |

**Período:** 2001-2024 (mensual)  
**Cálculo:** Biblioteca `astral` (posición solar)  
**Innovación:** Primera vez en modelo de krill  
**Estado:** ✅ LISTO - Variable novedosa lista

---

### 6. CMEMS (Copernicus Marine) - MLD + SST Oceánica

**Archivos:** 
- `cmems/mld_antartico.nc` - 1,041 MB (Mixed Layer Depth)
- `cmems/sst_oceanico_antartico_(1).nc` - 1,041 MB (Sea Surface Temperature)

**Estructura (NetCDF):**
| Variable | Descripción | Dimensiones |
|----------|-------------|-------------|
| `mlotst` | Mixed Layer Depth | time: 300, lat: 421, lon: 4320 |
| `thetao` | SST (capa superficial) | time: 300, depth: 1, lat: 421, lon: 4320 |

**Período:** 2000-01-01 a 2024-12-01 (300 meses)  
**Resolución:** 0.083° (~9 km)  
**Región:** -80° a -45° latitud (Antártida)  
**Fuente:** Copernicus Marine Service (GLOBAL_MULTIYEAR_PHY_001_030)  
**Estado:** ✅ **LISTO** - Ambos datasets descargados y verificados

---

## ⚠️ TAREAS PENDIENTES (Acción Requerida)

### 🔴 PRIORIDAD ALTA - Para Completar Modelo Base

---

#### TAREA 1: NASA Giovanni (Clorofila-a + SST)

**Estado Actual:** 🔄 INCOMPLETO - Descargas detenidas  
**Archivos descargados:**
- CHL: 59/270 archivos NetCDF mensuales (9km) - **867 MB de ~4 GB**
- SST: 16/269 archivos NetCDF mensuales (9km) - **16 archivos**
- Ubicación: `nasa_giovanni/chl/` (59 items) y `nasa_giovanni/sst/` (16 items)

**Faltan descargar:**
- CHL: ~211 archivos (~3.1 GB)
- SST: ~253 archivos

**Scripts creados:**
- `reanudar_descarga_nasa.py` - Reanudar descarga CHL
- `descargar_nasa_final.py` - Descarga final alternativa
- `descargar_giovanni_directo.py` - Método directo vía earthaccess

**Siguiente paso:** Ejecutar `reanudar_descarga_nasa.py` o descargar manual desde https://giovanni.gsfc.nasa.gov/

---

#### TAREA 2: CMEMS (Mixed Layer Depth + SST Oceánica)

**Estado Actual:** ✅ **COMPLETO** - Ambos datasets descargados y verificados  
**Archivos existentes:**
- ✅ `cmems/mld_antartico.nc` - 1,041 MB (Mixed Layer Depth - `mlotst`)
- ✅ `cmems/sst_oceanico_antartico_(1).nc` - 1,041 MB (SST - `thetao`, capa superficial 0.5m)

**Verificación:**
- Dimensiones: `time: 300`, `latitude: 421`, `longitude: 4320`
- Período: 2000-01-01 a 2024-12-01 (300 meses)
- Región: -80° a -45° latitud (Antártida completa)
- Resolución: 0.083° (~9 km)

**Registro:** ✅ iadiegomunoz@gmail.com (Copernicus Marine)

**Instrucciones originales:** Ver `cmems_instrucciones/`

---

### 🟡 PRIORIDAD MEDIA - Validación y Proyecciones

---

#### TAREA 3: CCAMLR (Datos de Pesca - CPUE)

**Estado Actual:** ⏳ Requiere aprobación de registro  
**Propósito:** Validación independiente del modelo con datos pesqueros reales

**QUÉ DEBES HACER:**

1. **Registrarse:** https://www.ccamlr.org/en/user/register
   - Completar formulario con afiliación institucional
   - Esperar aprobación: **1-2 días hábiles**

2. **Una vez aprobado:**
   - Ir a: Data > Statistical Data > Krill catches
   - Descargar: `CPUE by year and area`
   - Formato: CSV
   - Período: 1990-2024
   - Guardar en: `ccamlr_instrucciones/` (o crear carpeta `ccamlr/`)

**Variables a usar:**
- CPUE: Captura por Unidad de Esfuerzo (toneladas/hora de arrastre)
- AREA: Subzonas CCAMLR (48.1, 48.2, 48.3, 58.4, etc.)
- YEAR, MONTH

**Tiempo estimado:** 2-3 días (espera de aprobación)  
**Registro requerido:** ✅ Sí (con aprobación humana)

---

### 🟢 PRIORIDAD BAJA - Proyecciones Futuras

---

#### TAREA 4: CMIP6 (Proyecciones Climáticas 2050)

**Estado Actual:** ⏳ Solo instrucciones  
**Propósito:** Proyectar distribución de krill bajo escenarios SSP2/SSP5

**Escenarios a descargar:**
| Escenario | Nombre | Descripción |
|-----------|--------|-------------|
| SSP2-4.5 | "Middle of the Road" | Moderado, políticas intermedias |
| SSP5-8.5 | "Fossil-fueled Development" | Pesimista, alto CO2 |

**Variables:**
- `tos`: Sea Surface Temperature (SST futuro)
- `siconc`: Sea Ice Concentration

**Modelo recomendado:** `IPSL-CM6A-LR` (mejor resolución Antártica)

**QUÉ DEBES HACER:**

1. **Registrarse:** https://esgf-node.llnl.gov/user/add/

2. **Buscar datos:**
   - URL: https://esgf-node.llnl.gov/search/cmip6/
   - Filtros:
     - Project: CMIP6
     - Activity: ScenarioMIP
     - Experiment: ssp245 Y ssp585
     - Variable: tos, siconc
     - Frequency: mon
     - Source ID: IPSL-CM6A-LR
   - Descargar archivos `.nc`

3. **Guardar en:**
   - `cmip6/ssp245/`
   - `cmip6/ssp585/`

**Tiempo estimado:** 30 min setup + descarga (archivos grandes)  
**Registro requerido:** ✅ Sí (automático)
**Nota:** Esto es para **fase 2** del proyecto (proyecciones). El modelo base funciona sin estos datos.

---

## 📊 MATRIZ DE VARIABLES POR DATASET

### 1. KRILLBASE - Variable Objetivo ✅
| Variable | Descripción | Tipo | Uso en Modelo |
|----------|-------------|------|---------------|
| **STANDARDISED_KRILL_UNDER_1M2** | **Densidad de krill (# ind/m²)** | **float** | **🎯 VARIABLE Y** |
| LATITUDE | Latitud del muestreo (-90 a -45°) | float | Predictor espacial |
| LONGITUDE | Longitud del muestreo (-180 a 180°) | float | Predictor espacial |
| SEASON | Temporada de verano austral (año) | int | Control temporal |
| DATE | Fecha del muestreo (Oct-Mar) | date | Control temporal |
| CLIMATOLOGICAL_TEMPERATURE | Temperatura SST climatológica (°C) | float | Predictor físico |
| WATER_DEPTH_MEAN_WITHIN_10KM | Profundidad media 10km alrededor (m) | float | Predictor hábitat |
| N_OR_S_POLAR_FRONT | Posición relativa al Frente Polar | categoría | Predictor oceánico |
| NET_TYPE | Tipo de red usada | string | Control método |
| BOTTOM_SAMPLING_DEPTH_M | Profundidad máxima del muestreo | float | Control método |

**Total:** 29 columnas | 14,736 registros | 1926-2016

---

### 2. SAM Index - Southern Annular Mode ✅
| Variable | Descripción | Unidad | Uso |
|----------|-------------|--------|-----|
| **SAM_index** | Índice mensual SAM | adimensional | **Predictor principal** |
| SAM_9m_rolling | Promedio móvil 9 meses | adimensional | Tendencia corto plazo |
| SAM_12m_rolling | Promedio móvil 12 meses | adimensional | Tendencia largo plazo |
| year | Año | - | Temporal |
| month | Mes (1-12) | - | Temporal |

**Período:** Enero 2000 - Marzo 2026 (316 meses)  
**Fuente:** NOAA CPC  
**Relevancia:** Principal driver de variabilidad del krill según Ryabov et al. 2023

---

### 3. ENSO MEI v2 - El Niño Southern Oscillation ✅
| Variable | Descripción | Unidad | Uso |
|----------|-------------|--------|-----|
| **MEI_v2** | Índice multivariado ENSO | adimensional | **Predictor climático** |
| MEI_3m_rolling | Promedio móvil 3 meses | adimensional | Suavizado |
| year | Año | - | Temporal |
| month | Mes (1-12) | - | Temporal |

**Interpretación MEI:**
- > +0.5: El Niño (cálido) → Impacto en productividad Antártica
- < -0.5: La Niña (frío) → Mayores afloramientos, más productividad
- -0.5 a +0.5: Neutral

**Período:** Enero 2000 - Febrero 2026 (315 meses)  
**Fuente:** NOAA PSL

---

### 4. Sea Ice Extent (NSIDC) ✅
| Variable | Descripción | Unidad | Uso |
|----------|-------------|--------|-----|
| **Extent** | **Extensión de hielo marino** | **10⁶ km²** | **🔑 Predictor principal** |
| Area | Área cubierta por hielo | 10⁶ km² | Predictor secundario |
| Missing | Área sin datos | 10⁶ km² | Control calidad |
| Year | Año | - | Temporal |
| Month | Mes | - | Temporal |
| Day | Día | - | Temporal |

**Período:** 26 Oct 1978 - 2025 (15,684 días)  
**Fuente:** NSIDC (NASA/NOAA)  
**Relevancia:** El hielo marino modifica hábitat, alimentación y reproducción del krill

---

### 5. Fotoperiodo Antártico ✅
| Variable | Descripción | Unidad | Uso |
|----------|-------------|--------|-----|
| **daylight_hours** | **Horas de luz del día** | **horas** | **🌟 Variable innovadora** |
| photoperiod_delta | Cambio mensual en fotoperiodo | horas/mes | Señal de cambio estacional |
| punto | Ubicación (Antártida_Norte, Centro, etc.) | string | Estratificación espacial |
| lat | Latitud del punto | °S | Predictor espacial |
| lon | Longitud del punto | °E/°W | Predictor espacial |
| year | Año | - | Temporal |
| month | Mes | - | Temporal |

**Ubicaciones calculadas:**
- Antártida_Norte: -55.0°, -45.0° (Periférico)
- Antártida_Centro: -65.0°, -60.0° (Central)
- Mar_Ross: -72.0°, 175.0° (Mar específico)
- Mar_Weddell: -70.0°, -40.0° (Mar específico)

**Período:** 2001-2024 (mensual, 4 puntos = 1,104 registros)  
**Cálculo:** Biblioteca `astral` (posición solar)  
**Innovación:** Primera vez en modelo de krill - afecta ciclos biológicos

---

### 6. CMEMS - Copernicus Marine Service ✅
| Variable | Descripción | Unidad | Tipo de dato |
|----------|-------------|--------|--------------|
| **mlotst** | **Profundidad Capa de Mezcla** | **m** | **Predictor oceánico 3D** |
| **thetao** | **Temperatura Superficial del Mar** | **°C** | **Predictor térmico 3D** |
| depth | Profundidad de medición | m | Coordenada (0.5m para SST) |
| latitude | Latitud de la grilla | °S | Coordenada espacial |
| longitude | Longitud de la grilla | °E | Coordenada espacial |
| time | Tiempo (mes) | datetime | Coordenada temporal |

**Especificaciones técnicas:**
- **Resolución espacial:** 0.083° (~9 km)
- **Dimensiones:** 421 latitudes × 4320 longitudes × 300 meses
- **Región:** -80° a -45° latitud (Antártida completa)
- **Período:** 2000-01-01 a 2024-12-01 (300 meses)
- **Producto:** GLOBAL_MULTIYEAR_PHY_001_030 (Reanálisis GLORYS12)

**Relevancia:**
- **MLD:** Determina disponibilidad de nutrientes para fitoplancton (alimento krill)
- **SST:** Regula metabolismo, distribución y supervivencia del krill

---

### 7. NASA Giovanni - Clorofila-a + SST Satelital 🔄 22%
| Variable | Descripción | Unidad | Tipo | Uso |
|----------|-------------|--------|------|-----|
| **chlor_a** | **Concentración Clorofila-a** | **mg/m³** | Satelital MODIS | **🔑 Predictor alimentación** |
| **sst** | **Sea Surface Temperature** | **°C** | Satelital MODIS | **� Predictor térmico** |
| fecha | Fecha de medición | - | - | Temporal |

**Especificaciones:**
- **Satélite:** AQUA MODIS
- **Resolución:** 9 km
- **Período:** 2002-2024 (~270 meses)
- **Cobertura:** Antártida (-80° a -45°)

**Estado descarga:**
- CHL: 59/270 archivos descargados (867 MB de ~4 GB)
- SST: 16/269 archivos descargados
- **Faltan:** ~211 CHL + ~253 SST archivos

**Relevancia:** Clorofila-a = proxy de fitoplancton = alimento del krill

---

### 8. CCAMLR - CPUE (Catch Per Unit Effort) ⏳
| Variable | Descripción | Unidad | Uso |
|----------|-------------|--------|-----|
| **CPUE** | **Captura por Unidad de Esfuerzo** | **ton/hora** | **Validación modelo** |
| AREA | Subzona CCAMLR (48.1, 48.2, 48.3, 58.4...) | código | Estratificación espacial |
| YEAR | Año de pesca | - | Temporal |
| MONTH | Mes de pesca | - | Temporal |
| VESSEL | ID del buque | string | Control |

**Estado:** Requiere registro en ccamlr.org (1-2 días aprobación)  
**Propósito:** Validación independiente con datos pesqueros reales  
**Nota:** No es predictor, es para validar predicciones del modelo

---

### 9. CMIP6 - Proyecciones Climáticas ⏳
| Variable | Descripción | Unidad | Escenario |
|----------|-------------|--------|-----------|
| **tos** | **SST proyectada futura** | **°C** | SSP2-4.5 / SSP5-8.5 |
| **siconc** | **Concentración hielo proyectada** | **%** | SSP2-4.5 / SSP5-8.5 |
| time | Tiempo futuro (2025-2100) | datetime | - |
| latitude | Latitud | °S | - |
| longitude | Longitud | °E | - |

**Escenarios:**
- **SSP2-4.5:** "Middle of the Road" - Mitigación moderada
- **SSP5-8.5:** "Fossil-fueled Development" - Sin mitigación (pesimista)

**Período:** 2025-2100 (proyecciones)  
**Modelo:** IPSL-CM6A-LR (mejor resolución Antártica)  
**Uso:** Proyectar distribución del krill bajo cambio climático

---

### 10. Biomasa Acústica (ERDDAP) ⏳
| Variable | Descripción | Unidad | Uso |
|----------|-------------|--------|-----|
| **acoustic_biomass** | **Biomasa estimada acústicamente** | **g/m²** | **Validación alternativa** |
| latitude | Latitud | °S | Espacial |
| longitude | Longitud | °E | Espacial |
| date | Fecha del crucero | date | Temporal |
| vessel | Buque oceanográfico | string | Metadata |

**Estado:** Scripts creados (`buscar_erddap*.py`, `descargar_erddap*.py`) pero sin datos descargados  
**Fuentes potenciales:** NOAA SWFSC, IFREMER, COPAD  
**Uso:** Validación adicional del modelo con métodos independientes

---

### 📈 RESUMEN DE VARIABLES POR TIPO

| Tipo de Variable | Variables | Fuentes | Rol |
|------------------|-----------|---------|-----|
| **Variable Objetivo (Y)** | STANDARDISED_KRILL_UNDER_1M2 | KRILLBASE | Predecir |
| **Predictores Climáticos** | SAM_index, MEI_v2 | SAM, ENSO | Forzantes |
| **Predictores Oceánicos** | mlotst, thetao, sst | CMEMS, NASA | Hábitat |
| **Predictores de Alimento** | chlor_a | NASA | Productividad |
| **Predictores de Hielo** | Extent | NSIDC | Hábitat |
| **Predictores Temporales** | daylight_hours | Fotoperiodo | Ciclos biológicos |
| **Controles Espaciales** | LATITUDE, LONGITUDE, AREA | Todas | Estratificación |
| **Variables de Validación** | CPUE, acoustic_biomass | CCAMLR, ERDDAP | Testing |
| **Proyecciones Futuras** | tos, siconc | CMIP6 | Escenarios |

**Total estimado:** 25+ variables predictoras | 1 variable objetivo | ~16,500 registros

---

## 🔄 FLUJO DE TRABAJO RECOMENDADO

```
HOY (Actualizado):
├── ✅ LISTOS (6/10): KRILLBASE, SAM, ENSO, Sea Ice, Fotoperiodo, CMEMS
├── � PRIORIDAD: NASA Giovanni → Completar descarga (~211 CHL + ~253 SST)
└── ⏳ PENDIENTES: CCAMLR, CMIP6, Biomasa Acústica

OPCIONES AHORA:
1. � Iniciar modelo base con 6 fuentes completas
2. � Completar NASA Giovanni primero (más datos = mejor modelo)
3. ⏳ Esperar CCAMLR para validación adicional

SIGUIENTE:
└── 📝 Unificar datasets → python 02_unificar_dataset.py
```

---

## ❓ SOLUCIÓN DE PROBLEMAS

### NASA Giovanni: "No hay datos para la región"
- Verificar que las coordenadas sean: -80 (S) a -45 (S)
- Asegurar fechas dentro del período del satélite (MODIS: 2002+)

### CMEMS: "Error de autenticación"
- Verificar que el login fue exitoso: `copernicusmarine login`
- Si falla, intentar descarga manual desde la web

### CCAMLR: No llega email de aprobación
- Revisar carpeta spam/junk
- Contactar: data@ccamlr.org con asunto "Data Access Request"

---

## 📞 RESUMEN DE ACCIONES INMEDIATAS

**Para ti (siguientes 30 minutos):**
1. 🔄 **Completar NASA Giovanni** - Reanudar con `reanudar_descarga_nasa.py`
   - Faltan ~211 CHL y ~253 SST archivos NetCDF
   - Alternativa: Descarga manual desde https://giovanni.gsfc.nasa.gov/

**Esperando (días):**
2. ⏳ Aprobación CCAMLR - 1-2 días hábiles
3. ⏳ Descarga CMIP6 (opcional para proyecciones)
4. ⏳ Biomasa Acústica ERDDAP (opcional)

**Listo para ejecutar (6/10 fuentes):**
- ✅ KRILLBASE, SAM, ENSO, Sea Ice, Fotoperiodo, **CMEMS**
- ✅ Scripts base: `descargar_datos_antarticos.py`, `reanudar_descarga_nasa.py`
- ✅ Documentación completa en `info.md`

**Siguiente script a desarrollar:**
- 📝 `02_unificar_dataset.py` - Combinar todas las fuentes en dataset ML
- Nota: Se puede iniciar con las 6 fuentes completas mientras se completa NASA Giovanni

---

## 📦 REPOSITORIO GITHUB - Estado de Sincronización

**Repositorio:** `iadiegomunoz-dot/antarctic-krill-data`  
**URL:** https://github.com/iadiegomunoz-dot/antarctic-krill-data  
**Estado:** ✅ **CREADO Y ACTIVO**

### Archivos subidos (CSV procesados):

| Archivo | Local | GitHub | Tamaño | Estado |
|---------|-------|--------|--------|--------|
| `sam_index/sam_index_procesado.csv` | ✅ | ✅ | 16.2 KB | ✓ Subido |
| `enso_mei/mei_enso_procesado.csv` | ✅ | ✅ | 10.2 KB | ✓ Subido |
| `fotoperiodo/fotoperiodo_antartico.csv` | ✅ | ✅ | 55.8 KB | ✓ Subido |
| `sea_ice_nsidc/S_seaice_extent_daily_v4.0.csv` | ✅ | ✅ | 1,744 KB | ✓ Subido |
| `krillbase/krillbase_column_descriptions.csv` | ✅ | ✅ | 8.8 KB | ✓ Subido |
| `krillbase/krillbase_data.csv` | ✅ | ✅ | 4.3 MB | ✓ Subido |

### Archivos grandes (NetCDF) - NO subidos a GitHub:

| Archivo | Local | Tamaño | Nota |
|---------|-------|--------|------|
| `cmems/mld_antartico.nc` | ✅ | 1,041 MB | Usar Git LFS o Release |
| `cmems/sst_oceanico_antartico_(1).nc` | ✅ | 1,041 MB | Usar Git LFS o Release |
| `nasa_giovanni/chl/*.nc` (59 archivos) | ✅ | 867 MB | Procesar a CSV primero |
| `nasa_giovanni/sst/*.nc` (16 archivos) | ✅ | ~200 MB | Procesar a CSV primero |

**Total datos locales:** ~2.8 GB  
**Total en GitHub:** ~2 MB (CSVs pequeños)  
**Scripts Python:** 15+ archivos por subir  
**Documentación:** README.md subido, info.md por subir

---

*Archivo generado por asistente. Actualizado: 2026-04-17 21:50*
