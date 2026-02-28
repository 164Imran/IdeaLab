import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION CONNEXION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # Lit les données de la feuille "Sheet1" (ou le nom de ton onglet)
    return conn.read(worksheet="Feuille 1", ttl="0s")

def save_data(df):
    # Met à jour la feuille avec le nouveau DataFrame
    conn.update(worksheet="Feuille 1", data=df)
    st.cache_data.clear()

# --- CHARGEMENT ---
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
