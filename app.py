import streamlit as st
from data import *


def judul():
#judul dashboard
    st.title("🏥 Dashboard COVID-19")
    st.write("Selamat datang di dashborad interaktif untuk menganalisis data COVID-19 di Indonesia")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman",["Home","Halaman Data"])

if menu == "Home":
    judul()
    
    #filtering
    df = load_data()
    year = select_year()
    locations = select_location(df)
    df_filtered = filter_data(df, year, locations)
    #kolom 1
    kolom1(df_filtered)
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)
    
    
elif menu == "Halaman Data":
    judul()
    year = select_year()
    df = load_data()
    locations = select_location(df)
    df_filtered = filter_data(df, year, locations)
    show_data(df_filtered)
    
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: pink;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    <div class="footer">
        © SRI CAHYANI - 184230018
    </div>
    """,
    unsafe_allow_html=True
)