import streamlit as st
import pandas as pd
import os

databaseObject = pd.read_csv("Database/output.csv")
print(databaseObject.head())

def LoadData():
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


    text_values = []
    for column in selected_row.columns:
        #print(str(selected_row[column]))
        print(str(selected_row[column].values[0]))

    # Display the columns one by one
    for column in selected_row.columns:
        st.subheader(column)
        content = (str(selected_row[column].values[0]))
        if selected_row[column].dtype == 'object':
            # Display string columns using st.write()
            st.write(content)
            st.write("---")
            #print(selected_row[column])

        else:
            # Display numeric columns using appropriate widget (e.g., st.dataframe(), st.bar_chart())
            #text_values = selected_row[column].astype(str).values
            #st.write(text_values)
            st.write(content)
            st.write("---")

if __name__ == "__main__":
    main()


