import streamlit as st

st.set_page_config(page_title="Skrining Kejang Anak", layout="centered")

st.title("🧠 Aplikasi Skrining Serangan Kejang Anak")

st.write("Jawab pertanyaan berikut dengan **Ya** atau **Tidak**")

def yn(question):
    return st.radio(question, ["Tidak", "Ya"], horizontal=True)

# =====================
# PERTANYAAN 1–6
# =====================
st.header("Pertanyaan 1 – 6")

q1 = yn("1. Apakah serangan terjadi tiba-tiba/mendadak?")
q2a = yn("2.a Apakah serangan terjadi saat tidur?")
q2b = yn("2.b Apakah serangan terjadi saat sedang beraktivitas/bermain?")
q3 = yn("3. Saat serangan anak tidak berespons dan serangan tidak berhenti saat dipegang?")
q4a = yn("4.a Pasca serangan: Anak tidak dapat mengingat kejadian?")
q4b = yn("4.b Pasca serangan: Anak tampak kebingungan?")
q4c = yn("4.c Pasca serangan: Anak tampak lemas/mengantuk/tidur?")
q5 = yn("5. Serangan berulang dengan pola yang sama tanpa jeda?")
q6a = yn("6.a Durasi serangan < 2 menit?")
q6b = yn("6.b Durasi serangan ≥ 2 menit?")

def conv(x):
    return 1 if x == "Ya" else 0

q1, q2a, q2b, q3, q4a, q4b, q4c, q5, q6a, q6b = map(conv, 
    [q1,q2a,q2b,q3,q4a,q4b,q4c,q5,q6a,q6b])

score_1_6 = q1 + q2a + q2b + q3 + q4a + q4b + q4c + q5 + q6a + q6b

kemungkinan_kejang = (
    score_1_6 >= 6 and
    q1 == 1 and q2a == 1 and
    q2b == 1 and q3 == 1 and q5 == 1 and
    q4a == 1 and q4b == 1 and q4c == 1 and
    (q6a == 1 or q6b == 1)
)

bukan_kejang = (
    score_1_6 < 6 or
    (q2a == 0 and q3 == 0 and q4a == 0 and q4b == 0 and q4c == 0 and q6a == 0)
)

# =====================
# OUTPUT AWAL
# =====================
if bukan_kejang:
    st.error("❌ Diagnosis: **Bukan serangan kejang**")

elif kemungkinan_kejang:
    st.success("⚠️ Kemungkinan serangan kejang")
    st.header("Pertanyaan 7")

    q7a = yn("7.a Dipicu oleh emosi/aktivitas/lingkungan?")
    q7b = yn("7.b Dipicu oleh demam/muntah/dehidrasi/cedera kepala?")

    q7a = 1 if q7a == "Tidak" else 0
    q7b = 1 if q7b == "Tidak" else 0
    score_7 = q7a + q7b

    if q7a == 1 and q7b == 1:
        st.success("Diagnosis: **Kejang tanpa provokasi (kejang spontan)**")

        # =====================
        # PERTANYAAN 8
        # =====================
        st.header("Pertanyaan 8")
        q8a = yn("8.a Apakah serangan terjadi satu kali?")
        q8b = yn("8.b Apakah serangan terjadi lebih dari satu kali?")

        q8a = conv(q8a)
        q8b = conv(q8b)

        if q8b == 1:
            q8c = yn("8.c Apakah interval antar serangan > 24 jam?")
            q8c = conv(q8c)
        else:
            q8c = 0

        if q8a == 1 and q8b == 0 and q8c == 0:
            st.success("Diagnosis: **First Unprovoked Seizure (FUS)**")

        elif q8a == 1 and q8b == 1:
            st.success("Diagnosis: **Kemungkinan Epilepsi**")

        total_score = score_1_6 + score_7 + q8a + q8b + q8c

        # =====================
        # LANJUT KE 9 & 10
        # =====================
        if total_score == 10:
            st.header("Pertanyaan 9 (Kejang Fokal)")
            q9a = yn("9.a Serangan pada satu sisi tubuh?")
            q9b = yn("9.b Kepala/wajah/mata miring ke satu sisi?")
            q9d = yn("9.d Dimulai satu sisi lalu menjadi kedua sisi?")

            q9c = st.multiselect("9.c Aura sebelum serangan:",
                ["Perubahan perilaku", "Mual-muntah", "Nyeri ulu hati",
                 "Penciuman/pengecapan aneh",
                 "Gangguan penglihatan"])

            q9a, q9b, q9d = map(conv, [q9a,q9b,q9d])

            if q9a == 1 and q9b == 1 and len(q9c) > 0:
                diagnosis = "Kejang Fokal"
                if q9d == 1:
                    diagnosis = "Kejang focal to bilateral tonic clonic"
                st.success(f"Diagnosis: **{diagnosis}**")

            st.header("Pertanyaan 10 (Kejang Umum)")
            q10a = yn("10.a Serangan pada kedua sisi tubuh?")
            q10b = yn("10.b Pasca serangan anak mengompol?")
            q10c = yn("10.c Wajah membiru / mulut mengunci / mata deviasi?")

            q10a = conv(q10a)

            if q10a == 1:
                st.success("Diagnosis: **Kejang Umum**")

    elif q7a == 0 and q7b == 1:
        st.warning("Diagnosis: **Pencetus paroksismal non-epilepsi**")

    elif q7a == 1 and q7b == 0:
        st.warning("Diagnosis: **Kemungkinan kejang simptomatik akut**")
