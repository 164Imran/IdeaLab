import streamlit as st
import pandas as pd
import os
from PIL import Image


# Configuration de la page
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("logo_AAC.png", use_container_width=True)

st.markdown(
    """
    <style>
    /* Fond sombre avec halo lumineux jaune en haut à droite */
    [data-testid="stAppViewContainer"] {
        background-color: #050505 !important;
        background-image: 
            radial-gradient(at 80% 20%, rgba(255, 238, 88, 0.15) 0px, transparent 50%),
            radial-gradient(at 20% 80%, rgba(255, 238, 88, 0.05) 0px, transparent 50%) !important;
    }

    /* Effet de verre (Glassmorphism) pour les cartes de projets */
    div[data-testid="stExpander"], div.stButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Bouton de vote stylisé */
    .stButton > button {
        border: 1px solid #FFEE58 !important;
        color: #FFEE58 !important;
    }
    
    .stButton > button:hover {
        background: #FFEE58 !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.set_page_config(page_title="IA Asso - Projets", page_icon="petitlogo.png",layout="centered")
st.title("💡 Lab d'idées IA - CY Tech")
# Gestion de la base de données (CSV)
DB_FILE = "projets_asso.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "Titre", "Description", "Votes"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

data = load_data()

# --- SECTION 1 : Proposer un projet ---
with st.expander("Soumettre une nouvelle idée"):
    with st.form("form_projet"):
        titre = st.text_input("Nom du projet")
        desc = st.text_area("Description courte (Objectif IA)")
        submit = st.form_submit_button("Envoyer")
        
        if submit and titre:
            new_id = len(data) + 1
            new_row = {"ID": new_id, "Titre": titre, "Description": desc, "Votes": 0}
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            save_data(data)
            st.success("Idée ajoutée !")

# --- SECTION 2 : Liste des projets et Votes ---
st.subheader("🚀 Projets en lice")

# Tri par votes décroissants
data = data.sort_values(by="Votes", ascending=False)

for index, row in data.iterrows():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"**{row['Titre']}**")
        st.caption(row['Description'])
    with col2:
        if st.button(f"▲ {row['Votes']}", key=f"vote_{row['ID']}"):
            data.at[index, 'Votes'] += 1
            save_data(data)
            st.rerun()
    st.divider()
