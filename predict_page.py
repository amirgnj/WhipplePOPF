import pickle
import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb


def load_model():
    with open('saved.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

column_names = ['Age', 'bmi', 'PRHCT', 'PRWBC', 'PRPLATE', 'PRALBUM', 'PRCREAT',
                'PRSODM', 'PRBILI', 'PRSGOT', 'PRALKPH', 'OPTIME', 'SEX_female',
                'surg_app_MIS', 'surg_app_Open', 'malignant_histo_Adenocarcinoma',
                'malignant_histo_Cholangiocarcinoma', 'malignant_histo_IPMN',
                'malignant_histo_PNET', 'malignant_histo_Periampullary',
                'PAN_DUCTSIZE_3-6_mm', 'PAN_DUCTSIZE_Unknown', 'PAN_DUCTSIZE_less3_mm',
                'PAN_DUCTSIZE_more6_mm', 'PAN_CHEMO_Yes', 'PAN_RADIO_Yes',
                'DIABETES_Yes', 'SMOKE_Yes', 'HYPERMED_Yes', 'WTLOSS_Yes',
                'PAN_JAUNDICE_Yes', 'ASACLAS_I-II', 'ASACLAS_III', 'ASACLAS_IV',
                'ASACLAS_V', 'FNSTATUS2_Independent', 'FNSTATUS2_Partially_Dependent',
                'FNSTATUS2_Totally_Dependent']

# Create the DataFrame
#sample2 = pd.DataFrame(columns=column_names)


# Create a row with all values equal to zero
#row_data = [0] * len(column_names)
#sample2.loc[0] = row_data

model = data["model"]
sample = data["sample"]

#sample2 = data["sample"]

def show_predict_page():
    st.title("Pancreatic Fistula Following Whipple")

    st.write("""### Please  provide the following information:""")
    
    Age = st.slider("Age", 18, 90, 18)
    SEX =  st.selectbox('Sex', ("Male", "Female"))
    bmi = st.slider("Bmi", 10, 70, 25)
    col0 = st.columns(2)
    FNSTATUS2_ = col0[0].selectbox('Functional status', ("Independent", "Partially_Dependent", "Totally_Dependent"))
    ASACLAS_ = col0[1].selectbox('ASA class', ("I-II", "III", "IV", "V"))

    OPTIME = int(361)
    cols = st.columns(3)
    PRHCT = cols[0].number_input("Hematocrit", 10, 55, 45)
    PRWBC = cols[1].number_input("WBC", 1, 45, 7)
    PRPLATE = cols[2].number_input("Platelet", 10, 1000, 250, 10)
    cols2 = st.columns(3)
    PRCREAT = cols2[0].number_input("Creatinine", 0, 12, 1, 1)
    PRALBUM = cols2[1].number_input("Albumin", 1, 10, 3)
    PRSODM = cols2[2].number_input("Sodium", 115, 165, 140)
    cols3 = st.columns(3)
    PRBILI = cols3[0].number_input("Bilirubin", 0, 15, 1, 1)
    PRSGOT = cols3[1].number_input("SGOT", 10, 800, 20, 10)
    PRALKPH = cols3[2].number_input("ALP", 10, 1000, 40, 10)



    
    cols4 = st.columns(2)
    SMOKE_ = cols4[0].selectbox('Smoking', ("No", "Yes"))
    DIABETES_ = cols4[1].selectbox('History of Diabetes', ("No", "Yes"))
    cols5 = st.columns(2)   
    WTLOSS_ = cols5[0].selectbox('Weight loss', ("No", "Yes"))
    HYPERMED_ = cols5[1].selectbox('Hypertension needing medication', ("No", "Yes"))
    
    cols6 = st.columns(2)
    PAN_JAUNDICE_ = cols6[0].selectbox('Jaundice', ("No", "Yes"))
    PAN_CHEMO_ = cols6[1].selectbox('Neoadjuvant chemotherapy', ("No", "Yes"))
    cols7 = st.columns(2)
    PAN_RADIO_ = cols7[0].selectbox('Neoadjuvant radiotherapy', ("No", "Yes"))
    surg_app_ =  cols7[1].selectbox('Approach', ("Open", "MIS"))
    cols8 = st.columns(2)
    malignant_histo_ = cols8[0].selectbox('Pathology', ("Adenocarcinoma", "Cholangiocarcinoma", "IPMN", "PNET", "Periampullary"))
    PAN_DUCTSIZE_ = cols8[1].selectbox('Duct size', ("less3_mm", "3-6_mm", "more6_mm", "Unknown"))



    ok = st.button("Predict the chance of CR-POPF")

    if ok:
        sample["Age"] = Age

        sample["OPTIME"] = OPTIME
        sample["bmi"] = bmi
        sample["surg_app_"+surg_app_] = 1
        
        sample["PRHCT"] = PRHCT
        sample["PRWBC"] = PRWBC
        sample["PRPLATE"] = PRPLATE
        sample["PRCREAT"] = PRCREAT
        sample["PRALBUM"] = PRALBUM
        sample["PRSODM"] = PRSODM
        sample["PRBILI"] = PRBILI
        sample["PRSGOT"] = PRSGOT
        sample["PRALKPH"] = PRALKPH

        sample["malignant_histo_"+malignant_histo_] = 1
        sample["FNSTATUS2_"+FNSTATUS2_] = 1
        sample["ASACLAS_"+ASACLAS_] = 1
        sample["PAN_DUCTSIZE_"+PAN_DUCTSIZE_] = 1



        if  SEX == "Female":
            sample["SEX_female"] = 1
        
        if  SMOKE_ == "Yes":
            sample["SMOKE_Yes"] = 1
        
        if  DIABETES_ == "Yes":
            sample["DIABETES_Yes"] = 1

        if  WTLOSS_ == "Yes":
            sample["WTLOSS_Yes"] = 1

        if  HYPERMED_ == "Yes":
            sample["HYPERMED_Yes"] = 1

        if  PAN_JAUNDICE_ == "Yes":
            sample["PAN_JAUNDICE_Yes"] = 1

        if  PAN_CHEMO_ == "Yes":
            sample["PAN_CHEMO_Yes"] = 1

        if  PAN_RADIO_ == "Yes":
            sample["PAN_RADIO_Yes"] = 1



        
        chance = model.predict_proba(sample)
        #print("XGBoost version:", xgb.__version__)
        #st.subheader(sample.columns)

        st.subheader(f"Estimated chance of CR-POPF: {chance[0][1]:.2f}")

    reset = st.button("Reset")
    if reset:
        sample.loc[:,:] = 0





        

