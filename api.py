from flask import Flask, jsonify, request
import xarray as xr
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

app = Flask(__name__)

# Configurações
VARIAVEIS = ["Tmin", "Tmax", "Rs", "Tmedia"]
PERIODO = slice("1991-01-01", "2020-12-31")
# ATENÇÃO: Ajuste este caminho para a pasta onde estão seus arquivos .nc
DATA_PATH = "D:/python/"  

def rodar_clusterizacao(n_clusters=12):
    lista_features = []

    # Carregar variáveis
    for nvar in VARIAVEIS:
        if nvar == "Tmedia":
            ds_tmax = xr.open_mfdataset(os.path.join(DATA_PATH, "Tmax*.nc"))
            ds_tmin = xr.open_mfdataset(os.path.join(DATA_PATH, "Tmin*.nc"))
            data_var = ((ds_tmax["Tmax"] + ds_tmin["Tmin"]) / 2).sel(time=PERIODO)
        else:
            ds = xr.open_mfdataset(os.path.join(DATA_PATH, f"{nvar}*.nc"))
            data_var = ds[nvar].sel(time=PERIODO)

        # Médias sazonais
        normais = data_var.groupby("time.season").mean("time")
        for est in ["DJF", "MAM", "JJA", "SON"]:
            lista_features.append(normais.sel(season=est, drop=True).rename(f"{nvar}_{est}"))

    # Combinar features
    features_ds = xr.merge(lista_features).compute()
    df = features_ds.to_dataframe().dropna().reset_index()
    if 'latitude' in df.columns:
        df = df.rename(columns={'latitude': 'lat'})
    if 'longitude' in df.columns:
        df = df.rename(columns={'longitude': 'lon'})
    feature_cols = [col for col in df.columns if col not in ['lat', 'lon']]
    
    # Padronizar
    scaler = StandardScaler()
    dados_pad = scaler.fit_transform(df[feature_cols].values)

    # Clusterizar
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(dados_pad)

    return df

@app.route("/")
def home():
    return "API de Clusterização Climática"

@app.route("/clusters", methods=["GET"])
def clusters():
    k = int(request.args.get("k", 6))
    df = rodar_clusterizacao(k)
    return df.to_json(orient="records")

@app.route("/resumo", methods=["GET"])
def resumo():
    k = int(request.args.get("k", 6))
    df = rodar_clusterizacao(k)
    resumo = df.groupby("cluster").mean(numeric_only=True).to_dict()
    return jsonify(resumo)

if __name__ == "__main__":
    app.run(debug=True)
