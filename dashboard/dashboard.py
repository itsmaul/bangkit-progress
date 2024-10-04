import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def count_by_hour_df(hour_df):
    hour_count_df =  hour_df.groupby(by="hours").agg({"total": ["sum"]})
    return hour_count_df

def count_by_day_df(day_df):
    day_count_df = day_df.query(str('dates >= "2011-01-01" and dates <= "2012-12-31"'))
    return day_count_df

def total_registered_df(hour_df):
    total_registered =  hour_df.groupby(by="dates").agg({
      "registered": "sum"
    })
    total_registered = total_registered.reset_index()
    total_registered.rename(columns={
      "registered": "register_sum"
    }, inplace=True)
    return total_registered

def total_casual_df(hour_df):
    total_casual =  hour_df.groupby(by="dates").agg({
      "casual": "sum"
    })
    total_casual = total_casual.reset_index()
    total_casual.rename(columns={
      "casual": "casual_sum"
    }, inplace=True)
    return total_casual

def total_hour (hour_df):
    sum_hour_df = hour_df.groupby("hours").total.sum().reset_index()
    return sum_hour_df

def total_month(hour_df):
    sum_month_df = hour_df.groupby("months").total.sum().reset_index()
    return sum_month_df

def total_month_2(day_df):
    total_per_month = day_df.groupby('months')['total'].sum()
    return total_per_month

def total_year(day_df):
    total_per_year = day_df.groupby('years')['total'].sum()
    return total_per_year

def sum_category(day_df):
    category_total = day_df.groupby('days_category')['total'].sum()
    return category_total

def sum_season (day_df):
    season_total = day_df.groupby('season')['total'].sum()
    return season_total

hours_df = pd.read_csv("https://raw.githubusercontent.com/itsmaul/bangkit-progress/main/dashboard/hour_new.csv")
days_df = pd.read_csv("https://raw.githubusercontent.com/itsmaul/bangkit-progress/main/dashboard/day_new.csv")

hours_df.sort_values(by="dates", inplace=True)
hours_df.reset_index(inplace=True)

datetime_columns = ["dates"]
days_df.sort_values(by="dates", inplace=True)
days_df.reset_index(inplace=True)   

for column in datetime_columns:
    hours_df[column] = pd.to_datetime(hours_df[column])
    days_df[column] = pd.to_datetime(days_df[column])

min_date_hour = hours_df["dates"].min()
max_date_hour = hours_df["dates"].max()

min_date_days = days_df["dates"].min()
max_date_days = days_df["dates"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://genio.bike/wp-content/uploads/2023/05/MK-38-BK-GD-RD.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

main_df_hour = hours_df[(hours_df["dates"] >= str(start_date)) & 
                        (hours_df["dates"] <= str(end_date))]

main_df_days = days_df[(days_df["dates"] >= str(start_date)) & 
                       (days_df["dates"] <= str(end_date))]

hour_count_df = count_by_hour_df(main_df_hour)
day_count_df = count_by_day_df(main_df_days)
total_registered = total_registered_df(main_df_hour)
total_casual = total_casual_df(main_df_hour)
sum_hour_df = total_hour(main_df_hour)
sum_month_df = total_month(main_df_hour)
total_per_month = total_month_2(main_df_days)
total_per_year = total_year(main_df_days)
category_total = sum_category(main_df_days)
season_total = sum_season(main_df_days)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_count_df.total.sum()
    st.metric("Total Sharing Bike", value=total_orders)
with col2:
    total_sum = total_registered.register_sum.sum()
    st.metric("Total Registered", value=total_sum)
with col3:
    total_sum = total_casual.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Performa Penjualan Perusahaan dalam Beberapa Tahun Terakhir")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dates"],
    days_df["total"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Pada jam berapa peminjaman sepeda yang paling banyak dan paling sedikit?")

# Bar chart untuk melihat perbedaan peminjaman sepeda berdasarkan jam
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

# Bar plot untuk peminjam sepeda terbanyak
sns.barplot(x="hours", y="total", data=sum_hour_df, palette=["#D3D3D3"]*17 + ["#90CAF9"] + ["#D3D3D3"]*6, ax=ax[0])

# Atur label dan judul untuk subplot pertama
ax[0].set_ylabel("Total Rentals", fontsize=20)
ax[0].set_xlabel("Hours", fontsize=20)
ax[0].set_title("Most Rentals by Hour", fontsize=25)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=15)

# Bar plot untuk peminjam sepeda tersedikit
sns.barplot(x="hours", y="total", data=sum_hour_df.sort_values(by="hours", ascending=True), palette=["#D3D3D3"]*4 + ["#90CAF9"] + ["#D3D3D3"]*19, ax=ax[1])

# Atur label dan judul untuk subplot kedua
ax[1].set_ylabel("Total Rentals", fontsize=20)
ax[1].set_xlabel("Hours", fontsize=20)
ax[1].set_title("Fewest Rentals by Hour", fontsize=25)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=15) 

st.pyplot(fig)
st.write("Berdasarkan visualisasi bar chart, peminjam paling banyak terdapat pada pukul 17:00 dan peminjam paling sedikit pada pukul 4:00. Hal tersebut juga ditandai dengan perbedaan warna bar agar terlihat lebih jelas.")

st.subheader("Total peminjaman sepeda lebih banyak pada tahun berapa?")

# Bar chart
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="years", y="total", data=days_df.sort_values(by="years", ascending=True), palette=["#D3D3D3", "#72BCD4"], ax=ax)
ax.set_title("Total Rentals per Year", loc="center", fontsize=24)
ax.set_ylabel("Total Rentals", fontsize=18)
ax.set_xlabel("Years", fontsize=18)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

st.pyplot(fig)
st.write("Berdasarkan visualisasi bar chart, peminjaman pada tahun 2011 memiliki jumlah yang terdapat pada rentang 5000-6000, sedangkan peminjaman pada tahun 2012 memiliki jumlah yang terdapat pada rentang 3000-4000. Hal tersebut juga ditandai dengan perbedaan warna bar agar terlihat lebih jelas. Jadi, total peminjaman sepeda lebih banyak terjadi pada tahun 2012.")

st.subheader("Bagaimana tren peminjaman sepeda dari tahun 2011 ke tahun 2012?")

# Scatter chart
fig, ax = plt.subplots(figsize=(20, 6))
ax.scatter(total_per_year.index, total_per_year.values, c="#90CAF9", s=200, marker='o')
ax.plot(total_per_year.index, total_per_year.values, color="#72BCD4", linewidth=2)
ax.set_title('Bike Rental per Years', fontsize=24, loc='center')
ax.set_ylabel('Total Rentals', fontsize=18)
ax.set_xlabel('Years', fontsize=18)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

st.pyplot(fig)
st.write("Berdasarkan visualisasi scatter chart, tren peminjaman sepeda dari tahun 2011 ke 2012 mengalami peningkatan.")

st.subheader("Pada musim apa peminjaman sepeda paling sedikit?")

# Bar chart
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
        y="total",
        x="season",
        data=days_df.sort_values(by="season", ascending=False),
        palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
        ax=ax
    )
ax.set_title("Chart by Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

st.pyplot(fig)
st.write("Berdasarkan visualisasi bar chart, total peminjaman sepeda paling sedikit terjadi pada musim dingin.")

st.caption('Copyright (c) Risma Auliya Salsabilla 2024')
