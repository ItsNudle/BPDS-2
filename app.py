import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("model.joblib")

st.set_page_config(page_title="Prediksi Dropout Mahasiswa", layout="centered")
st.title("🎓 Prediksi Dropout Mahasiswa")

# Fungsi konversi manual kategori ke angka (sesuai dengan model)
def encode_yes_no(value):
    return 1 if value == 'Yes' else 0

def encode_gender(value):
    return 1 if value == 'Male' else 0

def encode_marital_status(value):
    mapping = {
        'Single': 0,
        'Married': 1,
        'Divorced': 2,
        'Widower': 3,
        'Facto Union': 4,
        'Legally Seperated': 5
    }
    return mapping.get(value, 0)

# --- Input Form ---

# Marital Status
marital_status = st.selectbox("Marital Status", [
    'Single', 'Married', 'Divorced', 'Widower', 'Facto Union', 'Legally Seperated'
])
marital_status_encoded = encode_marital_status(marital_status)

application_mode = st.number_input("Application Mode (angka)", min_value=0)

previous_grade = st.number_input("Previous Qualification Grade", min_value=0.0)
admission_grade = st.number_input("Admission Grade", min_value=0.0)

displaced = st.selectbox("Displaced", ["Yes", "No"])
debtor = st.selectbox("Debtor", ["Yes", "No"])
tuition_fees = st.selectbox("Tuition Fees Up-to-date", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female"])
scholarship = st.selectbox("Scholarship Holder", ["Yes", "No"])

age = st.number_input("Age at Enrollment", min_value=0)
units_1st_enrolled = st.number_input("1st Sem: Units Enrolled", min_value=0)
units_1st_approved = st.number_input("1st Sem: Units Approved", min_value=0)
units_1st_grade = st.number_input("1st Sem: Grade", min_value=0.0)

units_2nd_enrolled = st.number_input("2nd Sem: Units Enrolled", min_value=0)
units_2nd_evaluated = st.number_input("2nd Sem: Units Evaluated", min_value=0)
units_2nd_approved = st.number_input("2nd Sem: Units Approved", min_value=0)
units_2nd_grade = st.number_input("2nd Sem: Grade", min_value=0.0)
units_2nd_wo_eval = st.number_input("2nd Sem: Units Without Evaluation", min_value=0)

# --- Encoding ---
input_dict = {
    'Marital_status': [marital_status_encoded],
    'Application_mode': [application_mode],
    'Previous_qualification_grade': [previous_grade],
    'Admission_grade': [admission_grade],
    'Displaced': [encode_yes_no(displaced)],
    'Debtor': [encode_yes_no(debtor)],
    'Tuition_fees_up_to_date': [encode_yes_no(tuition_fees)],
    'Gender': [encode_gender(gender)],
    'Scholarship_holder': [encode_yes_no(scholarship)],
    'Age_at_enrollment': [age],
    'Curricular_units_1st_sem_enrolled': [units_1st_enrolled],
    'Curricular_units_1st_sem_approved': [units_1st_approved],
    'Curricular_units_1st_sem_grade': [units_1st_grade],
    'Curricular_units_2nd_sem_enrolled': [units_2nd_enrolled],
    'Curricular_units_2nd_sem_evaluations': [units_2nd_evaluated],
    'Curricular_units_2nd_sem_approved': [units_2nd_approved],
    'Curricular_units_2nd_sem_grade': [units_2nd_grade],
    'Curricular_units_2nd_sem_without_evaluations': [units_2nd_wo_eval]
}
input_df = pd.DataFrame(input_dict)

# --- Prediksi ---
if st.button("🔍 Prediksi"):
    prediction = model.predict(input_df)[0]
    probas = model.predict_proba(input_df)[0]

    if prediction == 1:
        st.error("❌ Mahasiswa diprediksi **akan Dropout**.")
    else:
        st.success("✅ Mahasiswa diprediksi **tidak akan Dropout**.")

    st.markdown(f"**Probabilitas Dropout:** `{probas[1]*100:.2f}%`")