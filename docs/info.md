# Resumen de Bases de Datos - data_antartica

**Proyecto:** Modelo de Krill (Euphausia superba)  
**Generado:** 2026-04-10  
**Objetivo:** Dataset integrado para modelado predictivo de densidad de krill antártico usando XGBoost

---

## Estructura General

Este dataset contiene datos para modelar la distribución y densidad de krill en la Antártida, integrando múltiples fuentes oceanográficas y climáticas.

| Carpeta | Estado | Descripción |
|---------|--------|-------------|
| `krillbase/` | ✅ **14,736 registros** | Variable objetivo (Y) - datos de densidad de krill |
| `enso_mei/` | ✅ COMPLETA | Índice ENSO MEI v2 mensual |
| `sam_index/` | ✅ COMPLETA | Índice SAM mensual con rolling averages |
| `sea_ice_nsidc/` | ✅ COMPLETA | Extensión de hielo marino diaria |
| `fotoperiodo/` | ✅ COMPLETA | Horas de luz calculadas (4 ubicaciones) |
| `nasa_giovanni/` | 🤖 AUTO/MANUAL | Intento automático + instrucciones backup |
| `cmems/` | 🤖 AUTO/MANUAL | Requiere `pip install copernicusmarine` |
| `ccamlr_instrucciones/` | ⚠️ MANUAL | Requiere registro aprobado (1-2 días) |
| `cmip6_instrucciones/` | ⚠️ MANUAL | Proyecciones climáticas ESGF |

---

## Datasets Completos

### 1. ENSO MEI (enso_mei/)

**Archivos:**
- `mei_enso_procesado.csv` (315 registros)
- `mei_v2_raw.txt` (datos crudos NOAA)

**Estructura (CSV):**
```
year, month, MEI_v2, MEI_3m_rolling
```

**Descripción:**
- Índice Multivariado del Niño/Oscilación del Sur (MEI v2)
- Período: Enero 2000 - Febrero 2026
- Frecuencia: Mensual
- Valores positivos = El Niño, negativos = La Niña
- `MEI_3m_rolling`: Promedio móvil de 3 meses

**Fuente:** NOAA PSL (Physical Sciences Laboratory)  
**Uso:** Predictor de variabilidad interanual para modelo de krill

---

### 2. SAM Index (sam_index/)

**Archivos:**
- `sam_index_procesado.csv` (316 registros)
- `sam_noaa_raw.txt` (datos crudos NOAA)

**Estructura (CSV):**
```
year, month, SAM_index, SAM_9m_rolling, SAM_12m_rolling
```

**Descripción:**
- Southern Annular Mode (Modo Anular del Sur)
- Período: Enero 2000 - Marzo 2026
- Frecuencia: Mensual
- Mide la intensidad de los vientos del oeste circumpolares
- Incluye promedios móviles de 9 y 12 meses para análisis de tendencias

**Fuente:** NOAA  
**Uso:** Predictor principal según Ryabov et al. 2023

---

### 3. Fotoperiodo Antártico (fotoperiodo/)

**Archivo:** `fotoperiodo_antartico.csv` (1,153 registros)

**Estructura:**
```
punto, lat, lon, year, month, daylight_hours, photoperiod_delta
```

**Ubicaciones:**
| Punto | Latitud | Longitud | Descripción |
|-------|---------|----------|-------------|
| Antártida_Centro | -65.0 | -60.0 | Zona central antártica |
| Antártida_Norte | -55.0 | -45.0 | Zona norte antártica |
| Mar_Ross | -72.0 | 175.0 | Mar de Ross |

**Descripción:**
- Período: 2001-2024 (mensual)
- `daylight_hours`: Horas de luz diarias calculadas con biblioteca astral
- `photoperiod_delta`: Cambio mensual en horas de luz
- **INNOVACIÓN:** Variable no usada previamente en modelos de krill

**Uso:** Variable de fotoperiodo como predictor potencial

---

### 4. Sea Ice Extent (sea_ice_nsidc/)

**Archivo:** `S_seaice_extent_daily_v4.0.csv` (15,684 registros)

**Estructura:**
```
Year, Month, Day, Extent, Missing, Source Data
```

**Descripción:**
- Extensión diaria de hielo marino antártico
- Período: 26 Octubre 1978 - Presente (2025)
- Unidades: 10^6 km² (millones de kilómetros cuadrados)
- Frecuencia: Diaria (muestreo cada 2 días en registros antiguos)
- `Extent`: Área cubierta por hielo marino
- `Missing`: Área sin datos

**Fuente:** NSIDC (National Snow and Ice Data Center)  
**Uso:** Predictor principal - correlación con distribución de krill según Atkinson et al. 2004

---

## Datasets Incompletos (requieren descarga)

### 5. KRILLBASE (krillbase/) - VARIABLE OBJETIVO ⚠️

**Estado:** VACÍO - **CRÍTICO PARA MODELO**

**Archivo esperado:** `krillbase_data.csv`

**Descripción:**
- Variable objetivo (Y) para el modelo: densidad de krill
- Basado en datos de Atkinson et al. 2004
- Incluye datos de muestreos científicos de biomasa de krill
- Debe colocarse manualmente en esta carpeta

**Sin este archivo el modelo NO puede entrenarse.**

---

### 6. CMEMS - Copernicus Marine Service (cmems_instrucciones/)

**Estado:** INSTRUCCIONES SOLAMENTE

**Variables a descargar:**
| Variable | Dataset ID | Descripción |
|----------|------------|-------------|
| `mlotst` | GLOBAL_MULTIYEAR_PHY_001_030 | Mixed Layer Depth (m) |
| `thetao` | GLOBAL_MULTIYEAR_PHY_001_030 | Sea Surface Temperature (°C) |

**Período:** 2000-2024  
**Área:** -80° a -45° latitud (Antártida)  
**Requiere:** Registro gratuito en copernicus.eu

---

### 7. NASA Giovanni (nasa_giovanni_instrucciones/)

**Estado:** INSTRUCCIONES SOLAMENTE

**Variables a descargar:**
| Variable | Producto | Descripción |
|----------|----------|-------------|
| `chlor_a` | MODIS-Aqua L3 | Clorofila-a (mg/m³) |
| `sst` | MODIS-Aqua L3 | SST satelital (°C) |

**Período:** 2002-2024  
**Resolución:** 9 km  
**Requiere:** Sin registro (acceso directo)

---

### 8. CCAMLR - Comisión de Pesca (ccamlr_instrucciones/)

**Estado:** INSTRUCCIONES SOLAMENTE

**Variables a descargar:**
| Variable | Descripción |
|----------|-------------|
| CPUE | Captura por Unidad de Esfuerzo (toneladas/hora) |
| AREA | Subzonas CCAMLR (48.1, 48.2, 48.3, 58.4, etc.) |

**Período:** 1990-2024  
**Requiere:** Registro aprobado (1-2 días hábiles)

---

### 5. KRILLBASE - Variable Objetivo (krillbase/) ✅ NUEVO

**Archivos:**
- `krillbase_data.csv` (**14,736 registros**, 4.3 MB)
- `krillbase_column_descriptions.csv` (descripción de columnas)

**Estructura (columnas principales):**
```
STATION, LATITUDE, LONGITUDE, SEASON, DATE, 
STANDARDISED_KRILL_UNDER_1M2,  # ← VARIABLE OBJETIVO (Y)
CLIMATOLOGICAL_TEMPERATURE, WATER_DEPTH_MEAN_WITHIN_10KM,
N_OR_S_POLAR_FRONT, NET_TYPE, BOTTOM_SAMPLING_DEPTH_M
```

**Descripción:**
- Base de datos de densidad de krill estandarizada (Atkinson et al. 2004, 2008)
- Período: 1926-2016 (temporadas de verano austral)
- Variable objetivo: `STANDARDISED_KRILL_UNDER_1M2` (número de krill por m²)
- Estandarizado a: RMT8 nocturno 0-200m, 1 de enero
- Incluye metadatos de ubicación, profundidad, temperatura, tipo de red

**Uso:** Variable Y para entrenamiento del modelo XGBoost

---

### 6. NASA Giovanni (nasa_giovanni/)

**Estado:** INTento AUTOMÁTICO + BACKUP MANUAL

**Script:** `descargar_datos_antarticos.py` intenta descarga automática via API

**Si falla automático:**
1. Ir a https://giovanni.gsfc.nasa.gov/giovanni/
2. Time Series → Area Averaged
3. Región: -80S a -45S, -180W a 180E
4. Variables: MODIS Clorofila-a + SST
5. Guardar en `nasa_giovanni/`

**Archivos esperados:**
- `giovanni_chlor_a_mensual.csv`
- `giovanni_sst_mensual.csv`

---

### 7. CMEMS (cmems/)

**Estado:** AUTOMÁTICO (si está instalado) o MANUAL

**Pre-requisito:**
```bash
pip install copernicusmarine
copernicusmarine login  # cuenta gratis en marine.copernicus.eu
```

**Script automático:** `descargar_cmems.sh` (Linux/Mac) o `descargar_cmems.bat` (Windows)

**Variables:**
- `mlotst`: Mixed Layer Depth (metros)
- `thetao`: Sea Surface Temperature (°C)

**Dataset ID:** `cmems_mod_glo_phy_my_0.083deg_PT1H-m`

---

### 8. CCAMLR - Pesca (ccamlr_instrucciones/)

**Estado:** MANUAL (requiere registro)

URL: https://www.ccamlr.org/en/data/statistical-data

**Variables:** CPUE (toneladas/hora), Área (48.1, 48.2, 48.3, 58.4)

---

### 9. CMIP6 - Proyecciones Climáticas (cmip6_instrucciones/)

**Estado:** MANUAL (ESGF requiere registro)

**Escenarios:**
| Escenario | Descripción | Período |
|-----------|-------------|---------|
| SSP2-4.5 | Escenario moderado | 2025-2050 |
| SSP5-8.5 | Escenario pesimista | 2025-2050 |

**Variables:**
- `tos`: Sea Surface Temperature (SST futuro)
- `siconc`: Sea ice concentration

**Modelo recomendado:** IPSL-CM6A-LR (mejor resolución para Antártida)  
**Uso:** Inputs para proyecciones del modelo XGBoost a 2050

---

## Resumen de Completitud

| Dataset | Registros | Período | Estado | Rol en Modelo |
|---------|-----------|---------|--------|---------------|
| KRILLBASE | **14,736** | 1926-2016 | ✅ | **Variable Y objetivo** |
| ENSO MEI | 315 | 2000-2026 | ✅ | Variabilidad interanual |
| SAM Index | 316 | 2000-2026 | ✅ | Predictor principal |
| Fotoperiodo | 1,104 | 2001-2024 | ✅ | Innovación (luz) |
| Sea Ice | 15,684 | 1978-2025 | ✅ | Predictor principal |
| NASA Giovanni | - | 2002-2024 | 🤖 AUTO/MANUAL | Clorofila + SST satelital |
| CMEMS | - | 2000-2024 | 🤖 AUTO/MANUAL | MLD + SST oceánica |
| CCAMLR | - | 1990-2024 | ⚠️ MANUAL | Validación CPUE |
| CMIP6 | - | 2025-2050 | ⚠️ MANUAL | Proyecciones 2050 |

---

## Variables por Fuente (Tabla Integrada)

| Fuente | Variable | Rol | Respaldo Científico |
|--------|----------|-----|---------------------|
| KRILLBASE | krill_density | **Variable Y objetivo** | Atkinson et al. 2004 |
| SAM Index | SAM_9m_rolling | Predictor principal | Ryabov et al. 2023 |
| NSIDC | sea_ice_extent | Predictor principal | Atkinson et al. 2004 |
| MEI/ENSO | MEI_v2 | Variabilidad interanual | Murphy et al. 2007 |
| NASA Giovanni | chlor_a, sst | Predictores clave | Tarling et al. 2022 |
| CMEMS | MLD | Predictor secundario | Atkinson et al. 2004 |
| Fotoperiodo | daylight_hours | **INNOVACIÓN** | Ryabov et al. 2023 |
| CMIP6 | SST, siconc | Proyección 2050 | ScenarioMIP |

---

## Configuración del Modelo

**Algoritmo:** XGBoost con grid search  
**Lookback windows:** 3, 6, 9, 12, 18 meses  
**Split temporal:**
- Train: 2002-2019
- Test: 2020-2024
- **NOTA:** Sin shuffle (series temporales)

---

## Próximos Pasos para Completar el Dataset

1. **PRIORIDAD ALTA:** Colocar `krillbase_data.csv` en `krillbase/`
2. Descargar datos CMEMS (requiere registro)
3. Descargar datos NASA Giovanni (acceso inmediato)
4. Solicitar acceso CCAMLR (1-2 días de espera)
5. Descargar proyecciones CMIP6 para análisis futuro
