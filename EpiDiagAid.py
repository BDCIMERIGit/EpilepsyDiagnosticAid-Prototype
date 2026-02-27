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
# FUNCTIONS
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

    q1 = yn("1. Apakah serangan terjadi tiba-tiba?")
    q2a = yn("2.a Saat tidur?")
    q2b = yn("2.b Saat beraktivitas?")
    q3 = yn("3. Tidak berespons saat serangan?")
    q4a = yn("4.a Tidak ingat kejadian?")
    q4b = yn("4.b Tampak kebingungan?")
    q4c = yn("4.c Lemas/mengantuk?")
    q5 = yn("5. Berulang dengan pola sama?")
    q6a = yn("6.a < 2 menit?")
    q6b = yn("6.b ≥ 2 menit?")

    if st.button("Proses Diagnosis Awal"):

        values = list(map(conv,[q1,q2a,q2b,q3,q4a,q4b,q4c,q5,q6a,q6b]))
        score = sum(values)

        if score >= 6:
            diagnosis_awal = "Kemungkinan Serangan Kejang"
        else:
            diagnosis_awal = "Bukan Kejang"

        st.session_state.diagnosis_awal = diagnosis_awal
        st.session_state.step = 2
        st.rerun()

# =====================================================
# STEP 2 — HASIL AWAL + PERTANYAAN 7
# =====================================================
elif st.session_state.step == 2:

    st.success(f"Diagnosis Awal adalah: **{st.session_state.diagnosis_awal}**")

    if st.session_state.diagnosis_awal == "Bukan Kejang":
        st.session_state.step = 6
        st.rerun()

    st.header("Pertanyaan 7")

    q7a = yn("7.a Dipicu emosi/aktivitas?")
    q7b = yn("7.b Dipicu demam/cedera kepala?")

    if st.button("Proses Lanjutan"):

        q7a = 1 if q7a == "Tidak" else 0
        q7b = 1 if q7b == "Tidak" else 0

        if q7a == 1 and q7b == 1:
            diagnosis_lanjutan = "Kejang tanpa provokasi"
        elif q7a == 0 and q7b == 1:
            diagnosis_lanjutan = "Pencetus paroksismal non-epilepsi"
        elif q7a == 1 and q7b == 0:
            diagnosis_lanjutan = "Kejang simptomatik akut"
        else:
            diagnosis_lanjutan = "Perlu evaluasi lanjut"

        st.session_state.diagnosis_lanjutan = diagnosis_lanjutan
        st.session_state.step = 3
        st.rerun()

# =====================================================
# STEP 3 — PERTANYAAN 8 (SESUAI RULE RESMI)
# =====================================================
if st.session_state.step == 3:

    st.subheader("Pertanyaan 8")

    # =========================
    # 8.a
    # =========================
    q8a = st.radio(
        "8.a. Apakah kejang tanpa demam?",
        ["Belum dijawab", "Ya", "Tidak"],
        key="q8a"
    )

    # =========================
    # 8.b (muncul jika 8.a = Ya)
    # =========================
    if q8a == "Ya":
        q8b = st.radio(
            "8.b. Apakah kejang terjadi ≥2 kali dalam 24 jam?",
            ["Belum dijawab", "Ya", "Tidak"],
            key="q8b"
        )
    else:
        st.session_state.q8b = "Belum dijawab"

    # =========================
    # 8.c (muncul jika 8.b = Ya)
    # =========================
    if q8a == "Ya" and st.session_state.q8b == "Ya":
        q8c = st.radio(
            "8.c. Apakah kejang tidak diprovokasi?",
            ["Belum dijawab", "Ya", "Tidak"],
            key="q8c"
        )
    else:
        st.session_state.q8c = "Belum dijawab"

    st.markdown("---")

    # =========================
    # TOMBOL SELALU MUNCUL
    # =========================
    if st.button("Proses Pertanyaan 8"):

        # Validasi lengkap dulu
        if st.session_state.q8a == "Belum dijawab":
            st.warning("Pertanyaan 8.a belum dijawab")
            st.stop()

        if st.session_state.q8a == "Ya" and st.session_state.q8b == "Belum dijawab":
            st.warning("Pertanyaan 8.b belum dijawab")
            st.stop()

        if (
            st.session_state.q8a == "Ya"
            and st.session_state.q8b == "Ya"
            and st.session_state.q8c == "Belum dijawab"
        ):
            st.warning("Pertanyaan 8.c belum dijawab")
            st.stop()

        # =========================
        # SCORING
        # =========================
        skor8a = 1 if st.session_state.q8a == "Ya" else 0
        skor8b = 1 if st.session_state.q8b == "Ya" else 0
        skor8c = 1 if st.session_state.q8c == "Ya" else 0

        # =========================
        # RULE DIAGNOSIS
        # =========================
        if skor8a == 1 and skor8b == 0 and skor8c == 0:
            hasil8 = "First Unprovoked Seizure (FUS)"
            next_step = 6

        elif skor8a == 1 and skor8b == 1:
            hasil8 = "Kemungkinan mengalami epilepsi"
            next_step = 4

        else:
            hasil8 = "Tidak memenuhi kriteria"
            next_step = 6

        st.session_state.hasil8 = hasil8
        st.session_state.step = next_step
        st.rerun()
# =====================================================
# STEP 4 — PERTANYAAN 9
# =====================================================
elif st.session_state.step == 4:

    st.success(f"Hasil Pertanyaan 8 adalah: **{st.session_state.hasil8}**")

    if st.session_state.hasil8 != "Kemungkinan Epilepsi":
        st.session_state.step = 6
        st.rerun()

    st.header("Pertanyaan 9")

    q9a = yn("9.a Satu sisi tubuh?")
    q9b = yn("9.b Deviasi kepala/mata?")
    q9d = yn("9.d Menjadi kedua sisi?")

    if st.button("Proses Pertanyaan 9"):

        q9a,q9b,q9d = map(conv,[q9a,q9b,q9d])

        if q9a and q9b:
            tipe9 = "Kejang Fokal"
            if q9d:
                tipe9 = "Focal to Bilateral Tonic Clonic"
        else:
            tipe9 = "Tidak memenuhi kriteria kejang fokal"

        st.session_state.tipe9 = tipe9
        st.session_state.step = 5
        st.rerun()

# =====================================================
# STEP 5 — PERTANYAAN 10 (KEJANG UMUM SESUAI RULE AWAL)
# =====================================================
elif st.session_state.step == 5:

    st.success(f"Hasil Pertanyaan 9 adalah: **{st.session_state.tipe9}**")

    st.header("Pertanyaan 10 (Kejang Umum)")

    q10a = yn("10.a Apakah serangan terjadi pada kedua sisi tubuh?")
    q10b = yn("10.b Apakah pasca serangan anak mengompol?")
    q10c = yn("""10.c Apakah saat serangan terjadi:
- Wajah dan bibir membiru?
- Mulut mengunci?
- Kedua mata berdeviasi ke atas?
""")

    if st.button("Proses Pertanyaan 10"):

        q10a, q10b, q10c = map(conv, [q10a, q10b, q10c])

        # =========================
        # RULE SESUAI PERMINTAAN
        # =========================
        if q10a == 1:
            tipe10 = "Kejang Umum"
        else:
            tipe10 = "Tidak memenuhi kriteria Kejang Umum"

        st.session_state.tipe10 = tipe10
        st.session_state.step = 6
        st.rerun()

# =====================================================
# STEP 6 — HASIL AKHIR + SIMPAN RIWAYAT
# =====================================================
elif st.session_state.step == 6:

    st.success("📋 HASIL AKHIR DIAGNOSIS")

    diagnosis_final = {
        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": st.session_state.username,
        "Diagnosis Awal": st.session_state.get("diagnosis_awal",""),
        "Diagnosis Lanjutan": st.session_state.get("diagnosis_lanjutan",""),
        "Hasil 8": st.session_state.get("hasil8",""),
        "Tipe Fokal": st.session_state.get("tipe9",""),
        "Tipe Umum": st.session_state.get("tipe10","")
    }

    st.write(diagnosis_final)

    if st.button("Simpan ke Riwayat"):
        st.session_state.history.append(diagnosis_final)
        st.success("Berhasil disimpan")

# =====================================================
# RIWAYAT DIAGNOSIS
# =====================================================
if st.session_state.history:

    st.divider()
    st.header("📁 Riwayat Diagnosis")

    df_history = pd.DataFrame(st.session_state.history)
    df_user = df_history[df_history["User"] == st.session_state.username]

    st.dataframe(df_user, use_container_width=True)

    csv = df_user.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Riwayat (CSV)",
        data=csv,
        file_name="riwayat_diagnosis.csv",
        mime="text/csv"
    )
