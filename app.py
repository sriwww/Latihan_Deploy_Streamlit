import streamlit as st
from data import *



# Judul dashboard
def judul():
    st.title("Dashboard Covid-19 Indonesia 😷")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data COVID-19 di Indonesia 🔴⚪")

st.sidebar.title("📊 Navigasi")
menu= st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])
if menu == "Home":
    #judul
    judul()

    #filtering
    df=load_data()
    year=select_year()
    location = select_location(df)
    df_filtered= filter_data(df, year, location)

    #kolom1
    kolom1(df_filtered)
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)

elif menu == "Halaman Data":
    #judul
    judul()

    #filtering
    year=select_year()
    df=load_data()
    location = select_location(df)
    df_filtered= filter_data(df, year, location)

    #show data
    show_data(df_filtered)

# Menambahkan copyright soal no 1
footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 10px;
            left: 50%;
            font-size: 12px;
            color: black;
        }
    </style>
    <div class="footer">
        © 2025 IgaPutriRamadhani 184230036. All rights reserved.
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
