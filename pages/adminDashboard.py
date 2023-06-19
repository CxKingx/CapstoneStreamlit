import streamlit as st
import pandas as pd
import os

databaseObject = pd.read_csv("Database/output.csv")
print(databaseObject.head())


def LoadData():
    #  Load the CSV which contains all the inputted Data
    filename = "Database/output.csv"
    if not os.path.exists(filename):
        print("No file.")

    else:
        databaseObject = pd.read_csv("Database/output.csv")
        print("File already exists.")
        return databaseObject


def main():
    st.title("Admin Dashboard")
    st.write("---")
    df = LoadData()
    # Sidebar (left side) with the list of names
    st.sidebar.title('Names')
    selected_name = st.sidebar.selectbox('Select a name', df['Name'])
    # Right side to display full information
    selected_row = df[df['Name'] == selected_name]

    # Display the columns one by one
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
