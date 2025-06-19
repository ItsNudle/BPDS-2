import streamlit as st
import pandas as pd
import joblib

# Konfigurasi halaman
st.set_page_config(page_title="Prediksi DropOut Mahasiswa", layout="centered")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("model.joblib")

model = load_model()

# --- Mapping label asli ---
marital_status_options = {
    "Single": 0,
    "Married": 1,
    "Divorced": 2,
    "Widower": 3,
    "Facto Union": 4,
    "Legally Seperated": 5
}

application_mode_options = {
    '1st Phase - General Contingent': 1,
    '2nd Phase - General Contingent': 17,
    '3rd Phase - General Contingent': 18,
    'Over 23 Years Old': 39,
    'International Student (Bachelor)': 15,
    'Short Cycle Diploma Holders': 53,
    'Technological Specialization Diploma Holders': 44,
    'Change of Institution/Course': 51,
    'Change of Institution/Course (International)': 57,
    'Change of Course': 43,
    'Transfer': 42,
    'Holders of Other Higher Courses': 7,
    '1st Phase - Special Contingent (Madeira Island)': 16,
    '1st Phase - Special Contingent (Azores Island)': 5,
    'Ordinance No. 612/93': 2,
    'Ordinance No. 854-B/99': 10,
    'Ordinance No. 533-A/99, Item B2 (Different Plan)': 26,
    'Ordinance No. 533-A/99, Item B3 (Other Institution)': 27
}

# Daftar input
input_fields = {
    "Marital_status": {"type": "select", "options": marital_status_options},
    "Application_mode": {"type": "select", "options": application_mode_options},
    "Previous_qualification_grade": {"type": "number", "min": 0.0, "max": 200.0, "step": 0.1, "default": 140.0},
    "Admission_grade": {"type": "number", "min": 0.0, "max": 200.0, "step": 0.1, "default": 130.0},
    "Displaced": {"type": "select", "options": {"No": 0, "Yes": 1}},
    "Debtor": {"type": "select", "options": {"No": 0, "Yes": 1}},
    "Tuition_fees_up_to_date": {"type": "select", "options": {"No": 0, "Yes": 1}},
    "Gender": {"type": "select", "options": {"Female": 0, "Male": 1}},
    "Scholarship_holder": {"type": "select", "options": {"No": 0, "Yes": 1}},
    "Age_at_enrollment": {"type": "number", "min": 15, "max": 90, "step": 1, "default": 18},
    "Curricular_units_1st_sem_enrolled": {"type": "number", "min": 0, "max": 100, "step": 1, "default": 6},
    "Curricular_units_1st_sem_approved": {"type": "number", "min": 0, "max": 100, "step": 1, "default": 6},
    "Curricular_units_1st_sem_grade": {"type": "number", "min": 0.0, "max": 20.0, "step": 0.1, "default": 12.0},
    "Curricular_units_2nd_sem_enrolled": {"type": "number", "min": 0, "max": 100, "step": 1, "default": 6},
    "Curricular_units_2nd_sem_evaluations": {"type": "number", "min": 0, "max": 20, "step": 1, "default": 6},
    "Curricular_units_2nd_sem_approved": {"type": "number", "min": 0, "max": 100, "step": 1, "default": 6},
    "Curricular_units_2nd_sem_grade": {"type": "number", "min": 0.0, "max": 20.0, "step": 0.1, "default": 12.0},
    "Curricular_units_2nd_sem_without_evaluations": {"type": "number", "min": 0, "max": 100, "step": 1, "default": 0},
}

ordered_columns = list(input_fields.keys())

# Judul halaman
st.title("📊 Prediksi Dropout Mahasiswa (Input Individu)")

# Form input
user_data = {}
col1, col2 = st.columns(2)
cols = [col1, col2]
i = 0

for field, config in input_fields.items():
    with cols[i % 2]:
        if config["type"] == "number":
            user_data[field] = st.number_input(
                label=field.replace("_", " "),
                min_value=config["min"],
                max_value=config["max"],
                value=config.get("default", config["min"]),
                step=config["step"]
            )
        elif config["type"] == "select":
            label_list = list(config["options"].keys())
            default_index = 0
            user_data[field] = config["options"][st.selectbox(
                label=field.replace("_", " "),
                options=label_list,
                index=default_index
            )]
    i += 1

# Tombol prediksi
if st.button("🔍 Jalankan Prediksi"):
    input_df = pd.DataFrame([user_data])[ordered_columns]
    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0]

    st.markdown("---")
    st.subheader("📢 Hasil Analisis:")
    if pred == 0:
        st.error("⚠️ Mahasiswa ini berpotensi **DROP OUT**.")
        st.markdown(f"**Probabilitas Dropout:** `{prob[0]:.2%}`")
    else:
        st.success("✅ Mahasiswa ini **kemungkinan besar tetap kuliah**.")
        st.markdown(f"**Probabilitas Tidak Dropout:** `{prob[1]:.2%}`")

    st.markdown("---")
    st.subheader("📝 Ringkasan Data yang Dimasukkan")
    st.dataframe(input_df)