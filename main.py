import streamlit as st


def login():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password":
            st.success("Logged in as {}".format(username))
            # Add your code for authenticated access or redirect to another page
        else:
            st.error("Invalid username or password")


def main():
    login()


if __name__ == "__main__":
    main()
