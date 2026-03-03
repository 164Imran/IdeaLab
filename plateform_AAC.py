import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Nettoyage de l'URL : s'arrêter après l'ID de la feuille
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1pD_AwECwHYoov2ZNOkZZnu64inOK3SsW9cU6tMI8anE"
# Vérifier exactement le nom sur l'onglet en bas de votre Google Sheet
SHEET_NAME = "Sheet1" 

conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # Suppression de ttl="0s" pour le premier test afin de valider la connexion
    return conn.read(spreadsheet=SPREADSHEET_URL, worksheet=SHEET_NAME)

def save_data(df):
    conn.update(spreadsheet=SPREADSHEET_URL, worksheet=SHEET_NAME, data=df)
    st.cache_data.clear()

data = load_data()

# --- SECTION AJOUT ---
with st.expander("Soumettre une nouvelle idée"):
    with st.form("form_projet"):
        titre = st.text_input("Nom du projet")
        desc = st.text_area("Description")
        submit = st.form_submit_button("Envoyer")
        
        if submit and titre:
            new_row = pd.DataFrame([{
                "ID": len(data) + 1,
                "Titre": titre,
                "Description": desc,
                "Votes": 0
            }])
            # Utilisation de pd.concat pour mettre à jour le DataFrame local
            updated_df = pd.concat([data, new_row], ignore_index=True)
            save_data(updated_df)
            st.success("Projet enregistré dans Google Sheets !")
            st.rerun()

# --- SECTION VOTES ---
for index, row in data.iterrows():
    col_a, col_b = st.columns([4, 1])
    with col_a:
        st.write(f"**{row['Titre']}**")
        st.caption(row['Description'])
    with col_b:
        if st.button(f"▲ {row['Votes']}", key=f"vote_{index}"):
            data.at[index, 'Votes'] = int(row['Votes']) + 1
            save_data(data)
            st.rerun()
