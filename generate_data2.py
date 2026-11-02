import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os

# 1. Buat folder assets jika belum ada
os.makedirs('assets', exist_ok=True)

# 2. Load data processed yang sudah dibersihkan sebelumnya
df = pd.read_csv('data/processed/clean_karhutla_mask_sales.csv')
df['week_date'] = pd.to_datetime(df['week_date'])

print("Data berhasil dimuat. Total baris:", len(df))

# Set tema visualisasi seaborn
sns.set_theme(style="whitegrid")

# --- VISUALISASI 1: Dual-Axis Trend Line (Hotspot vs Penjualan Masker) ---
fig, ax1 = plt.subplots(figsize=(12, 6))

color = '#d9534f'  # Merah bata untuk Hotspot
ax1.set_xlabel('Periode Minggu (2023)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Titik Hotspot Karhutla', color=color, fontsize=12, fontweight='bold')
line1 = ax1.plot(df['week_date'], df['total_hotspots'], color=color, linewidth=2, label='Titik Hotspot Karhutla')
ax1.tick_params(axis='y', labelcolor=color)

# Membuat sumbu Y kedua (Twin axis) untuk Penjualan Masker
ax2 = ax1.twinx()  
color = '#0275d8'  # Biru untuk Penjualan
line2 = ax2.plot(df['week_date'], df['total_mask_sales'], color=color, linewidth=2, linestyle='--', label='Penjualan Masker (Unit)')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylabel('Total Penjualan Masker (Unit)', color=color, fontsize=12, fontweight='bold')

# Judul dan Legend
plt.title('Dampak Bencana Karhutla terhadap Lonjakan Penjualan Masker di Indonesia (2023)', fontsize=14, pad=15, fontweight='bold')
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True)

fig.tight_layout()
plt.savefig('assets/sales_vs_hotspots.png', dpi=300)
print("Grafik 1 berhasil disimpan ke 'assets/sales_vs_hotspots.png'")
plt.close()


# --- VISUALISASI 2: Scatter Plot dengan Garis Regresi (Korelasi) ---
# Hitung koefisien korelasi Pearson
corr_coef, p_value = pearsonr(df['total_hotspots'], df['total_mask_sales'])

plt.figure(figsize=(8, 5))
sns.regplot(
    data=df, 
    x='total_hotspots', 
    y='total_mask_sales', 
    color='#6f42c1', 
    scatter_kws={'alpha': 0.6, 's': 50},
    line_kws={'color': '#d9534f', 'linewidth': 2}
)

plt.title(f'Korelasi Hotspot Karhutla vs Penjualan Masker (r = {corr_coef:.2f})', fontsize=13, fontweight='bold')
plt.xlabel('Jumlah Titik Hotspot Karhutla', fontsize=11, fontweight='bold')
plt.ylabel('Total Penjualan Masker (Unit)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('assets/correlation_scatter.png', dpi=300)
print("Grafik 2 berhasil disimpan ke 'assets/correlation_scatter.png'")
plt.close()