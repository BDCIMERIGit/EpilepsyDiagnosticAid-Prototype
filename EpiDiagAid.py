import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(page_title="Skrining Kejang Anak", layout="centered")

# =====================================================
# SESSION STATE INIT
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "step" not in st.session_state:
    st.session_state.step = 1

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# LOGIN SYSTEM
# =====================================================
USERS = {
    "profhandry": "123456",
    "doktervalerie": "123456"
}

if not st.session_state.logged_in:
    st.title("🔐 Login Sistem Skrining Kejang Anak")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username atau password salah")

    st.stop()

# =====================================================
# HEADER SETELAH LOGIN
# =====================================================
st.title("🧠 Aplikasi Skrining Serangan Kejang Anak")
st.write(f"Login sebagai: **{st.session_state.username}**")

col1, col2 = st.columns([1,1])

with col1:
    if st.button("🔄 Mulai Ulang"):
        st.session_state.step = 1
        st.rerun()

with col2:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.step = 1
        st.rerun()

st.divider()

# =====================================================
# FUNGSI BANTU
# =====================================================
def yn(question):
    return st.radio(question, ["Tidak", "Ya"], horizontal=True)

def conv(x):
    return 1 if x == "Ya" else 0

# =====================================================
# STEP 1 — PERTANYAAN 1–6
# =====================================================
if st.session_state.step == 1:

    st.header("Pertanyaan 1 – 6")

    q1 = yn("1. Apakah serangan terjadi tiba-tiba/mendadak?")
    q2a = yn("2.a Apakah serangan terjadi saat tidur?")
    q2b = yn("2.b Apakah serangan terjadi saat sedang beraktivitas/bermain?")
    q3 = yn("3. Saat serangan anak tidak berespons dan serangan tidak berhenti saat dipegang?")
    q4a = yn("4.a Pasca serangan: Anak tidak dapat mengingat kejadian?")
    q4b = yn("4.b Pasca serangan: Anak tampak kebingungan?")
    q4c = yn("4.c Pasca serangan: Anak tampak lemas/mengantuk/tidur?")
    q5 = yn("5. Serangan berulang dengan pola sama tanpa jeda?")
    q6a = yn("6.a Durasi serangan < 2 menit?")
    q6b = yn("6.b Durasi serangan ≥ 2 menit?")

    if st.button("Proses Diagnosis Awal"):

        values = list(map(conv, [q1,q2a,q2b,q3,q4a,q4b,q4c,q5,q6a,q6b]))
        score = sum(values)

        st.session_state.score = score
        st.session_state.step = 2
        st.rerun()

# =====================================================
# STEP 2 — PERTANYAAN 7
# =====================================================
elif st.session_state.step == 2:

    if st.session_state.score < 6:
        st.error("❌ Diagnosis: Bukan Kejang")
    else:
        st.success("⚠️ Kemungkinan Serangan Kejang")

        st.header("Pertanyaan 7")

        q7a = yn("7.a Dipicu oleh emosi/aktivitas/lingkungan?")
        q7b = yn("7.b Dipicu oleh demam/muntah/dehidrasi/cedera kepala?")

        if st.button("Proses Lanjutan"):

            st.session_state.q7a = q7a
            st.session_state.q7b = q7b
            st.session_state.step = 3
            st.rerun()

# =====================================================
# STEP 3 — PERTANYAAN 8–10 + HASIL
# =====================================================
elif st.session_state.step == 3:

    diagnosis_final = ""
    tipe_kejang = ""

    q7a = 1 if st.session_state.q7a == "Tidak" else 0
    q7b = 1 if st.session_state.q7b == "Tidak" else 0

    if q7a == 1 and q7b == 1:

        st.header("Pertanyaan 8")

        q8a = yn("8.a Apakah serangan terjadi satu kali?")
        q8b = yn("8.b Apakah serangan terjadi lebih dari satu kali?")

        q8a = conv(q8a)
        q8b = conv(q8b)

        if q8a == 1 and q8b == 0:
            diagnosis_final = "First Unprovoked Seizure (FUS)"

        elif q8b == 1:
            diagnosis_final = "Kemungkinan Epilepsi"

            st.header("Pertanyaan 9 (Kejang Fokal)")

            q9a = conv(yn("9.a Serangan pada satu sisi tubuh?"))
            q9b = conv(yn("9.b Kepala/wajah/mata miring ke satu sisi?"))
            q9d = conv(yn("9.d Dimulai satu sisi lalu menjadi kedua sisi?"))

            st.header("Pertanyaan 10 (Kejang Umum)")

            q10a = conv(yn("10.a Serangan pada kedua sisi tubuh?"))

            if q9a and q9b:
                tipe_kejang = "Kejang Fokal"
                if q9d:
                    tipe_kejang = "Focal to Bilateral Tonic Clonic"

            elif q10a:
                tipe_kejang = "Kejang Umum"

    elif q7a == 0 and q7b == 1:
        diagnosis_final = "Pencetus paroksismal non-epilepsi"

    elif q7a == 1 and q7b == 0:
        diagnosis_final = "Kejang simptomatik akut"

    # =========================
    # TAMPILKAN HASIL AKHIR
    # =========================
    st.divider()
    st.header("📋 HASIL DIAGNOSIS")

    st.success(f"Diagnosis Utama: **{diagnosis_final}**")

    if tipe_kejang:
        st.info(f"Tipe Kejang: **{tipe_kejang}**")

    # =========================
    # SIMPAN KE RIWAYAT
    # =========================
    data = {
        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": st.session_state.username,
        "Diagnosis": diagnosis_final,
        "Tipe Kejang": tipe_kejang
    }

    st.session_state.history.append(data)

    st.session_state.step = 4

# =====================================================
# STEP 4 — RIWAYAT
# =====================================================
if st.session_state.history:

    st.divider()
    st.header("📁 Riwayat Diagnosis")

    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history, use_container_width=True)

    csv = df_history.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Riwayat (CSV)",
        data=csv,
        file_name="riwayat_diagnosis.csv",
        mime="text/csv"
    )
