import streamlit as st
import pandas as pd
import os

databaseObject = pd.read_csv("Database/output.csv")


def LoadData():
    #  Load the CSV which contains all the inputted Data
    filename = "Database/output.csv"
    if not os.path.exists(filename):
        print("No file.")
    else:
        databaseObject = pd.read_csv("Database/output.csv")
        print("File already exists.")
        return databaseObject


def ReverseEncode(dfL):
    # Mapping values for FIRST_TIME_HOMEBUYER_FLAG
    dfL["FIRST_TIME_HOMEBUYER_FLAG"] = dfL["FIRST_TIME_HOMEBUYER_FLAG"].map({1: "Yes", 0: "No"})
    # Mapping values for OCCUPANCY_STATUS
    dfL["OCCUPANCY_STATUS"] = dfL["OCCUPANCY_STATUS"].map(
        {1: "Primary Residence", 0: "Investment Property", 2: "Secondary Residence"})
    # Mapping values for CHANNEL
    dfL["CHANNEL"] = dfL["CHANNEL"].map({0: "Broker", 1: "Correspondent", 2: "Retail"})
    # Mapping values for PROPERTY_TYPE
    dfL["PROPERTY_TYPE"] = dfL["PROPERTY_TYPE"].map(
        {0: "Condominium", 1: "Commercial Property", 2: "Manufactured Housing", 3: "Planned Unit", 4: "Single Family"})
    # Mapping values for LOAN_PURPOSE
    dfL["LOAN_PURPOSE"] = dfL["LOAN_PURPOSE"].map({0: "Cash-out Refinance", 1: "Refinance", 2: "Purchase"})
    return dfL


def main():
    st.title("Admin Dashboard")
    st.write("---")
    df = LoadData()
    dfRE = ReverseEncode(df)
    # Sidebar (left side) with the list of names
    st.sidebar.title('Names')
    selected_name = st.sidebar.selectbox('Select a name', dfRE['Name'])
    # Display the columns one by one
    selected_row = dfRE[dfRE['Name'] == selected_name]
    for column in selected_row.columns:
        st.subheader(column)
        content = (str(selected_row[column].values[0]))
        if selected_row[column].dtype == 'object':
            # Displaying String Object which is the name
            st.write(content)
            st.write("---")
        else:
            # Write the content of that column
            st.write(content)
            st.write("---")


if __name__ == "__main__":
    main()
