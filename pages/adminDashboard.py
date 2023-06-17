import streamlit as st
import pandas as pd


databaseObject = pd.read_csv("Database/output.csv")
print(databaseObject.head())

def LoadLabelEncoder():
    pkl_file = open('encoderModel.pkl', 'rb')
    label_encoder = pickle.load(pkl_file)
    pkl_file.close()
    return label_encoder






def main():
    st.title("Admin Dashboard")
    labelEncoder = LoadLabelEncoder()


if __name__ == "__main__":
    print("Loaded Admin Dashboard")
    main()
