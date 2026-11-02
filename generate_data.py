import os
import pandas as pd
import numpy as np

# 1. Membuat struktur direktori (folder) jika belum ada
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
print("Direktori 'data/raw/' dan 'data/processed/' berhasil dibuat!")

# Set random seed agar data konsisten saat digenerate
np.random.seed(42)

# --- 2. MEMBUAT DATA RAW (DATA MENTAH) ---
date_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
regions = ['Sumatera_Selatan', 'Riau', 'Kalimantan_Barat', 'Kalimantan_Tengah']

# A. Raw Hotspot Karhutla
hotspot_data = []
for date in date_range:
    for reg in regions:
        # Puncak Karhutla diset tinggi pada bulan Juli - Oktober (bulan 7-10)
        if date.month in [7, 8, 9, 10] and reg in ['Riau', 'Kalimantan_Tengah']:
            h_count = np.random.randint(150, 450)
        else:
            h_count = np.random.randint(0, 35)
        hotspot_data.append({'tanggal': date, 'wilayah': reg, 'jumlah_hotspot': h_count})

df_raw_hotspot = pd.DataFrame(hotspot_data)
# Simpan ke data/raw/
df_raw_hotspot.to_csv('data/raw/raw_hotspot_karhutla.csv', index=False)
print("File tersimpan: data/raw/raw_hotspot_karhutla.csv")

# B. Raw Penjualan Masker (E-commerce)
sales_data = []
for index, row in df_raw_hotspot.iterrows():
    # Asumsi penjualan dipengaruhi oleh jumlah hotspot + faktor random/noise normal
    base_sales = row['jumlah_hotspot'] * np.random.uniform(12, 18) + np.random.normal(120, 30)
    units = max(10, int(base_sales)) # Minimal penjualan 10 unit
    sales_data.append({
        'order_id': f"ORD-{index+1000}",
        'order_date': row['tanggal'],
        'region': row['wilayah'],
        'product_category': np.random.choice(['Masker Medis 3Ply', 'Masker N95', 'Masker Kain'], p=[0.5, 0.3, 0.2]),
        'units_sold': units,
        'revenue_idr': units * np.random.choice([15000, 45000, 10000]) # Estimasi harga sesuai jenis
    })

df_raw_sales = pd.DataFrame(sales_data)
# Simpan ke data/raw/
df_raw_sales.to_csv('data/raw/raw_mask_sales_ecommerce.csv', index=False)
print("File tersimpan: data/raw/raw_mask_sales_ecommerce.csv")


# --- 3. MEMBUAT DATA PROCESSED (DATA BERSIH & SIAP ANALISIS) ---
# Mengagregasi data mentah ke level Mingguan (Weekly) agar mudah dianalisis korelasinya
df_raw_hotspot['tanggal'] = pd.to_datetime(df_raw_hotspot['tanggal'])
df_raw_sales['order_date'] = pd.to_datetime(df_raw_sales['order_date'])

# Weekly Hotspots
weekly_hotspot = df_raw_hotspot.set_index('tanggal').groupby([
    pd.Grouper(freq='W'), 'wilayah'
])['jumlah_hotspot'].sum().reset_index()

# Weekly Sales
weekly_sales = df_raw_sales.set_index('order_date').groupby([
    pd.Grouper(freq='W'), 'region'
])['units_sold'].sum().reset_index()

# Merge data mingguan
df_processed = pd.merge(
    weekly_hotspot, 
    weekly_sales, 
    left_on=['tanggal', 'wilayah'], 
    right_on=['order_date', 'region'], 
    how='inner'
).drop(columns=['order_date', 'region'])

df_processed.columns = ['week_date', 'region', 'total_hotspots', 'total_mask_sales']

# Simpan ke data/processed/
df_processed.to_csv('data/processed/clean_karhutla_mask_sales.csv', index=False)
print("File tersimpan: data/processed/clean_karhutla_mask_sales.csv")
print("\nSemua file dataset berhasil dibuat dengan sukses!")