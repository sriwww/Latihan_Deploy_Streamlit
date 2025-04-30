import streamlit as st
import pandas as pd
import plotly.express as px

#fungsi load data
def load_data():
    df = pd.read_csv("dataset\covid_19_indonesia_time_series_all.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

def filter_data(df, year=None, locations=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if locations and "Semua Provinsi" not in locations:
        df = df[df["Location"].isin(locations)]
    return df

def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun",
        options= [None,2020,2021,2022],
        format_func=lambda x: "Semua Tahun" if x is None else x
    )
    
def select_location(df):
    locations = sorted(df["Location"].unique())
    return st.sidebar.multiselect(
        "Pilih Provinsi",
        options=locations,
        default=locations
    )
    
#fungsi untuk menampilkan data
def show_data(df):
   selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
   df_selected = df[selected_columns]
   st.subheader("Data Covid-19 Indonesia")
   st.dataframe(df_selected.head(10))
   
#Total Kasus
def total_case(df):
    total_kasus = df.sort_values('Date').groupby('Location',as_index=False).last()
    return total_kasus['Total Cases'].sum()

#total death
def total_death(df):
    total_kematian = df.sort_values('Date').groupby('Location',as_index=False).last()
    return total_kematian['Total Deaths'].sum()

#total sembuh
def total_recovery(df):
    total_sembuh= df.sort_values('Date').groupby('Location',as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

#kolom 1
def kolom1(df):
    kasus= total_case(df)
    kematian= total_death(df)
    sembuh= total_recovery(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Kasus", value=kasus)
    col2.metric(label="Total Kematian", value=kematian)
    col3.metric(label="Total Sembuh", value=sembuh)

def pie_chart1(df):
    total_mati= total_death(df)
    total_sembuh= total_recovery(df)
    
    data = {
        'Status' : ['Meninggal','Sembuh'],
        'Jumlah' : [total_mati,total_sembuh]
    }
    
    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#4de89f','#ff6459']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def bar_chart1(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='5 Provinsi dengan kematia  Tertinggi',
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
        color='Total Recovered',
        color_continuous_scale='greens',
        title='5 provinsi dengan kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )
    
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    
def map_chart(df, year=None):
    df['Date']=pd.to_datetime(df['Date'])
    
    #filter data berdasarkan tahun
    if year:
        df = df[df['Date'].dt.year == year]
    
    #agregasi data per lokasi
    df_agg = df.groupby(['Location','Latitude','Longitude',], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude','Longitude','New Cases'])
    
    #validasi data
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
        opacity=0.2,
        title=f'Sebaran Kasus Baru Covid-19 di Indonesia - {year if year else "Semua Tahun"}',
        mapbox_style='carto-positron'
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r":0,"t":50,"1":0,"b":0}
    )
    st.plotly_chart(fig, use_container_width=True)
        
    
    
# Menjalankan fungsi
if __name__ == "__main__":
    df = load_data()
    show_data(df)

