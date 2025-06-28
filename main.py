import pandas as pd
import streamlit as st
from streamlit import table


#obbiettivi
# poter filtrare i film
# avere una lista guradabile
# farla in maniera veloce
#devo fare web scraping?


def extract_names(col_index: int, start: int, end: int):
    # Inserisci qui il link CSV pubblico esatto del foglio 2, l'ho fatto cliccando su file e poi pubblica usl web
    url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRAY3JYbC7JCueZOQdmGdG3mj0aCiUVxTbWC3-ROJODXv28QPhlLBte6gA_L5cWCv8XRlBcESGvPPFc/pub?gid=769724799&single=true&output=csv"

    # Leggi il CSV in un DataFrame pandas
    df = pd.read_csv(url_csv)

    generi = df.iloc[start:end, col_index].dropna().unique() # con questo prendo le righe B3:33 della pagina però la funzione è generalizzata, fare la chiamata giusta

    # Ordina i generi in ordine alfabetico e restituisci la lista
    return sorted(generi)


def get_data():
    #url della tabella
    # url = "https://docs.google.com/spreadsheets/d/1R_wfR8PVKebj4JRLWbJeeTo_7_3_lfS-i0wCZR2ILnU/edit?gid=0#gid=0" // questo è senza la visione in webscraping
    url = "https://docs.google.com/spreadsheets/d/1R_wfR8PVKebj4JRLWbJeeTo_7_3_lfS-i0wCZR2ILnU/htmlview?gid=0#gid=0"
    #lettura della tabella
    tables = pd.read_html(url, encoding="utf-8")
    #rimozione prime sette righe
    tabelle = tables[0].iloc[2:].reset_index(drop=True) #elimino le prime due righe in modo da far leggere dalla seconda in poi
    #aggiornamento nomi colonne
    tabelle.columns = tabelle.iloc[0]             # imposti la prima riga per i nomi delle colonne
    tabelle = tabelle[1:].reset_index(drop=True)           # rimuovi di nuovo la riga ora divenuta intestazione

    #RIMOZIONE COLONNE SUPERFLUE
    ##tables = tables.drop(columns="Voto") // con questa elimino la colonna voto
    tabelle = tabelle.drop(columns=3) #esiste un dato rumoroso che si chiama 3 è l'ho eliminato
    ## print(tables.columns) //stampa array con tutti i nomi delle colonne

    #rimozione valori nulli
    tabelle = tabelle.dropna()

    #estraiamo i generi
    generi = extract_names(col_index=1, start=2, end=33)
    categorie = extract_names(col_index=2, start=2, end=35)

    return tabelle, generi, categorie


def search_filter(cell, values):
    if not values or values[0] is None:
        return True  # è stata fatta per permettere un sottoinsieme di filtri, se no l'utente è obbligato a selezionare più valori


if __name__ == "__main__":
    st.title(" Lorenzo Crescitelli's reviews")

    tabelle, generi, categorie = get_data()

    #filtro per genere
    st.header("Genere(i)")
    generi = st.pills("Genere(i)", generi, selection_mode="multi",label_visibility="hidden")
    #filtro per categorie
    st.header("Categorie")
    categorie = st.pills("Genere(i)", categorie, selection_mode="multi", label_visibility="hidden")
    #filtro per stato


    ###riprendere da 43:20
