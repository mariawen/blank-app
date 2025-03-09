import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    # Gantilah dengan data asli yang Anda miliki
    df = pd.read_csv("main_data.csv",)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")  # Konversi ke datetime
    df["year"] = df["datetime"].dt.year
    return df

df = load_data()

# Sidebar
st.sidebar.title("Dashboard Polusi Udara")
tahun_pilihan = st.sidebar.selectbox("Pilih Tahun", sorted(df["year"].unique()))

# Filter data berdasarkan tahun yang dipilih
df_filtered = df[df["year"] == tahun_pilihan]
monthly_avg = df_filtered.groupby("month")[["pm2.5", "pm10"]].mean()
df.groupby("month")[["pm2.5", "pm10"]].mean()  # ✅ Berjalan dengan baik!

# Visualisasi Tren Polusi Udara
st.title(f"Tren Polusi Udara Tahun {tahun_pilihan}")
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(data=monthly_avg, markers=True, ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Konsentrasi Polutan")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
st.pyplot(fig)

# Heatmap Korelasi Faktor Lingkungan
st.subheader("Korelasi Faktor Lingkungan dan Polusi Udara")
corr = df_filtered[["pm2.5", "pm10", "temp", "pres", "rain", "wspm"]].corr()
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Kesimpulan
st.subheader("Kesimpulan")
st.write(
    f"Pengendalian polusi perlu difokuskan pada bulan-bulan dengan tren peningkatan (awal dan akhir tahun) untuk mengurangi dampak buruknya.Peningkatan pemantauan dan intervensi kebijakan bisa membantu mengendalikan tren polusi, terutama di kota-kota dengan risiko tinggi. \n"
    "Pengurangan polusi harus difokuskan pada pengendalian sumber pencemaran seperti kendaraan bermotor dan industri, bukan hanya mengandalkan faktor cuaca.Strategi tata kota bisa memanfaatkan pola angin untuk mengurangi polusi di daerah dengan tingkat polutan tinggi, misalnya dengan menanam lebih banyak pohon di jalur angin utama.Pemantauan polusi sebaiknya tidak hanya mempertimbangkan faktor cuaca, tetapi juga aktivitas manusia, seperti lalu lintas dan aktivitas industri."
)