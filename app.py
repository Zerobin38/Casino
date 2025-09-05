import streamlit as st
from roulette_core import simulate_strategy, stats_from_history, append_history_from_list
from ocr_reader import parse_image_with_ocr
import json, os

st.set_page_config(page_title="Roulette Analyzer", layout="wide", page_icon="🎯")
st.title("Roulette Analyzer — Photo → Stats → Simulation")

st.markdown("""
Prends une photo de la table/historique ou téléverse une image. \
L'app extrait les numéros, met à jour l'historique et te permet de simuler des stratégies.
""")

# -- Upload / Camera
st.header("1) Prendre une photo ou téléverser")
img = st.camera_input("Prendre une photo (mobile)")  # supported on mobile
img_file = st.file_uploader("Ou téléverser une image", type=["png","jpg","jpeg"])

image = img or img_file

if image:
    with st.spinner("Extraction OCR en cours…"):
        extracted = parse_image_with_ocr(image)  # returns list of ints (most recent first)
    st.success(f"Extraction: {len(extracted)} numéros récupérés")
    st.write(extracted)
    # Save into local history file
    os.makedirs("data", exist_ok=True)
    hist_file = "data/history.json"
    if os.path.exists(hist_file):
        with open(hist_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []
    # append extracted (assume newest first in image)
    history = append_history_from_list(history, extracted)
    with open(hist_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    st.info(f"Histoire sauvegardée ({len(history)} derniers numéros).")

# -- Manual import
st.header("2) Importer / Voir l'historique")
if st.button("Charger l'historique local"):
    hist_file = "data/history.json"
    if os.path.exists(hist_file):
        with open(hist_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        st.write(history[:200])
    else:
        st.warning("Aucun historique trouvé. Prends une photo ou téléverse une image d'abord.")

# -- Stats & Simulation
st.header("3) Statistiques et simulation")
if os.path.exists("data/history.json"):
    with open("data/history.json", "r", encoding="utf-8") as f:
        history = json.load(f)
    stats = stats_from_history(history)
    st.subheader("Statistiques rapides")
    st.write(stats)
    st.subheader("Simuler une stratégie")
    strategy = st.selectbox("Choisir une stratégie", ["Martingale (sur couleur)", "Fibonacci (sur couleur)", "Flat bet"])
    initial_bank = st.number_input("Bankroll (€)", 100.0)
    base_bet = st.number_input("Mise de base (€)", 1.0)
    n_rounds = st.number_input("Nombre de tours simulés", 100, min_value=1, max_value=10000)
    if st.button("Lancer simulation"):
        with st.spinner("Simulation en cours…"):
            sim = simulate_strategy(strategy, history, n_rounds=int(n_rounds), bank=initial_bank, base_bet=base_bet)
        st.subheader("Résultats simulation")
        st.write(sim)
        st.line_chart(sim["bank_history"])
else:
    st.info("Aucun historique — prends une photo d'un tableau de roulette pour commencer.")
