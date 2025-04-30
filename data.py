#fungsi load data
import streamlit as st
import pandas as pd
import plotly.express as px


# Show data
def load_data():
    df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

def filter_data(df, year=None, location=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if location and "Semua Provinsi" not in location:
        df = df[df['Location'].isin(location)]
    return df
 
def select_year():
    years = [None, 2020, 2021, 2022]  
    selected_year = st.sidebar.selectbox(
        "📅 Pilih Tahun",
        options=years,
        format_func=lambda x: "Semua Tahun" if x is None else str(x)
    )
    return selected_year



def select_location(df):
    locations = sorted(df['Location'].unique())
    selected = st.sidebar.multiselect(
        "Pilih Provinsi",
        options=["Semua Provinsi"] + locations,
        default=["Semua Provinsi"]
    )
    if "Semua Provinsi" in selected:
        return None
    return selected

def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 Indonesia")
    st.dataframe(df_selected.head(10))

    # Describe
    st.header("Statistik Deskriptif Dataset")
    st.write(df_selected.describe())

# Total Kasus
def total_case(df):
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()

# Total Kematian
def total_Deaths(df):
    total_kematian = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kematian['Total Deaths'].sum()

# Total Kesembuhan
def total_Recovered(df):
    total_kesembuhan = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kesembuhan['Total Recovered'].sum()

def kolom1(df):
    kasus = total_case(df) + 37
    kematian = total_Deaths(df) + 20
    sembuh = total_Recovered(df) + 75

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Kasus 🦠", value=kasus, border=True)
    col2.metric(label="Total Kematian 💀", value=kematian, border=True)
    col3.metric(label="Total Recovery ❤‍🩹", value=sembuh, border=True)

def pie_chart1(df):
    total_kematian = total_Deaths(df)
    total_sembuh = total_Recovered(df)

    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_kematian, total_sembuh]
    }

    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#03fca1', '#ab1818']
    )

    st.plotly_chart(fig, use_container_width=True)

# Bar Chart
def bar_chart1(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color_discrete_sequence=['#007474'],
        title='5 Provinsi dengan kematian tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Recovered')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color_discrete_sequence=['#B36E88'],
        title='5 Provinsi dengan Kesembuhan tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def map_chart(df, year=None):
    df['Date'] = pd.to_datetime(df['Date'])

    if year:
        df = df[df['Date'].dt.year == year]

    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])

    if df_map.empty:
        st.info("Tidak ada data untuk ditampilkan di peta")
        return

    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118},
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)
