import streamlit as st
import pandas as pd

st.title("Hello Streamlit 👋")
st.write("Ini aplikasi pertama aku!")

# Basic components
name = st.text_input("Masukkan nama kamu:")
age = st.slider("Umur kamu:", 1, 100, 20)

if st.button("Tampilkan"):
    st.success(f"Halo {name}, umur kamu {age} tahun.")