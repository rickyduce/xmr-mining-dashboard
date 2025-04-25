# Monero Mining Dashboard - Streamlit App
import streamlit as st
import requests

st.set_page_config(page_title="Monero Mining Dashboard", layout="centered")

WALLET = "442Ukh1NBsiTJboCzH5VbCuvCj5hsh1QQJAx3m5m5dxLgEAKdU7owzr2cT8rp8ududsQ8vaCHcRdFQ4JGJpyoPwpkmBsGe8"
API_URL = f"https://supportxmr.com/api/miner/{WALLET}/stats"

st.title("XMR Mining Dashboard")
st.markdown("Suivi temps réel des performances de minage Monero (XMR)")

@st.cache_data(ttl=300)
def fetch_data():
    res = requests.get(API_URL)
    return res.json() if res.status_code == 200 else None

data = fetch_data()

if data:
    hashrate = data.get("hash", 0)
    total_paid = float(data.get("paid", 0)) / 1e12
    total_due = float(data.get("due", 0)) / 1e12

    st.metric("Hashrate actuel", f"{hashrate/1000:.2f} KH/s")
    st.metric("XMR total payé", f"{total_paid:.5f} XMR")
    st.metric("XMR en attente", f"{total_due:.5f} XMR")

    st.progress(min(hashrate / 100000, 1.0))
else:
    st.error("Impossible de récupérer les données. Vérifie la connexion Internet ou l'adresse Monero.")

st.caption("Mise à jour automatique toutes les 5 minutes")
