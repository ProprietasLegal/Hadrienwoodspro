import streamlit as st
import pandas as pd
import io
from datetime import date

st.set_page_config(page_title="Hadrien Golf Pro Stats", layout="wide")
st.title("🏌️ Hadrien Golf Pro Stats")

st.markdown("## 📝 Fiche de compétition")

# Formulaire fiche compétition
with st.form("competition_form"):
    col1, col2 = st.columns(2)

    with col1:
        competition_name = st.text_input("Nom de la compétition")
        competition_type = st.text_input("Type de compétition")
        organiser = st.text_input("Compétition organisée par")
        competition_date = st.date_input("Date de la compétition", value=date.today())
        location = st.text_input("Lieu")
        course_name = st.text_input("Nom du parcours")
        par = st.text_input("Par (ex: 72)")
        length = st.text_input("Longueur (m)")
        tee_time = st.time_input("Heure départ")
        play_with = st.text_input("Jouer avec")
        participants = st.number_input("Nombre de participants", step=1)
        tee_start = st.text_input("Départ des boules")
        course_condition = st.text_input("État du parcours")
        weather = st.text_input("Météo")
        place_ball = st.radio("Placer la balle ?", options=["oui", "non"])
        balls_used = st.text_input("Balles utilisées (facultatif)")

    with col2:
        target_score = st.number_input("Objectif de score", step=1)
        final_score = st.number_input("Score final", step=1)
        target_handicap = st.text_input("Objectif handicap")
        hcp_before = st.text_input("Handicap avant compétition")
        hcp_after = st.text_input("Handicap après compétition")
        target_putts = st.number_input("Objectif nombre de putts", step=1)
        putts_done = st.number_input("Nombre de putts", step=1)
        target_appputt = st.text_input("Objectif approche/putt (%)")
        real_appputt = st.text_input("Approche/putt réel (%)")
        target_gir = st.text_input("Objectif greens en régulation (/18 et %)")
        real_gir = st.text_input("Greens en rég. (/18 et %)")
        target_fairway = st.text_input("Objectif fairways en rég.")
        real_fairway = st.text_input("Fairway en rég.")
        other_goals = st.text_area("Objectif(s) autres avant compétition")
        achieved_goals = st.text_area("Objectif(s) réussis après compétition")

    submitted = st.form_submit_button("Valider la fiche compétition")

st.markdown("---")
st.subheader("🕳️ Encodage Scorecard trou par trou")

if "scorecard" not in st.session_state:
    st.session_state.scorecard = pd.DataFrame([{
        "Trou": i + 1, "Par": "", "Coups": "", "Putts": "", "Club 1": "", "Club 2": ""
    } for i in range(18)])

scorecard_df = st.data_editor(
    st.session_state.scorecard,
    num_rows="fixed",
    use_container_width=True
)
st.session_state.scorecard = scorecard_df

st.markdown("---")
st.subheader("📊 Statistiques")

if scorecard_df["Coups"].apply(lambda x: str(x).isdigit()).any():
    scorecard_df["Coups"] = pd.to_numeric(scorecard_df["Coups"], errors="coerce")
    scorecard_df["Putts"] = pd.to_numeric(scorecard_df["Putts"], errors="coerce")
    total_strokes = int(scorecard_df["Coups"].sum(skipna=True))
    avg_putts = round(scorecard_df["Putts"].mean(skipna=True), 2)
    st.write("**Total de coups :**", total_strokes)
    st.write("**Putts moyens par trou :**", avg_putts)
    st.write("**Score brut :**", total_strokes)

st.markdown("---")
st.subheader("📤 Exporter les données")

if st.button("📥 Télécharger le fichier Excel"):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        # Fiche compétition
        fiche_data = {
            "Nom compétition": competition_name,
            "Type": competition_type,
            "Organisateur": organiser,
            "Date": competition_date,
            "Lieu": location,
            "Parcours": course_name,
            "Par": par,
            "Longueur": length,
            "Départ": tee_time,
            "Joueurs": play_with,
            "Participants": participants,
            "Départ boules": tee_start,
            "État": course_condition,
            "Météo": weather,
            "Balle placée": place_ball,
            "Balles": balls_used,
            "Objectif score": target_score,
            "Score final": final_score,
            "Objectif hcp": target_handicap,
            "HCP avant": hcp_before,
            "HCP après": hcp_after,
            "Objectif putts": target_putts,
            "Putts faits": putts_done,
            "Objectif app/putt": target_appputt,
            "App/putt réel": real_appputt,
            "Objectif GIR": target_gir,
            "GIR réel": real_gir,
            "Objectif fairway": target_fairway,
            "Fairway réel": real_fairway,
            "Autres objectifs": other_goals,
            "Objectifs réussis": achieved_goals
        }
        pd.DataFrame(list(fiche_data.items()), columns=["Champ", "Valeur"]).to_excel(writer, sheet_name="Fiche Compétition", index=False)
        scorecard_df.to_excel(writer, sheet_name="Scorecard", index=False)

    st.download_button(
        label="📄 Télécharger le fichier Excel complet",
        data=buffer.getvalue(),
        file_name="hadrien_golf_pro_stats.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
