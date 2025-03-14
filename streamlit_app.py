import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv",)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["year"] = df["datetime"].dt.year
    return df

df = load_data()

# Sidebar
st.sidebar.title("Dashboard Polusi Udara")
tahun_pilihan = st.sidebar.selectbox("Pilih Tahun", sorted(df["year"].unique()))

# Filter data berdasarkan tahun yang dipilih
df_filtered = df[df["year"] == tahun_pilihan]
monthly_avg = df_filtered.groupby("month")[["pm2.5", "pm10"]].mean()
df.groupby("month")[["pm2.5", "pm10"]].mean()

# Visualisasi Tren Polusi Udara
st.title(f"Pola Polusi Udara Tahun {tahun_pilihan}")
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(data=monthly_avg, markers=True, ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Konsentrasi Polutan")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
st.pyplot(fig)

kesimpulan = ["Polusi PM2.5 dan PM10 cenderung mengalami peningkatan pada awal tahun (Jan - Apr) dan menurun di pertengahan tahun (Jun - Sep). Lonjakan kembali terjadi menjelang akhir tahun (Okt - Des), yang mungkin terkait dengan perubahan cuaca atau aktivitas manusia tertentu (misalnya musim kemarau, polusi kendaraan, atau aktivitas industri).","Tahun 2014 dan 2016 menunjukkan lonjakan PM2.5 dan PM10 yang lebih tinggi dibandingkan tahun lainnya, terutama pada Maret - Mei. Tahun 2015 tampaknya memiliki tren yang lebih stabil dibandingkan 2014 dan 2016."]

st.subheader("Kesimpulan")
for item in kesimpulan:
    st.write(f"- {item}")

# Heatmap Korelasi Faktor Lingkungan
st.title("Pola Hubungan antara Faktor Meteorologi dan Polusi")
corr = df_filtered[['pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3', 'temp', 'pres', 'dewp', 'rain', 'wspm']].corr()
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

kesimpulan = ["PM2.5 dan PM10 memiliki korelasi sangat tinggi (0.85)Artinya, jika PM2.5 meningkat, PM10 juga cenderung meningkat, karena keduanya berasal dari sumber yang serupa","Suhu (temp) memiliki korelasi rendah dengan polusi (sekitar 0.07 dan 0.09)Artinya, suhu tidak terlalu berpengaruh langsung terhadap tingkat polusi udara.","Tekanan udara (pres) memiliki korelasi negatif dengan PM2.5 dan PM10 (-0.13 dan -0.16)Saat tekanan udara tinggi, polutan cenderung terdispersi lebih baik, sehingga konsentrasi polusi menurun.","Curah hujan (rain) memiliki korelasi negatif dengan polusi (-0.10 dan -0.12)Hujan membantu mengurangi polusi udara dengan cara 'membersihkan' partikel dari atmosfer.","Kecepatan angin (wspm) juga berkorelasi negatif dengan polusi (-0.25 dan -0.21)Saat kecepatan angin lebih tinggi, polutan lebih cepat terbawa dan terdispersi, sehingga polusi berkurang.","PM2.5 dan PM10 sangat dipengaruhi oleh CO, NO2, dan SO2,berarti sumber utama polusi udara kemungkinan besar berasal dari emisi kendaraan, industri, dan pembakaran bahan bakar fosil."]

st.subheader("Kesimpulan")
for item in kesimpulan:
    st.write(f"- {item}")

