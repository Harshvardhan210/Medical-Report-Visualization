import streamlit as st


def home_screen():
    st.title("Home - Enter Medical Data")

    sugar_level = st.number_input("Enter Sugar Level")
    blood_pressure = st.number_input("Enter Blood Pressure")

    if st.button("Save Data"):
        st.success("Data saved successfully!")