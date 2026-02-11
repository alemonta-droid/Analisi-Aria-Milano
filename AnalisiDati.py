import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import matplotlib.dates as mdates

st.set_page_config(page_title="Analisi Aria", layout="wide")
st.title(":red[Analisi dell'aria a Milano]", text_alignment="center")


base_path = os.path.dirname(__file__) 
file_stazioni = os.path.join(base_path, "qaria_stazione.geojson")

with open(file_stazioni, "r", encoding="utf8") as file:
    string_stazioni = json.loads(file.read())

lista_stazioni = string_stazioni["features"]

stazioni = []
for i in lista_stazioni:
    proprietà = {}
    proprietà["id"] = i["properties"]["id_amat"]
    proprietà["nome"] = i["properties"]["nome"]
    proprietà["inquinanti"] = i["properties"]["inquinanti"]
    proprietà["coordinate"] = i["geometry"]["coordinates"]
    stazioni.append(proprietà)


dati_completi_aria = []

for anno in range(2016, 2026):
    file_name = os.path.join(base_path, f"{anno}_stazioni.json") 
    
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf8") as file:
            dati_anno = json.load(file)
            dati_completi_aria.extend(dati_anno)
    else:
        st.error(f"Attenzione: non trovo il file {file_name}")


# st.write(f"Totale stazioni caricate: {len(stazioni)}")
# st.write(f"Totale record aria caricati (2016-2025): {len(dati_completi_aria)}")

df_aria = pd.DataFrame(dati_completi_aria)


df_aria['data'] = pd.to_datetime(df_aria['data'])
df_aria['anno'] = df_aria['data'].dt.year
df_aria['mese'] = df_aria['data'].dt.month
df_aria['valore'] = pd.to_numeric(df_aria['valore'], errors='coerce')

st.divider()
st.subheader(":red[Numero di misurazioni per anno]")


#Primo grafico: Conteggio delle misurazioni per ogni anno
if not df_aria.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set_theme(style="darkgrid")
    plt.rcParams.update({
        'figure.facecolor': "#000000", 
        'axes.facecolor': "#000000",
        'text.color': 'white', 
        'axes.labelcolor': 'white', 
        'xtick.color': 'white', 
        'ytick.color': 'white'
    })
    palette_1=sns.diverging_palette(220,20, n=20)
    sns.countplot(data=df_aria, y='anno', palette=palette_1, ax=ax)
    ax.set_title("Conteggio record totali per ogni anno", color='white')
    ax.set_xlabel("Conteggio delle misurazioni")
    ax.set_ylabel("Anno")
    st.pyplot(fig,width="content")


# Secondo grafico
st.divider()
Anno = st.slider("Scegli l'anno", 2016, 2025)
st.subheader(f"Andamento mensile inquinanti nel {Anno}")


df_anno_filtrato = df_aria[df_aria['anno'] == Anno].dropna(subset=['valore'])
#prende i valori solo dell'anno sullo slider ed elimina valori mancanti

if not df_anno_filtrato.empty:
    lista_gas = sorted(df_anno_filtrato['inquinante'].unique())
    gas_scelto = st.selectbox("Seleziona l'inquinante da visualizzare:", lista_gas)
    
    df_gas = df_anno_filtrato[df_anno_filtrato['inquinante'] == gas_scelto]
    df_mensile = df_gas.groupby('mese')['valore'].mean().reset_index() 
    #mean=media matematica, reset index rende una colonna mese groupby non so

    fig_line, ax_line = plt.subplots(figsize=(10, 5))
    
    sns.lineplot(
        data=df_mensile, 
        x='mese', 
        y='valore', 
        marker='o', 
        markersize=8,
        linewidth=5, 
        color="#173bb1", 
        ax=ax_line
    )
    
    ax_line.set_xticks(range(1, 13))
    ax_line.set_xticklabels(['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'])
    
    ax_line.set_ylabel(f"Media {gas_scelto} (µg/m³)")
    ax_line.set_xlabel("Mese")
    ax_line.grid(True, alpha=0.15, linestyle='--')

    st.pyplot(fig_line, width="content")


#Terzo grafico

st.divider()
st.subheader("Qualità dell'aria media per Stazione (2016-2025)")


df_info_stazioni = pd.DataFrame(stazioni)[['id', 'nome']]

df_aria_nomi = pd.merge(df_aria, df_info_stazioni, left_on='stazione_id',right_on='id')
#unisce i due database


lista_gas_totali = sorted(df_aria_nomi['inquinante'].unique())
gas_confronto = st.selectbox("Seleziona l'inquinante per il confronto tra stazioni:", lista_gas_totali)

# PASSAGGIO 3: Filtro e Calcolo
df_confronto = df_aria_nomi[df_aria_nomi['inquinante'] == gas_confronto]
 
# Calcoliamo la media per ogni stazione
df_medie_stazioni = df_confronto.groupby('nome')['valore'].mean().sort_values(ascending=False).reset_index()

# PASSAGGIO 4: Creazione del Grafico
if not df_medie_stazioni.empty:
    fig_staz, ax_staz = plt.subplots(figsize=(12, 8))
    
    # Usiamo un grafico a barre orizzontali (barh) per leggere meglio i nomi delle stazioni
    sns.barplot(
        data=df_medie_stazioni, 
        y='nome', 
        x='valore', 
        palette='magma', 
        ax=ax_staz
    )
    
    ax_staz.set_title(f"Classifica stazioni per media decennale di {gas_confronto}", fontsize=15)
    ax_staz.set_xlabel("Valore medio (µg/m³)")
    ax_staz.set_ylabel("Stazione")
    ax_staz.grid(True, alpha=0.2, axis='x')
    
    st.pyplot(fig_staz, width="content")

    # PASSAGGIO 5: Tabella di riepilogo
    with st.expander("Vedi classifica testuale"):
        st.write(df_medie_stazioni)
else:
    st.info("Dati non sufficienti per calcolare le medie decennali di questo gas.")

st.divider()



#Quarto grafico


df_info_stazioni = pd.DataFrame(stazioni)[['id', 'nome']]
df_info_stazioni['id'] = df_info_stazioni['id'].astype(str)

# PASSAGGIO 2: Preparazione tabella aria
# Forziamo anche stazione_id a essere STRINGA per non avere errori di tipo
df_aria_merge = df_aria.copy()
df_aria_merge['stazione_id'] = df_aria_merge['stazione_id'].astype(str)

# PASSAGGIO 3: L'Unione (Merge)
# Uniamo le due tabelle: usiamo 'stazione_id' per l'aria e 'id' per le stazioni
df_totale = pd.merge(df_aria_merge, df_info_stazioni, left_on='stazione_id', right_on='id')

# PASSAGGIO 4: Selezione dell'anno
# Invece di scrivere 2025, prendiamo l'anno più recente caricato nei dati
anno_recente = int(df_totale['anno'].max())
st.subheader(f"🔍 Focus {anno_recente}: Andamento mensile per Stazione")

# Filtriamo i dati per l'anno trovato
df_focus = df_totale[df_totale['anno'] == anno_recente].copy()

if not df_focus.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Mostriamo i nomi reali (viale Marche, via Senato...) invece degli ID
        stazione_scelta = st.selectbox("Seleziona la Stazione:", sorted(df_focus['nome'].unique()), key="f_staz")
    
    with col2:
        # Filtriamo gli inquinanti disponibili per quella specifica stazione
        gas_per_stazione = sorted(df_focus[df_focus['nome'] == stazione_scelta]['inquinante'].unique())
        gas_scelto = st.selectbox("Inquinante:", gas_per_stazione, key="f_gas")

    # PASSAGGIO 5: Calcolo media e Grafico
    df_plot_focus = df_focus[(df_focus['nome'] == stazione_scelta) & (df_focus['inquinante'] == gas_scelto)]
    
    # Calcoliamo la media mensile
    df_mensile_focus = df_plot_focus.groupby('mese')['valore'].mean().reset_index()

    if not df_mensile_focus.empty:
        fig_f, ax_f = plt.subplots(figsize=(10, 4))
        
        # Disegniamo la linea
        sns.lineplot(data=df_mensile_focus, x='mese', y='valore', marker='s', color='#FF4B4B', ax=ax_f)
        
        # --- EVIDENZIAZIONE PICCO (Variabile corretta) ---
        # Troviamo il punto massimo nel dataframe appena creato
        picco = df_mensile_focus.loc[df_mensile_focus['valore'].idxmax()]

        # Disegniamo il cerchio rosso sopra il picco
        ax_f.plot(picco['mese'], picco['valore'], 'o', color='red', markersize=12)
        
        # Formattazione assi e titoli
        ax_f.set_xticks(range(1, 13))
        ax_f.set_xticklabels(['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'])
        ax_f.set_title(f"{gas_scelto} a {stazione_scelta} - Media Mensile {anno_recente}")
        
        st.pyplot(fig_f, width="content")
    else:
        st.info("Nessun dato valido per generare la linea (controlla la colonna 'valore').")