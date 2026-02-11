import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import matplotlib.dates as mdates

st.set_page_config(page_title="stretch", layout="wide")
st.title(":red[Analisi dell'aria a Milano]",width="stretch", text_alignment="center")
st.write("In questo progetto andremo ad esaminare i dati della qualità dell'aria degli ultimi dieci anni a Milano, conteggio delle misurazioni, media annuale per il valore di ogni gas, andamento annuale nel 2025, e una media per stazione del valore dei gas, in questo modo potremo rispondere a questioni comuni, se l'inquinamento sta diminuendo e il perchè sta succedendo.")
with st.expander("I gas inquinanti, cosa sono e perchè sono pericolosi"):
    st.subheader("Biossido di Azoto NO2")
    st.write("Il biossido di azoto è un gas irritante prodotto principalmente nelle combustioni ad alta temperatura, come quelle dei motori diesel e delle centrali termoelettriche. È pericoloso perché attacca le vie respiratorie causando infiammazioni croniche, edemi polmonari e un aumento della suscettibilità alle infezioni batteriche, oltre a essere un precursore dell'ozono e uno degli agenti che causano lo smog fotochimico.")
    st.subheader("Ozono O3")
    st.write("Il biossido di zolfo è un gas prodotto dalla combustione di carburanti fossili contenenti zolfo, come il carbone e gli oli combustibili utilizzati in ambito produttivo e navale. È pericoloso perché provoca grave irritazione polmonare ed è il principale responsabile delle piogge acide che acidificano suoli ed acque, danneggiando gli interi ecosistemi oltre alle costruzioni e ai monumenti.")
    st.subheader("Biossido di zolfo SO2")
    st.write("Il biossido di zolfo è un gas prodotto dalla combustione di carburanti fossili contenenti zolfo, come il carbone e gli oli combustibili utilizzati in ambito produttivo e navale. È pericoloso perché provoca grave irritazione polmonare ed è il principale responsabile delle piogge acide che acidificano suoli ed acque, danneggiando gli interi ecosistemi oltre alle costruzioni e ai monumenti.")
    st.subheader("Ozono O3")
    st.write("L'ozono troposferico non è emesso direttamente, ma si forma per reazione chimica tra ossidi di azoto (NOx) e composti organici volatili in presenza di forte radiazione solare. È un potente ossidante che irrita le mucose respiratorie e gli occhi, riducendo la funzionalità polmonare specialmente in bambini e anziani, oltre a danneggiare i tessuti delle piante e ridurre i raccolti agricoli.")
    st.subheader("Benzene C6H6")
    st.write("Il benzene è un idrocarburo aromatico derivante principalmente dalle emissioni dei veicoli a benzina e dai processi industriali di raffinazione. È classificato come cancerogeno certo per l'uomo: l'esposizione prolungata, anche a basse concentrazioni, è associata a un aumento del rischio di leucemie e altre malattie del sistema del sangue (emolinfopoietico).")
    st.subheader("Monossido di Carbonio CO")
    st.write("Il monossido di carbonio è un gas incolore e inodore prodotto dalla combustione incompleta di combustibili fossili e biomasse. La sua pericolosità deriva dalla capacità di legarsi all'emoglobina nel sangue molto più velocemente dell'ossigeno, riducendo il trasporto di ossigeno ai tessuti e causando, ad alte dosi, danni al sistema nervoso centrale e a quello cardiovascolare.")
    st.subheader("Particolato PM10")
    st.write("Il PM10 è costituito da polveri con diametro inferiore a 10 micrometri. Include particelle sia solide che liquide derivanti da traffico, riscaldamento e industrie. Queste particelle sono in grado di penetrare nel tratto superiore dell'apparato respiratorio, causando infiammazioni, asma e peggiorando patologie polmonari e cardiache preesistenti.")
    st.subheader("Particolato Fine PM2.5")
    st.write("Il PM2.5 rappresenta la frazione più sottile del particolato (diametro inferiore a 2.5 micrometri). A causa delle dimensioni ridottissime, queste polveri possono spingersi fino agli alveoli polmonari e passare direttamente nel flusso sanguigno. Sono considerate tra gli inquinanti più pericolosi per la salute umana, essendo correlate a malattie respiratorie gravi, tumori e disturbi cardiocircolatori.")

base_path = os.path.dirname(__file__) #unisce i percorsi dei file
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


df_aria['data'] = pd.to_datetime(df_aria['data']) #trasforma in una vera data
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
Anno = 2016
st.subheader(f":red[Andamento mensile inquinanti nel {Anno}]")
Anno = st.slider("Scegli l'anno", 2016, 2025)


df_anno_filtrato = df_aria[df_aria['anno'] == Anno].dropna(subset=['valore'])
#prende i valori solo dell'anno sullo slider ed elimina valori mancanti

if not df_anno_filtrato.empty:
    lista_gas = sorted(df_anno_filtrato['inquinante'].unique()) #unique salva solo un elemento
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
    with st.expander("L'inquinamento è diminuito?"):
        st.write("Possiamo osservare che l'inquinamento è diminuito, praticamente ogni gas alla fine del 2025 ha meno valore del 2016.")
    with st.expander("Ci sono anni con valori anomali?"):
        st.write("Non abbiamo visto nessun valore che si può definire 'anomalo' in questo grafico, ogni gas aumenta o diminuisce il suo valore con un picco o diminuzione alla fine di ogni anno, prevedibilmente.")
        
#Terzo grafico

st.divider()
st.subheader(":red[Qualità dell'aria media per Stazione 2016-2025]")


df_info_stazioni = pd.DataFrame(stazioni)[['id', 'nome']]

df_aria_nomi = pd.merge(df_aria, df_info_stazioni, left_on='stazione_id',right_on='id') #merge= unire due dataframe tramite una variabile
#unisce i due database


lista_gas_totali = sorted(df_aria_nomi['inquinante'].unique())
gas_confronto = st.selectbox("Seleziona l'inquinante per il confronto tra stazioni:", lista_gas_totali)

df_confronto = df_aria_nomi[df_aria_nomi['inquinante'] == gas_confronto]
 

df_medie_stazioni = df_confronto.groupby('nome')['valore'].mean().sort_values(ascending=False).reset_index()

if not df_medie_stazioni.empty:
    fig_staz, ax_staz = plt.subplots(figsize=(12, 8))
    
    
    sns.barplot(
        data=df_medie_stazioni, 
        y='nome', 
        x='valore', 
        palette='mako', 
        ax=ax_staz
    )

    ax_staz.set_title(f"Classifica stazioni per media decennale di {gas_confronto}", fontsize=15)
    ax_staz.set_xlabel("Valore medio (µg/m³)")
    ax_staz.set_ylabel("Stazione")
    ax_staz.grid(True, alpha=0.2, axis='x')
    
    
    st.pyplot(fig_staz, width="content")

    top_5_stazioni = df_aria_nomi['nome'].value_counts().head(5).reset_index()
    top_5_stazioni.columns = ['Nome', 'Conteggio']

    st.write("Le 5 stazioni con più rilevazioni:")
    st.table(top_5_stazioni)
    



#Quarto grafico

st.divider()

df_info_stazioni = pd.DataFrame(stazioni)[['id', 'nome']]
df_info_stazioni['id'] = df_info_stazioni['id'].astype(str)


df_aria_merge = df_aria.copy()
df_aria_merge['stazione_id'] = df_aria_merge['stazione_id'].astype(str)


df_totale = pd.merge(df_aria_merge, df_info_stazioni, left_on='stazione_id', right_on='id')


anno_recente = int(df_totale['anno'].max())
st.subheader(f":red[{anno_recente}: Andamento mensile per Stazione]")

df_focus = df_totale[df_totale['anno'] == anno_recente].copy()

if not df_focus.empty:
    col1, col2 = st.columns(2)
    
    with col1:
       
        stazione_scelta = st.selectbox("Seleziona la Stazione:", sorted(df_focus['nome'].unique()), key="f_staz")
    
    with col2:
       
        gas_per_stazione = sorted(df_focus[df_focus['nome'] == stazione_scelta]['inquinante'].unique())
        gas_scelto = st.selectbox("Inquinante:", gas_per_stazione, key="f_gas")

  
    df_plot_focus = df_focus[(df_focus['nome'] == stazione_scelta) & (df_focus['inquinante'] == gas_scelto)]
    
    df_mensile_focus = df_plot_focus.groupby('mese')['valore'].mean().reset_index()

    if not df_mensile_focus.empty:
        fig_f, ax_f = plt.subplots(figsize=(10, 4))
        
      
        sns.lineplot(data=df_mensile_focus, 
                     x='mese', 
                     y='valore', 
                     marker='o',
                     linewidth=5,
                     markersize=8, 
                     color="#0B0199", 
                     ax=ax_f)
        
        picco = df_mensile_focus.loc[df_mensile_focus['valore'].idxmax()]

        ax_f.plot(picco['mese'], picco['valore'], 'o', color='blue', markersize=7)
   
        ax_f.set_xticks(range(1, 13))
        ax_f.set_xticklabels(['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'])
        ax_f.set_title(f"{gas_scelto} a {stazione_scelta} - Media Mensile {anno_recente}")
        ax_f.grid(True, alpha=0.15, linestyle='--')
        ax_f.set_ylabel("Valore")
        ax_f.set_xlabel("Mese")
        
        st.pyplot(fig_f, width="content")
        with st.expander("L'andamento è regolare?"):
            st.write("L'andamento in gas diversi è differente come si può immaginare, ma l'andamento di un gas in diverse stazioni è pressochè lo stesso, con un po di variazioni, questo ci può dire che c'è un buon funzionamento delle stazioni, in quanto le misurazioni sono coerenti tra loro.")
    else:
        st.info("Nessun dato valido per generare la linea (controlla la colonna 'valore').")
        

