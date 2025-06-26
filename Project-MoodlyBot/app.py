import streamlit as st
import replicate
import os
from dotenv import load_dotenv

# Load token dari .env
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Konfigurasi halaman
st.set_page_config(page_title="MoodlyBot", page_icon="🤖")
st.title("🧠 MoodlyBot – Chatbot Emosi Berbasis AI")

# Kamus respon empatik
response_dict = {
    "Anger": "Kemarahan itu wajar, kamu ingin cerita lebih lanjut tentang apa yang membuatmu kesal?",
    "Sadness": "Sedih memang berat. Aku di sini mendengarkan, kamu tidak sendiri.",
    "Joy": "Senangnya dengar kamu merasa bahagia! Ada hal spesial terjadi hari ini?",
    "Fear": "Rasa takut kadang datang tiba-tiba. Ceritakan, aku di sini untuk bantu.",
    "Disgust": "Aku paham perasaan muak itu menyakitkan. Ada yang ingin kamu lepaskan?",
    "Surprise": "Wah! Sepertinya ada hal mengejutkan terjadi. Boleh cerita lebih lanjut?"
}

# Fungsi deteksi emosi
def detect_emotion(user_text):
    prompt = f"""Dari teks berikut, tentukan satu emosi utama: Anger, Sadness, Joy, Fear, Disgust, atau Surprise.
Jawab hanya nama emosinya. misal: Anger

Teks: "{user_text}"
Emosi:"""
    
    try:
        result = replicate.run(
            "ibm-granite/granite-3.3-8b-instruct",
            input={"prompt": prompt}
        )
        output = "".join(result).strip().lower()
        for emo in response_dict.keys():
            if emo.lower() in output:
                return emo
    except:
        return "Joy"  # fallback jika gagal

    return "Joy"

# Tampilan UI
user_input = st.text_area("📝 Ketik perasaanmu di sini:", placeholder="Contoh: Gue ngerasa sendirian banget akhir-akhir ini...")

if st.button("💬 Kirim"):
    if user_input:
        with st.spinner("MoodlyBot sedang memproses..."):
            emotion = detect_emotion(user_input)
            bot_reply = response_dict.get(emotion, "Aku di sini mendengarkan, kamu bisa cerita apa saja.")
            st.success(f"🧠 Emosi yang terdeteksi: **{emotion}**")
            st.markdown(f"**🤖 MoodlyBot:** {bot_reply}")
    else:
        st.warning("Tolong ketik sesuatu terlebih dahulu.")
