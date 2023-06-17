import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import pickle
import joblib
import os
from sklearn.preprocessing import LabelEncoder


# Save into a csv the information and the Result
def SaveInput(dfS):
    filename = "Database/output.csv"
    if not os.path.exists(filename):
        dfS.to_csv("Database/output.csv", index=False)
        print("New file created.")
    else:
        databaseObject = pd.read_csv("Database/output.csv")
        dfresult = databaseObject.append(dfS)
        dfresult.to_csv("Database/output.csv", index=False)
        print("File already exists.")
    print("SAVED")


def ChangeData(dfC):
    print("Change Data")
    # Mapping values for FIRST_TIME_HOMEBUYER_FLAG
    dfC["FIRST_TIME_HOMEBUYER_FLAG"] = dfC["FIRST_TIME_HOMEBUYER_FLAG"].map({"Yes": "Y", "No": "N"})

    # Mapping values for OCCUPANCY_STATUS
    dfC["OCCUPANCY_STATUS"] = dfC["OCCUPANCY_STATUS"].map(
        {"Primary Residence": "P", "Investment Property": "I", "Secondary Residence": "S"})

    # Mapping values for CHANNEL
    dfC["CHANNEL"] = dfC["CHANNEL"].map({"Retail": "R", "Correspondent": "C", "Broker": "B"})

    # Mapping values for PROPERTY_TYPE
    dfC["PROPERTY_TYPE"] = dfC["PROPERTY_TYPE"].map(
        {"Single Family": "SF", "Planned Unit": "PU", "Condominium": "CO", "Manufactured Housing": "MH",
         "Commercial Property": "CP"})

    # Mapping values for LOAN_PURPOSE
    dfC["LOAN_PURPOSE"] = dfC["LOAN_PURPOSE"].map({"Purchase": "P", "Refinance": "N", "Cash-out Refinance": "C"})
    # ["FIRST_TIME_HOMEBUYER_FLAG", "OCCUPANCY_STATUS", "CHANNEL", "PROPERTY_TYPE", "LOAN_PURPOSE"]
    return dfC


def LabelEncode(dfL):
    toEncodeDF = dfL
    # Mapping values for FIRST_TIME_HOMEBUYER_FLAG
    dfL["FIRST_TIME_HOMEBUYER_FLAG"] = dfL["FIRST_TIME_HOMEBUYER_FLAG"].map({"Y": 1, "N": 0})

    # Mapping values for OCCUPANCY_STATUS
    dfL["OCCUPANCY_STATUS"] = dfL["OCCUPANCY_STATUS"].map({"P": 1, "I": 0, "S": 2})

    # Mapping values for CHANNEL
    dfL["CHANNEL"] = dfL["CHANNEL"].map({"B": 0, "C": 1, "R": 2})

    # Mapping values for PROPERTY_TYPE
    dfL["PROPERTY_TYPE"] = dfL["PROPERTY_TYPE"].map({"CO": 0, "CP": 1, "MH": 2, "PU": 3, "SF": 4})

    # Mapping values for LOAN_PURPOSE
    dfL["LOAN_PURPOSE"] = dfL["LOAN_PURPOSE"].map({"C": 0, "N": 1, "P": 2})
    return toEncodeDF


def GivePrediction(dfP):
    print("Predicting")
    UserInput = dfP
    # Drop Name
    PredictDF = UserInput.drop('Name', axis=1)
    # Load Model
    model_xgb = xgb.XGBClassifier()
    model_xgb.load_model("model.json")
    # Predict it Returns 2 inputs
    preds = model_xgb.predict_proba(PredictDF)
    # Add it to the Dataframe
    print(type(preds))
    UserInput['Non_Default_Prediction'] = preds[0][0]
    UserInput['Default_Prediction'] = preds[0][1]

    # Return Dataframe
    return UserInput, preds


def main():
    st.title("Data Entry Form")
    # Create a form using the st.form context manager
    with st.form("data_entry_form"):
        st.subheader("Personal Information")

        name = st.text_input("Name")
        credit_score = st.number_input("Credit Score", format="%d", value=0, min_value=0, max_value=800)

        first_time_homebuyer = st.selectbox("First Time Homebuyer Flag", ["No", "Yes"])
        msa = st.number_input("Metropolitan Statistical Area", format="%d", value=0)
        num_units = st.number_input("Number of Units", format="%d", value=1, min_value=1, max_value=4)
        occupancy_status = st.selectbox("Occupancy Status", ["Primary Residence", "Investment Property", "Secondary "
                                                                                                         "Residence"])
        combined_loan_to_value = st.number_input("Original Combined Loan-to-Value", format="%d", value=0, min_value=0,
                                                 max_value=200)
        loan_to_value = st.number_input("Original Loan-to-Value", format="%d", value=0, min_value=0, max_value=200)
        channel = st.selectbox("Channel", ["Retail", "Correspondent", "Broker"])
        property_type = st.selectbox("Property Type", ["Single Family", "Planned Unit", "Condominium", "Manufactured "
                                                                                                        "Housing",
                                                       "Commercial Property"])
        postal_code = st.number_input("Postal Code", format="%d", value=0)
        loan_purpose = st.selectbox("Loan Purpose", ["Purchase", "Refinance", "Cash-out Refinance"])
        loan_term = st.number_input("Original Loan Term", format="%d", value=0, min_value=0, max_value=360)
        num_borrowers = st.number_input("Number of Borrowers", format="%d", value=1, min_value=1, max_value=4)

        submit_button = st.form_submit_button("Submit")

    # Process the form submission
    if submit_button:
        # Create a dictionary with the form data
        data = {
            "Name": name,
            "CREDIT_SCORE": credit_score,
            "FIRST_TIME_HOMEBUYER_FLAG": first_time_homebuyer,
            "METROPOLITAN_STATISTICAL_AREA": msa,
            "NUMBER_OF_UNITS": num_units,
            "OCCUPANCY_STATUS": occupancy_status,
            "ORIGINAL_COMBINED_LOAN_TO_VALUE": combined_loan_to_value,
            "ORIGINAL_LOAN_TO_VALUE": loan_to_value,
            "CHANNEL": channel,
            "PROPERTY_TYPE": property_type,
            "POSTAL_CODE": postal_code,
            "LOAN_PURPOSE": loan_purpose,
            "ORIGINAL_LOAN_TERM": loan_term,
            "NUMBER_OF_BORROWERS": num_borrowers
        }
        # Create a DataFrame from the form data
        df = pd.DataFrame([data])
        print(df)
        # Display the submitted data
        st.subheader("Submitted Data")
        st.dataframe(df)
        # Change from the Full txt, to simple ones for Categorical
        df2 = ChangeData(df)
        # Display the submitted data
        st.subheader("Simplified Data")
        st.dataframe(df2)

        # Label Encode the data
        df3 = LabelEncode(df2)
        st.subheader("Encoded Data")
        st.dataframe(df3)
        # Predict and Save to CSV
        df4, predictionValues = GivePrediction(df3)
        st.subheader("Final DF with prediction")
        st.dataframe(df4)
        st.subheader("The prediction is " + str(round(float(predictionValues[0][0]) * 100, 1)) + "% low risk")

        # Save the Dataframe
        SaveInput(df4)


if __name__ == "__main__":
    main()
