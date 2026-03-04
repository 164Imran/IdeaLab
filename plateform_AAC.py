import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image

# Charger l'image avec PIL (pour éviter les erreurs de format)
img = Image.open("logo_AAC.png")
# Initialisation de la connexion unique
conn = st.connection("gsheets", type=GSheetsConnection)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(img, use_container_width=True)
# --- FONCTIONS DE DONNÉES ---

def get_data(sheet_name):
    return conn.read(worksheet=sheet_name, ttl="0s")

def save_data(sheet_name, df):
    conn.update(worksheet=sheet_name, data=df)
    st.cache_data.clear()

def add_to_members(name, role, project):
    df_members = get_data("Membres")
    new_member = pd.DataFrame([{
        "Nom": name,
        "Role": role,           
        "Projet_Associe": project,
        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    }])
    updated_df = pd.concat([df_members, new_member], ignore_index=True)
    save_data("Membres", updated_df)

# --- INTERFACE UTILISATEUR ---

st.title("IdeaLab - Plateforme Collaborative")

# Chargement des idées
df_idees = get_data("Idees")

# Formulaire d'ajout
with st.expander("Soumettre une nouvelle idée"):
    with st.form("new_idea_form"):
        nom_utilisateur = st.text_input("Votre Nom")
        titre = st.text_input("Titre du projet")
        description = st.text_area("Description")
        
        submit = st.form_submit_button("Publier")

        if submit and titre and nom_utilisateur:
            # 1. Enregistrement de l'idée
            new_id = int(df_idees["ID"].max() + 1) if not df_idees.empty else 1
            new_idea_row = pd.DataFrame([{
                "ID": new_id, "Titre": titre, "Description": description, 
                "Votes": 0, "Auteur": nom_utilisateur
            }])
            save_data("Idees", pd.concat([df_idees, new_idea_row], ignore_index=True))
            
            # 2. Enregistrement automatique du membre (Rôle: Créateur)
            add_to_members(nom_utilisateur, "Créateur", titre)
            
            st.success("Idée publiée et profil membre créé !")
            st.rerun()

# Affichage et Votes
for index, row in df_idees.iterrows():
    st.write(f"### {row['Titre']} (par {row['Auteur']})")
    st.info(row['Description'])
    
    col1, col2 = st.columns([1, 3])
    with col1:
        voter_name = st.text_input("Ton nom pour voter", key=f"voter_{index}")
        if st.button(f"Voter ({row['Votes']})", key=f"btn_{index}"):
            if voter_name:
                # Mise à jour du score
                df_idees.at[index, 'Votes'] = int(row['Votes']) + 1
                save_data("Idees", df_idees)
                
                # Ajout du votant à la liste des membres (Rôle: Votant)
                add_to_members(voter_name, "Votant", row['Titre'])
                
                st.rerun()
            else:
                st.warning("Saisis ton nom pour voter.")