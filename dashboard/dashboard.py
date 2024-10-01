import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Jumlah count berdasarkan jam
def create_total_count_by_hour(hour_df):
    total_count_by_hour = hour_df.groupby(by="hr").agg({"cnt": ["sum"]})
    return total_count_by_hour

# jumlah count berdsarkan pengguna casual
def create_total_count_by_casual(day_df):
    total_count_by_casual = day_df.groupby(by="dteday").agg({"casual": ["sum"]})
    return total_count_by_casual

# jumlah count berdasarkan pengguna registered    
def create_total_count_by_registered(day_df):
    total_count_by_registered = day_df.groupby(by="dteday").agg({"registered": ["sum"]})
    return total_count_by_registered

# Jumlah count berdasarkan hari
def create_total_count_by_day(day_df):
    total_count_by_day = day_df.groupby(by="dteday").agg({"cnt": ["sum"]})
    return total_count_by_day

#jumlah count berdasarkan musim
def create_total_count_by_season(day_df):
    total_count_by_season = day_df.groupby("season").agg({"cnt": "sum"})
    return total_count_by_season


# Load data
hour_df = pd.read_csv("dashboard/hour.csv")
day_df = pd.read_csv("dashboard/day.csv")

# Mengubah tipe data integer menjadi kategori
columns_to_convert = ['season', 'mnth', 'holiday', 'weekday', 'weathersit']
day_df[columns_to_convert] = day_df[columns_to_convert].astype('category')
hour_df[columns_to_convert] = hour_df[columns_to_convert].astype('category')

# Mengubah tipe data object menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Konversi season menjadi 1.spring 2.summer 3.fall 4.winter
day_df['season']=day_df['season'].map({
    1: 'spring',
    2: 'summer',
    3: 'fall',
    4: 'winter'
    })

min_date_day = day_df["dteday"].min()
max_date_day = day_df["dteday"].max()

min_date_hours = hour_df["dteday"].min()
max_date_hours = hour_df["dteday"].max()

with st.sidebar:
    # Logo 
    st.image("dashboard/gambar sewa sepeda.jpg")

    # Mengambil rentang tanggal
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )   

# Menyimpan data day yang difilter
main_df_day = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]
main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & (hour_df["dteday"] <= str(end_date))]

# Memanggil helper yang sudah difungsikan berdasarkan filter
total_count_by_day = create_total_count_by_day(main_df_day)
total_count_by_hour = create_total_count_by_hour(main_df_hour)
total_count_by_casual = create_total_count_by_casual(main_df_day)
total_count_by_registered = create_total_count_by_registered(main_df_day)
total_count_by_season = create_total_count_by_season(main_df_day)

# Melengkapi bagian dashboard
st.header("Analisis Data Penyewaan Sepeda")

# Total penyewaan
st.subheader("Total penyewaan sepeda")

col1, col2, col3= st.columns(3)

with col1:
    total_sewa_byRegistered= total_count_by_registered.registered.sum()
    st.metric("Sewa registered", value=total_sewa_byRegistered)

with col2:
    total_sewa_byCasual= total_count_by_casual.casual.sum()
    st.metric("Sewa casual", value=total_sewa_byCasual)

with col3:
    total_sewa= total_count_by_day.cnt.sum()
    st.metric("Total sewa", value=total_sewa)

# Visualisasi performa penyewaan sepeda harian
st.subheader("Performa Penyewaan Sepeda Harian")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df_day["dteday"],
    main_df_day['cnt'],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Total Penyewaan Sepeda Harian", fontsize=20)
ax.set_xlabel("Tanggal", fontsize=16)
ax.set_ylabel("Jumlah Penyewaan", fontsize=16)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=14, rotation=45)

st.pyplot(fig)

# Visualisasi penyewaan sepeda berdasarkan jam
st.subheader("Penyewaan Sepeda Berdasarkan Jam")

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    total_count_by_hour.index,
    total_count_by_hour[('cnt', 'sum')],
    color="#FFA726"
)
ax.set_title("Total Penyewaan Berdasarkan Jam", fontsize=20)
ax.set_xlabel("Jam", fontsize=16)
ax.set_ylabel("Jumlah Penyewaan", fontsize=16)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=14)

st.pyplot(fig)

# Visualisasi penyewaan sepeda berdasarkan musim
st.subheader("Penyewaan Sepeda Berdasarkan Musim")

# Membuat pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    total_count_by_season["cnt"],
    labels=total_count_by_season.index,
    autopct='%1.1f%%',  # Menampilkan persentase
    colors=sns.color_palette("Set2", len(total_count_by_season.index)),  # Skema warna
    startangle=90,  # Memutar pie chart agar lebih terlihat proporsional
    wedgeprops={'edgecolor': 'black'}  # Menambahkan garis tepi
)
ax.set_title("Persentase Penyewaan Sepeda Berdasarkan Musim", fontsize=16)

# Menampilkan pie chart di Streamlit
st.pyplot(fig)

# Membuat pie chart untuk perbandingan pengguna casual dan registered
st.subheader("Perbandingan Penyewaan: Casual vs Registered")

# Menghitung total penyewaan casual dan registered
total_sewa_by_casual = total_count_by_casual.casual.sum().values[0]  # Ambil nilai total
total_sewa_by_registered = total_count_by_registered.registered.sum().values[0]  # Ambil nilai total

# Membuat pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    [total_sewa_by_registered, total_sewa_by_casual],  # Total sewa casual dan registered
    labels=['Registered', 'Casual'],
    autopct='%1.1f%%',  # Menampilkan persentase
    colors=sns.color_palette("Set2", 2),  # Skema warna untuk dua kategori
    startangle=90,  # Memutar pie chart agar lebih terlihat proporsional
    wedgeprops={'edgecolor': 'black'}  # Menambahkan garis tepi
)
ax.set_title("Perbandingan Penyewaan: Casual vs Registered", fontsize=16)

# Menampilkan pie chart di Streamlit
st.pyplot(fig)




# Footer
st.write("Dashboard dibuat oleh Aditya Vahreza")
