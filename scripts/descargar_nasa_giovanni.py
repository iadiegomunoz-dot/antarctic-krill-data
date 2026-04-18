"""
=============================================================
  DESCARGA NASA MODIS-AQUA: Clorofila-a y SST
  Usa la librería oficial de NASA: earthaccess
  
  REQUISITO PREVIO:
    1. Crear cuenta GRATIS en: https://urs.earthdata.nasa.gov/users/new
    2. pip install earthaccess xarray netCDF4 numpy pandas

  OUTPUT:
    data_antartica/nasa_giovanni/
      ├── chlor_a_antartico_YYYY_MM.nc   (un archivo por mes)
      ├── sst_antartico_YYYY_MM.nc
      └── nasa_antartico_mensual.csv     ← CSV final listo para XGBoost
=============================================================
"""

import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

# ── Verificar dependencias ─────────────────────────────────────────────────
try:
    import earthaccess
except ImportError:
    print("✗ Falta earthaccess. Ejecuta: pip install earthaccess")
    sys.exit(1)

try:
    import xarray as xr
except ImportError:
    print("✗ Falta xarray. Ejecuta: pip install xarray netCDF4")
    sys.exit(1)

# ── Configuración ──────────────────────────────────────────────────────────
BASE_DIR   = Path("data_antartica/nasa_giovanni")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Región Océano Austral (W, S, E, N)
BBOX = (-180, -80, 180, -45)

# Período de interés
FECHA_INICIO = "2002-07-01"
FECHA_FIN    = "2024-12-31"

# Short names oficiales NASA OB.DAAC
DATASETS = {
    "CHL": {
        "short_name":    "MODISA_L3m_CHL",
        "granule_filter": "*.MO*.CHL*.9km*.nc",   # mensual, 9km, netCDF
        "variable":       "chlor_a",
        "unidad":         "mg/m³",
        "descripcion":    "Clorofila-a (proxy biomasa fitoplancton)"
    },
    "SST": {
        "short_name":    "MODISA_L3m_SST",
        "granule_filter": "*.MO*.SST*.9km*.nc",
        "variable":       "sst",
        "unidad":         "°C",
        "descripcion":    "Temperatura superficial del mar"
    }
}

# ── PASO 1: Login con NASA Earthdata ──────────────────────────────────────
def login_nasa():
    print("\n" + "═"*60)
    print("  PASO 1: Autenticación NASA Earthdata")
    print("═"*60)
    print("""
  Si no tienes cuenta, créala gratis en:
  → https://urs.earthdata.nasa.gov/users/new

  El login va a pedir tu usuario y contraseña.
  Las credenciales se guardan en ~/.netrc para usos futuros.
""")
    try:
        auth = earthaccess.login(strategy="interactive", persist=True)
        if auth.authenticated:
            print("  ✓ Login exitoso con NASA Earthdata")
            return True
        else:
            print("  ✗ Login fallido. Verifica usuario/contraseña")
            return False
    except Exception as e:
        print(f"  ✗ Error de login: {e}")
        return False


# ── MÉTODO ALTERNATIVO: Descarga desde Giovanni Web ───────────────────────
def descargar_giovanni_web():
    """
    Descarga manual-simulada desde NASA Giovanni interface web.
    Útil si earthaccess no funciona o como backup.
    """
    print("\n" + "═"*60)
    print("  MÉTODO ALTERNATIVO: NASA Giovanni Web Interface")
    print("═"*60)
    print("""
  Si earthaccess falla, sigue estos pasos MANUALES:

  1. Ir a: https://giovanni.gsfc.nasa.gov/giovanni/

  2. Configurar consulta:
     - Select Plot: Time Series, Area Averaged
     - Date Range: 2002-07-04 to 2024-12-31
     - Region: -80S to -45S, -180W to 180E

  3. Descargar CLOROFILA-A:
     - Search: MODIS Aqua Level 3 Monthly chlorophyll
     - Variable: MODISA_L3m_CHL_Monthly_9km_R2022_0_chlor_a
     - Download as: CSV
     - Save: data_antartica/nasa_giovanni/giovanni_chlor_a.csv

  4. Descargar SST:
     - Variable: MODISA_L3m_SST_Monthly_9km_R2022_0_sst
     - Download as: CSV
     - Save: data_antartica/nasa_giovanni/giovanni_sst.csv

  5. Ejecutar procesamiento:
     python descargar_nasa_giovanni.py --procesar-csv
""")
    return False


# ── PASO 2: Buscar y descargar archivos mensuales ─────────────────────────
def descargar_dataset(nombre, config):
    print(f"\n{'═'*60}")
    print(f"  DESCARGANDO: {nombre} — {config['descripcion']}")
    print(f"{'═'*60}")

    carpeta = BASE_DIR / nombre.lower()
    carpeta.mkdir(exist_ok=True)

    print(f"  Buscando granules mensuales {FECHA_INICIO} → {FECHA_FIN}...")
    print(f"  Región: Océano Austral (-80° a -45° lat)")
    print(f"  Short name: {config['short_name']}")

    try:
        resultados = earthaccess.search_data(
            short_name   = config["short_name"],
            granule_name = config["granule_filter"],
            temporal     = (FECHA_INICIO, FECHA_FIN),
            bounding_box = BBOX,
            count        = -1  # todos los resultados
        )

        if not resultados:
            print(f"  ✗ Sin resultados para {nombre}")
            print(f"    Prueba con granule_filter más amplio")
            # Intento sin filtro de nombre
            print("  Reintentando sin filtro de granule_name...")
            resultados = earthaccess.search_data(
                short_name   = config["short_name"],
                temporal     = (FECHA_INICIO, FECHA_FIN),
                count        = -1
            )
            # Filtrar manualmente los mensuales de 9km
            resultados = [r for r in resultados
                         if ".MO." in str(r) or "monthly" in str(r).lower()]

        print(f"  ✓ Encontrados: {len(resultados)} archivos mensuales")

        if len(resultados) == 0:
            print("  ✗ No se encontraron archivos. Verifica la cuenta Earthdata.")
            return []

        # Descargar
        print(f"  Descargando a: {carpeta}/")
        print("  (Esto puede tomar 5-15 minutos según conexión)\n")

        archivos = earthaccess.download(
            resultados,
            local_path=str(carpeta)
        )
        print(f"\n  ✓ Descargados: {len(archivos)} archivos")
        return archivos

    except Exception as e:
        print(f"  ✗ Error descargando {nombre}: {e}")
        return []


# ── PASO 3: Procesar NetCDF → CSV mensual promedio Océano Austral ─────────
def procesar_a_csv(nombre, config):
    print(f"\n{'═'*60}")
    print(f"  PROCESANDO: {nombre} → CSV mensual")
    print(f"{'═'*60}")

    carpeta  = BASE_DIR / nombre.lower()
    archivos = sorted(carpeta.glob("*.nc"))

    if not archivos:
        print(f"  ✗ No hay archivos .nc en {carpeta}")
        return pd.DataFrame()

    print(f"  Procesando {len(archivos)} archivos NetCDF...")

    filas = []
    for nc_path in archivos:
        try:
            ds = xr.open_dataset(nc_path, engine="netcdf4")

            # Detectar variable (el nombre puede variar)
            var_name = config["variable"]
            if var_name not in ds:
                # Buscar variable alternativa
                candidatos = [v for v in ds.data_vars
                              if any(k in v.lower()
                                     for k in ["chlor", "sst", "chl"])]
                if candidatos:
                    var_name = candidatos[0]
                    print(f"    Usando variable alternativa: {var_name}")
                else:
                    print(f"    ✗ Variable no encontrada en {nc_path.name}")
                    print(f"      Variables disponibles: {list(ds.data_vars)}")
                    continue

            data = ds[var_name]

            # Extraer coordenadas lat/lon
            lat_name = "lat" if "lat" in ds.coords else "latitude"
            lon_name = "lon" if "lon" in ds.coords else "longitude"

            # Filtrar región Océano Austral: -80° a -45° lat
            lat_vals = ds[lat_name].values
            mask_lat = (lat_vals >= -80) & (lat_vals <= -45)

            data_sur = data.sel({lat_name: lat_vals[mask_lat]})

            # Promedio espacial (media de toda la región)
            valor_medio = float(data_sur.mean(skipna=True).values)
            valor_std   = float(data_sur.std(skipna=True).values)
            n_pixeles   = int((~np.isnan(data_sur.values)).sum())

            # Extraer fecha del nombre del archivo o atributos
            fecha = extraer_fecha(nc_path, ds)

            if fecha and not np.isnan(valor_medio):
                filas.append({
                    "year":           fecha.year,
                    "month":          fecha.month,
                    f"{nombre}_mean": round(valor_medio, 4),
                    f"{nombre}_std":  round(valor_std, 4),
                    f"{nombre}_n_px": n_pixeles,
                })
                print(f"    ✓ {fecha.strftime('%Y-%m')} | "
                      f"mean={valor_medio:.3f} {config['unidad']} | "
                      f"n={n_pixeles:,} px")
            else:
                print(f"    ⚠ {nc_path.name}: sin datos válidos")

            ds.close()

        except Exception as e:
            print(f"    ✗ Error procesando {nc_path.name}: {e}")

    if not filas:
        return pd.DataFrame()

    df = pd.DataFrame(filas).sort_values(["year", "month"]).reset_index(drop=True)
    print(f"\n  ✓ Procesados: {len(df)} meses ({df.year.min()}-{df.year.max()})")
    return df


def extraer_fecha(nc_path, ds):
    """Extraer año/mes del nombre del archivo o atributos del NetCDF."""
    nombre = nc_path.stem  # ej: AQUA_MODIS.20030101_20030131.L3m.MO.CHL.chlor_a.9km

    # Patrón NASA OB.DAAC: AQUA_MODIS.YYYYMMDD_YYYYMMDD.L3m...
    import re
    match = re.search(r'(\d{4})(\d{2})\d{2}_', nombre)
    if match:
        return datetime(int(match.group(1)), int(match.group(2)), 1)

    # Intento con atributos del NetCDF
    for attr in ["time_coverage_start", "start_time", "date_created"]:
        if attr in ds.attrs:
            try:
                return datetime.strptime(ds.attrs[attr][:7], "%Y-%m")
            except Exception:
                pass

    # Intento con coordenada time
    if "time" in ds.coords:
        try:
            t = pd.to_datetime(str(ds.coords["time"].values[0]))
            return datetime(t.year, t.month, 1)
        except Exception:
            pass

    print(f"    ⚠ No se pudo extraer fecha de {nc_path.name}")
    return None


# ── PASO 4: Procesar CSV descargado manualmente de Giovanni ──────────────
def procesar_csv_giovanni():
    """
    Procesar archivos CSV descargados manualmente desde Giovanni.
    """
    print("\n" + "═"*60)
    print("  PROCESANDO CSV descargados manualmente desde Giovanni")
    print("═"*60)

    giovanni_dir = BASE_DIR
    csv_chl = giovanni_dir / "giovanni_chlor_a.csv"
    csv_sst = giovanni_dir / "giovanni_sst.csv"

    dfs = []

    for archivo, nombre in [(csv_chl, "CHL"), (csv_sst, "SST")]:
        if not archivo.exists():
            print(f"  ✗ No encontrado: {archivo.name}")
            continue

        print(f"\n  Leyendo {archivo.name}...")
        try:
            # Giovanni CSV tiene formato específico
            df = pd.read_csv(archivo, skiprows=14)  # Saltar headers de metadata

            # Detectar columnas de fecha y variable
            col_fecha = None
            col_var = None

            for col in df.columns:
                col_lower = col.lower()
                if any(x in col_lower for x in ["time", "date", "day", "month", "year"]):
                    col_fecha = col
                if nombre == "CHL" and any(x in col_lower for x in ["chlor", "chl"]):
                    col_var = col
                if nombre == "SST" and any(x in col_lower for x in ["sst", "temp"]):
                    col_var = col

            if col_fecha and col_var:
                df["date"] = pd.to_datetime(df[col_fecha])
                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month
                df[f"{nombre}_mean"] = df[col_var]

                df_out = df[["year", "month", f"{nombre}_mean"]].copy()
                dfs.append(df_out)
                print(f"  ✓ {nombre}: {len(df_out)} registros")
            else:
                print(f"  ✗ Columnas no identificadas en {archivo.name}")
                print(f"    Columnas disponibles: {list(df.columns)}")

        except Exception as e:
            print(f"  ✗ Error procesando {archivo.name}: {e}")

    if len(dfs) == 2:
        df_final = pd.merge(dfs[0], dfs[1], on=["year", "month"], how="outer")
    elif len(dfs) == 1:
        df_final = dfs[0]
    else:
        print("\n  ✗ No se pudieron procesar los CSV")
        return None

    df_final = df_final.sort_values(["year", "month"]).reset_index(drop=True)

    # Calcular anomalías
    for col in ["CHL_mean", "SST_mean"]:
        if col in df_final.columns:
            clim = df_final.groupby("month")[col].mean()
            df_final[f"{col}_anomaly"] = df_final.apply(
                lambda r: r[col] - clim.get(r["month"], np.nan), axis=1
            ).round(4)

    dest = BASE_DIR / "nasa_antartico_mensual.csv"
    df_final.to_csv(dest, index=False)

    print(f"\n  ✓ CSV combinado guardado: {dest}")
    print(f"  ✓ Total: {len(df_final)} meses ({df_final.year.min()}-{df_final.year.max()})")
    print(f"\n  Vista previa:")
    print(df_final.head(10).to_string(index=False))

    return df_final


# ── PASO 4: Combinar CHL + SST en un único CSV ────────────────────────────
def combinar_y_guardar(df_chl, df_sst):
    print(f"\n{'═'*60}")
    print("  COMBINANDO CHL + SST → CSV final")
    print(f"{'═'*60}")

    dfs = []
    if not df_chl.empty:
        dfs.append(df_chl)
    if not df_sst.empty:
        dfs.append(df_sst)

    if not dfs:
        print("  ✗ Sin datos para combinar")
        return

    if len(dfs) == 2:
        df_final = pd.merge(df_chl, df_sst, on=["year", "month"], how="outer")
    else:
        df_final = dfs[0]

    df_final = df_final.sort_values(["year", "month"]).reset_index(drop=True)

    # Agregar anomalías respecto a climatología mensual
    for col in ["CHL_mean", "SST_mean"]:
        if col in df_final.columns:
            clim = df_final.groupby("month")[col].mean()
            df_final[f"{col}_anomaly"] = df_final.apply(
                lambda r: r[col] - clim.get(r["month"], np.nan), axis=1
            ).round(4)

    dest = BASE_DIR / "nasa_antartico_mensual.csv"
    df_final.to_csv(dest, index=False)

    print(f"  ✓ CSV guardado: {dest}")
    print(f"  ✓ Registros: {len(df_final)} meses")
    print(f"  ✓ Variables: {list(df_final.columns)}")
    print(f"\n  Vista previa:")
    print(df_final.head(8).to_string(index=False))

    return df_final


# ── MAIN ──────────────────────────────────────────────────────────────────
def main():
    print("\n" + "█"*62)
    print("  DESCARGA NASA MODIS-AQUA: Clorofila-a + SST")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("█"*62)

    print("""
  DATASETS A DESCARGAR:
    → Clorofila-a (MODISA_L3m_CHL) — 2002-2024 mensual 9km
    → SST (MODISA_L3m_SST)         — 2002-2024 mensual 9km
    → Región: Océano Austral (-80° a -45° lat)

  TIEMPO ESTIMADO:
    → Login:    2 minutos
    → Búsqueda: 1-2 minutos
    → Descarga: 10-30 minutos (depende de conexión)
    → Proceso:  2-3 minutos
""")

    # 1. Login
    if not login_nasa():
        print("\n  ✗ No se pudo autenticar. Abortando.")
        print("  Crea tu cuenta en: https://urs.earthdata.nasa.gov/users/new")
        return

    # 2. Descargar y procesar cada dataset
    df_chl = pd.DataFrame()
    df_sst = pd.DataFrame()

    for nombre, config in DATASETS.items():
        archivos = descargar_dataset(nombre, config)
        if archivos:
            if nombre == "CHL":
                df_chl = procesar_a_csv(nombre, config)
            else:
                df_sst = procesar_a_csv(nombre, config)
        else:
            # Si ya estaban descargados, procesar igual
            carpeta = BASE_DIR / nombre.lower()
            if list(carpeta.glob("*.nc")):
                print(f"\n  → Archivos ya descargados. Procesando {nombre}...")
                if nombre == "CHL":
                    df_chl = procesar_a_csv(nombre, config)
                else:
                    df_sst = procesar_a_csv(nombre, config)

    # 3. Combinar
    combinar_y_guardar(df_chl, df_sst)

    print("\n" + "═"*62)
    print("  RESUMEN FINAL")
    print("═"*62)
    print(f"""
  Archivos generados en: {BASE_DIR}/
    ├── chl/          ← NetCDF mensuales de clorofila (sin tocar)
    ├── sst/          ← NetCDF mensuales de SST (sin tocar)
    └── nasa_antartico_mensual.csv  ← LISTO PARA XGBOOST

  Variables en el CSV final:
    year, month
    CHL_mean, CHL_std, CHL_n_px, CHL_mean_anomaly
    SST_mean, SST_std, SST_n_px, SST_mean_anomaly

  Siguiente paso:
    → python 02_unificar_dataset.py
""")


def generar_reporte():
    """Generar reporte de estado de los datos NASA."""
    print("\n" + "█"*62)
    print("  REPORTE DE ESTADO: NASA GIOVANNI DATA")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("█"*62)

    reporte = []
    reporte.append(f"\n📁 Directorio: {BASE_DIR}")
    reporte.append(f"{'─'*60}\n")

    # Verificar archivos
    archivos_netcdf_chl = list((BASE_DIR / "chl").glob("*.nc")) if (BASE_DIR / "chl").exists() else []
    archivos_netcdf_sst = list((BASE_DIR / "sst").glob("*.nc")) if (BASE_DIR / "sst").exists() else []
    csv_giovanni_chl = BASE_DIR / "giovanni_chlor_a.csv"
    csv_giovanni_sst = BASE_DIR / "giovanni_sst.csv"
    csv_final = BASE_DIR / "nasa_antartico_mensual.csv"

    # CHL
    if archivos_netcdf_chl:
        reporte.append(f"✅ CHL (NetCDF): {len(archivos_netcdf_chl)} archivos")
    elif csv_giovanni_chl.exists():
        reporte.append(f"✅ CHL (CSV Giovanni): {csv_giovanni_chl.name}")
    else:
        reporte.append(f"❌ CHL: NO DESCARGADO")

    # SST
    if archivos_netcdf_sst:
        reporte.append(f"✅ SST (NetCDF): {len(archivos_netcdf_sst)} archivos")
    elif csv_giovanni_sst.exists():
        reporte.append(f"✅ SST (CSV Giovanni): {csv_giovanni_sst.name}")
    else:
        reporte.append(f"❌ SST: NO DESCARGADO")

    # CSV Final
    if csv_final.exists():
        df = pd.read_csv(csv_final)
        reporte.append(f"\n✅ CSV FINAL: {csv_final.name}")
        reporte.append(f"   Registros: {len(df)}")
        reporte.append(f"   Período: {df.year.min()}-{df.year.max()}")
        reporte.append(f"   Columnas: {list(df.columns)}")
    else:
        reporte.append(f"\n❌ CSV FINAL: NO GENERADO")

    reporte.append(f"\n{'─'*60}")
    reporte.append(f"\n📊 RESUMEN:")
    reporte.append(f"   • Método earthaccess: {'✅' if archivos_netcdf_chl or archivos_netcdf_sst else '❌'}")
    reporte.append(f"   • Método Giovanni CSV: {'✅' if csv_giovanni_chl.exists() or csv_giovanni_sst.exists() else '❌'}")
    reporte.append(f"   • CSV procesado: {'✅' if csv_final.exists() else '❌'}")

    reporte_texto = "\n".join(reporte)
    print(reporte_texto)

    # Guardar reporte
    reporte_path = BASE_DIR / "REPORTE_ESTADO.txt"
    reporte_path.write_text(reporte_texto, encoding='utf-8')
    print(f"\n💾 Reporte guardado: {reporte_path}")

    return csv_final.exists()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Descarga NASA Giovanni")
    parser.add_argument("--reporte", action="store_true", help="Solo generar reporte")
    parser.add_argument("--procesar-csv", action="store_true", help="Procesar CSV manual")
    parser.add_argument("--instrucciones", action="store_true", help="Mostrar instrucciones manuales")
    args = parser.parse_args()

    if args.reporte:
        generar_reporte()
    elif args.procesar_csv:
        procesar_csv_giovanni()
    elif args.instrucciones:
        descargar_giovanni_web()
    else:
        main()
