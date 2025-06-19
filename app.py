import streamlit as st
import pandas as pd
import joblib

# Konfigurasi Halaman
st.set_page_config(layout="centered", page_title="Prediksi DropOut Mahasiswa")

# Memuat model
@st.cache_resource
def load_model():
    return joblib.load('model.joblib')

model = load_model()

# Definisi input fitur
features_definition = {
    "Marital_status": {
        "type": "selectbox",
        "options": {"Single": 1, "Married": 2, "Widower": 3, "Divorced": 4, "Legally Separated": 5},
        "default": 1,
    },
    "Application_mode": {
        "type": "selectbox",
        "options": {
            "1 - General Contingent": 1, "2 - Ordinance No. 612/93": 2, "17 - 2nd Phase - General": 17,
            "39 - Over 23 Years Old": 39
        },
        "default": 1,
    },
    "Previous_qualification_grade": {
        "type": "number_input", "min_value": 0.0, "max_value": 200.0, "default": 140.0, "step": 0.1,
    },
    "Admission_grade": {
        "type": "number_input", "min_value": 0.0, "max_value": 200.0, "default": 130.0, "step": 0.1,
    },
    "Displaced": {
        "type": "selectbox", "options": {"Tidak": 0, "Ya": 1}, "default": 0
    },
    "Debtor": {
        "type": "selectbox", "options": {"Tidak": 0, "Ya": 1}, "default": 0
    },
    "Tuition_fees_up_to_date": {
        "type": "selectbox", "options": {"Tidak": 0, "Ya": 1}, "default": 1
    },
    "Gender": {
        "type": "selectbox", "options": {"Perempuan": 0, "Laki-laki": 1}, "default": 1
    },
    "Scholarship_holder": {
        "type": "selectbox", "options": {"Tidak": 0, "Ya": 1}, "default": 0
    },
    "Age_at_enrollment": {
        "type": "number_input", "min_value": 15, "max_value": 90, "default": 18, "step": 1,
    },
    "Curricular_units_1st_sem_enrolled": {
        "type": "number_input", "min_value": 0, "max_value": 100, "default": 6, "step": 1
    },
    "Curricular_units_1st_sem_approved": {
        "type": "number_input", "min_value": 0, "max_value": 100, "default": 6, "step": 1
    },
    "Curricular_units_1st_sem_grade": {
        "type": "number_input", "min_value": 0.0, "max_value": 20.0, "default": 12.0, "step": 0.1
    },
    "Curricular_units_2nd_sem_enrolled": {
        "type": "number_input", "min_value": 0, "max_value": 100, "default": 6, "step": 1
    },
    "Curricular_units_2nd_sem_evaluations": {
        "type": "number_input", "min_value": 0, "max_value": 20, "default": 6, "step": 1
    },
    "Curricular_units_2nd_sem_approved": {
        "type": "number_input", "min_value": 0, "max_value": 100, "default": 6, "step": 1
    },
    "Curricular_units_2nd_sem_grade": {
        "type": "number_input", "min_value": 0.0, "max_value": 20.0, "default": 12.0, "step": 0.1
    },
    "Curricular_units_2nd_sem_without_evaluations": {
        "type": "number_input", "min_value": 0, "max_value": 100, "default": 0, "step": 1
    },
}

feature_columns_order = list(features_definition.keys())

# UI Prediksi Single Mahasiswa
st.title("🎓 Prediksi DropOut Mahasiswa")

input_data = {}
cols = st.columns(2)
col_idx = 0

for feature, detail in features_definition.items():
    with cols[col_idx % 2]:
        if detail["type"] == "number_input":
            input_data[feature] = st.number_input(
                label=feature.replace("_", " "),
                min_value=detail["min_value"],
                max_value=detail["max_value"],
                value=detail["default"],
                step=detail["step"]
            )
        elif detail["type"] == "selectbox":
            labels = list(detail["options"].keys())
            default_label = next(k for k, v in detail["options"].items() if v == detail["default"])
            selected = st.selectbox(
                label=feature.replace("_", " "),
                options=labels,
                index=labels.index(default_label)
            )
            input_data[feature] = detail["options"][selected]
    col_idx += 1

if st.button("🔍 Prediksi Mahasiswa"):
    input_df = pd.DataFrame([input_data])[feature_columns_order]
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]

    st.markdown("---")
    st.subheader("📊 Hasil Prediksi")
    if prediction == 0:
        st.error("❌ Mahasiswa ini DIPREDIKSI AKAN DROPOUT.")
        st.markdown(f"**Probabilitas Dropout:** `{proba[0]:.2f}`")
    else:
        st.success("✅ Mahasiswa ini DIPREDIKSI TIDAK AKAN DROPOUT.")
        st.markdown(f"**Probabilitas Tidak Dropout:** `{proba[1]:.2f}`")

    st.markdown("---")
    st.subheader("📄 Data yang Diberikan:")
    st.dataframe(input_df)