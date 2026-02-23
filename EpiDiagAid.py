import streamlit as st

st.set_page_config(page_title="Skrining Kejang Anak", layout="centered")
st.title("🧠 Aplikasi Skrining Serangan Kejang Anak")
st.write("Jawab pertanyaan berikut dengan **Ya** atau **Tidak**")

def yn(question):
    return st.radio(question, ["Tidak", "Ya"], horizontal=True)

def conv(x):
    return 1 if x == "Ya" else 0

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
q5 = yn("5. Serangan berulang dengan pola sama tanpa jeda?")
q6a = yn("6.a Durasi serangan < 2 menit?")
q6b = yn("6.b Durasi serangan ≥ 2 menit?")

q1,q2a,q2b,q3,q4a,q4b,q4c,q5,q6a,q6b = map(conv,
    [q1,q2a,q2b,q3,q4a,q4b,q4c,q5,q6a,q6b])

score_1_6 = q1 + q2a + q2b + q3 + q4a + q4b + q4c + q5 + q6a + q6b

bukan_kejang = score_1_6 < 6
kemungkinan_kejang = score_1_6 >= 6

diagnosis = None

# =====================
# OUTPUT AWAL
# =====================
if bukan_kejang:
    st.error("❌ Diagnosis: **Bukan Kejang**")

elif kemungkinan_kejang:
    st.success("⚠️ **Kemungkinan Serangan Kejang**")
    st.header("Pertanyaan 7")

    q7a = yn("7.a Dipicu oleh emosi/aktivitas/lingkungan?")
    q7b = yn("7.b Dipicu oleh demam/muntah/dehidrasi/cedera kepala?")

    q7a = 1 if q7a == "Tidak" else 0
    q7b = 1 if q7b == "Tidak" else 0

    if q7a == 1 and q7b == 1:
        diagnosis = "Kejang tanpa provokasi (kejang spontan)"
        st.success(f"Diagnosis: **{diagnosis}**")

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
            diagnosis = "First Unprovoked Seizure (FUS)"
            st.success(f"Diagnosis: **{diagnosis}**")

        elif q8a == 1 and q8b == 1:
            diagnosis = "Kemungkinan Epilepsi"
            st.success(f"Diagnosis: **{diagnosis}**")

        # =====================
        # LANJUT KE TIPE KEJANG (HANYA JIKA EPILEPSI)
        # =====================
        if diagnosis == "Kemungkinan Epilepsi":

            st.header("Pertanyaan 9 (Kejang Fokal)")

            q9a = yn("9.a Serangan pada satu sisi tubuh?")
            q9b = yn("9.b Kepala/wajah/mata miring ke satu sisi?")

            q9c = st.multiselect(
                "9.c Apakah ada gejala sebelum serangan?",
                ["Perubahan perilaku", "Mual-muntah", "Nyeri ulu hati",
                 "Penciuman/pengecapan aneh",
                 "Gangguan penglihatan"]
            )

            q9d = yn("9.d Dimulai satu sisi lalu menjadi kedua sisi?")

            q9a,q9b,q9d = map(conv,[q9a,q9b,q9d])

            if q9a == 1 and q9b == 1 and len(q9c) > 0:
                diagnosis_fokal = "Kejang Fokal"
                if q9d == 1:
                    diagnosis_fokal = "Kejang focal to bilateral tonic clonic"
                st.success(f"Diagnosis tipe kejang: **{diagnosis_fokal}**")

            st.header("Pertanyaan 10 (Kejang Umum)")

            q10a = yn("10.a Serangan pada kedua sisi tubuh?")
            q10b = yn("10.b Pasca serangan anak mengompol?")
            q10c = yn("10.c Wajah membiru / mulut mengunci / mata deviasi?")

            q10a = conv(q10a)

            if q10a == 1:
                st.success("Diagnosis tipe kejang: **Kejang Umum**")

    elif q7a == 0 and q7b == 1:
        diagnosis = "Pencetus paroksismal non-epilepsi"
        st.warning(f"Diagnosis: **{diagnosis}**")

    elif q7a == 1 and q7b == 0:
        diagnosis = "Kemungkinan kejang simptomatik akut"
        st.warning(f"Diagnosis: **{diagnosis}**")
