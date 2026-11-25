import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime
import os


# NETCDF List
# 0–2  -> Shallow  (max, mean, min)
# 3–5  -> Average  (max, mean, min)
# 6–8  -> Deep     (max, mean, min)

temp_list = [
    r"\dataset\nc_files\Shallow\max_temp_shallow.nc",
    r"\nc_files\Shallow\mean_temp_shallow.nc",
    r"\nc_files\Shallow\min_temp_shallow.nc",

    r"\nc_files\Average\max_temp_average.nc",
    r"\nc_files\Average\mean_temp_average.nc",
    r"\nc_files\Average\min_temp_average.nc",

    r"\nc_files\Deep\max_temp_deep.nc",
    r"\nc_files\Deep\mean_temp_deep.nc",
    r"\nc_files\Deep\min_temp_deep.nc",
]

def extrator_temp_por_label(
    var_csv: str,
    temp_list: list,
    output_base_dir: str,
    tolerance: float = 0.1
):
    """
    Extrai temperaturas (max, mean, min) a partir de NetCDFs
    selecionados dinamicamente conforme rótulo (0, 1, 2).

    CSV de entrada deve conter:
    - lat
    - lon
    - label (0, 1 ou 2)
    """

    
    # CSV Read
    
    df = pd.read_csv(var_csv)

    required_cols = {"lat", "lon", "label"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"O CSV deve conter as colunas: {required_cols}")

    df["lat"] = pd.to_numeric(df["lat"], errors="raise")
    df["lon"] = pd.to_numeric(df["lon"], errors="raise")
    df["label"] = df["label"].astype(int)

    df_final = df.copy()

    
    # Mapping
    
    label_to_indices = {
        0: (0, 1, 2),  # Shallow
        1: (3, 4, 5),  # Average
        2: (6, 7, 8)   # Deep
    }

    var_order = ["max", "mean", "min"]

    var_names = {
        "max": "thetao_max",
        "mean": "thetao_mean",
        "min": "thetao_min"
    }

    # Columns
    for v in var_order:
        df_final[f"temp_{v}"] = np.nan

    
    # Loop 
    
    for idx, row in df.iterrows():
        label = row["label"]
        if label not in label_to_indices:
            continue

        nc_indices = label_to_indices[label]

        for nc_idx, var_type in zip(nc_indices, var_order):

            nc_path = temp_list[nc_idx]
            var_name = var_names[var_type]

            with xr.open_dataset(nc_path) as ds:

                # Detectar nomes das coordenadas
                lat_name = "lat" if "lat" in ds.coords else "latitude"
                lon_name = "lon" if "lon" in ds.coords else "longitude"

                # Verificar se o ponto está dentro do grid
                if (
                    row["lat"] < float(ds[lat_name].min()) or
                    row["lat"] > float(ds[lat_name].max()) or
                    row["lon"] < float(ds[lon_name].min()) or
                    row["lon"] > float(ds[lon_name].max())
                ):
                    value = np.nan
                else:
                    value = ds[var_name].sel(
                        **{lat_name: row["lat"], lon_name: row["lon"]},
                        method="nearest",
                        tolerance=tolerance
                    ).values.item()

                df_final.at[idx, f"temp_{var_type}"] = (
                    round(value, 2) if pd.notna(value) else np.nan
                )

   
    # Save
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_base_dir, exist_ok=True)

    csv_path = os.path.join(output_base_dir, f"temp_por_label_{timestamp}.csv")
    xlsx_path = os.path.join(output_base_dir, f"temp_por_label_{timestamp}.xlsx")

    df_final.to_csv(csv_path, index=False)
    df_final.to_excel(xlsx_path, index=False)

    print("Arquivos gerados:")
    print(csv_path)
    print(xlsx_path)

    return df_final


#Call

if __name__ == "__main__":

    df_result = extrator_temp_por_label(
        var_csv=r"C:\Users\lynic\OneDrive\Desktop\extracao_temp_env\dataset\nc_fake.csv",
        temp_list=temp_list,
        output_base_dir=r"C:\Users\lynic\OneDrive\Desktop\extracao_temp_env\dataset\results",
        tolerance=0.1
    )
