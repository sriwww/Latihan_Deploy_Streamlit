#fungsi load data
import streamlit as st
import pandas as pd
import plotly.express as px

# === FUNGSI UTAMA ===
@st.cache_data

def load_data():
    try:
        df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
        df = df[df["Location"] != "Indonesia"]
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    except FileNotFoundError:
        st.error("File data tidak ditemukan. Pastikan file CSV tersedia.")
        return pd.DataFrame()


def filter_data(df, year=None, locations=None):
    if year:
        df = df[df['Date'].dt.year == year]
    if locations and "Semua Provinsi" not in locations:
        df = df[df["Location"].isin(locations)]
    return df


def select_year():
    selected = st.sidebar.selectbox(
        "Pilih Tahun",
        options=["Semua Tahun", 2020, 2021, 2022]
    )
    return None if selected == "Semua Tahun" else selected



def select_location(df):
    locations = sorted(df["Location"].unique())
    return st.sidebar.multiselect(
        "Pilih Provinsi",
        options=locations,
        default=locations
    )


# === VISUALISASI DAN TABEL ===
def show_data(df):
    if df.empty:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 Indonesia")
    st.dataframe(df_selected.head(10))


def total_case(df):
    total = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total['Total Cases'].sum()


def total_death(df):
    total = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total['Total Deaths'].sum()


def total_recovery(df):
    total = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total['Total Recovered'].sum()


def kolom1(df):
    if df.empty:
        return
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Kasus", total_case(df))
    col2.metric("Total Kematian", total_death(df))
    col3.metric("Total Sembuh", total_recovery(df))


def pie_chart1(df):
    if df.empty:
        return
    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_death(df), total_recovery(df)]
    }
    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#ff6459', '#4de89f']
    )
    st.plotly_chart(fig, use_container_width=True)


def bar_chart1(df):
    if df.empty:
        return
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')
    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def bar_chart2(df):
    if df.empty:
        return
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Recovered')
    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='greens',
        title='5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def map_chart(df, year=None):
    if df.empty:
        return
    if year:
        df = df[df['Date'].dt.year == year]
    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])
    if df_map.empty:
        st.info("Tidak ada data untuk ditampilkan di peta.")
        return
    fig = px.scatter_mapbox(
        df_map,
        lat='Latitude',
        lon='Longitude',
        color='New Cases',
        size='New Cases',
        hover_name='Location',
        zoom=3,
        center={"lat": -2, "lon": 118},
        color_continuous_scale='OrRd',
        size_max=20,
        opacity=0.4,
        title=f'Sebaran Kasus Baru Covid-19 - {year if year else "Semua Tahun"}',
        mapbox_style='carto-positron'
    )
    st.plotly_chart(fig, use_container_width=True)
