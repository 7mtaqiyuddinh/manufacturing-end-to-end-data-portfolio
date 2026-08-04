"""Helper script to generate data_cleaning.ipynb programmatically."""
import json, os

cells = []

def md(source):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": source if isinstance(source, list) else [source]})

def code(source):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source if isinstance(source, list) else [source]})

# Title
md([
    "# Data Cleaning - PT Voltec Indonesia\n",
    "## Analisis Produksi Elektronik H2 2024\n",
    "\n",
    "**Tujuan:** Membersihkan data produksi mentah agar siap untuk analisis eksplorasi (EDA) dan SQL analysis.\n",
    "\n",
    "**Langkah-langkah:**\n",
    "1. Load data mentah\n",
    "2. Inspeksi awal (shape, info, describe)\n",
    "3. Penanganan missing values\n",
    "4. Penghapusan duplikat\n",
    "5. Validasi dan koreksi tipe data\n",
    "6. Deteksi dan penanganan outlier\n",
    "7. Validasi business rules\n",
    "8. Export data bersih\n",
    "9. Ringkasan perubahan",
])

md(["---\n", "## 1. Setup & Load Data"])

code([
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import os\n",
    "import warnings\n",
    "\n",
    "warnings.filterwarnings('ignore')\n",
    "pd.set_option('display.max_columns', None)\n",
    "pd.set_option('display.float_format', '{:.2f}'.format)\n",
    "print('Libraries loaded successfully.')",
])

code([
    "# Konfigurasi path\n",
    "RAW_DIR = os.path.join('..', 'data', 'raw')\n",
    "CLEAN_DIR = os.path.join('..', 'data', 'cleaned')\n",
    "os.makedirs(CLEAN_DIR, exist_ok=True)\n",
    "\n",
    "# Load semua tabel\n",
    "production = pd.read_csv(os.path.join(RAW_DIR, 'production_fact.csv'))\n",
    "line_dim = pd.read_csv(os.path.join(RAW_DIR, 'line_dim.csv'))\n",
    "machine_dim = pd.read_csv(os.path.join(RAW_DIR, 'machine_dim.csv'))\n",
    "shift_dim = pd.read_csv(os.path.join(RAW_DIR, 'shift_dim.csv'))\n",
    "product_dim = pd.read_csv(os.path.join(RAW_DIR, 'product_dim.csv'))\n",
    "\n",
    "print(f'production_fact : {production.shape}')\n",
    "print(f'line_dim        : {line_dim.shape}')\n",
    "print(f'machine_dim     : {machine_dim.shape}')\n",
    "print(f'shift_dim       : {shift_dim.shape}')\n",
    "print(f'product_dim     : {product_dim.shape}')",
])

md(["---\n", "## 2. Inspeksi Awal"])
code(["# Melihat 5 baris pertama\n", "production.head()"])
code(["# Informasi tipe data dan non-null count\n", "production.info()"])
code(["# Statistik deskriptif\n", "production.describe()"])
code([
    "# Cek tipe data saat ini\n",
    "print('Tipe data setiap kolom:')\n",
    "print(production.dtypes)\n",
    "print(f'\\nJumlah baris : {len(production):,}')\n",
    "print(f'Jumlah kolom : {production.shape[1]}')",
])

md(["---\n", "## 3. Penanganan Missing Values"])
code([
    "# Hitung missing values per kolom\n",
    "missing = production.isnull().sum()\n",
    "missing_pct = (missing / len(production) * 100).round(2)\n",
    "missing_df = pd.DataFrame({\n",
    "    'Missing Count': missing,\n",
    "    'Missing %': missing_pct\n",
    "}).sort_values('Missing Count', ascending=False)\n",
    "\n",
    "print('=== Missing Values Summary ===')\n",
    "print(missing_df[missing_df['Missing Count'] > 0])\n",
    "print(f'\\nTotal missing values: {missing.sum()}')",
])

code([
    "# Visualisasi missing values\n",
    "fig, ax = plt.subplots(figsize=(10, 4))\n",
    "cols_with_missing = missing_df[missing_df['Missing Count'] > 0].index\n",
    "sns.barplot(x=cols_with_missing, y=missing_df.loc[cols_with_missing, 'Missing %'], ax=ax, palette='Reds_d')\n",
    "ax.set_title('Persentase Missing Values per Kolom', fontsize=14, fontweight='bold')\n",
    "ax.set_ylabel('Missing (%)')\n",
    "ax.set_xlabel('Kolom')\n",
    "for i, v in enumerate(missing_df.loc[cols_with_missing, 'Missing %']):\n",
    "    ax.text(i, v + 0.05, f'{v}%', ha='center', fontsize=10)\n",
    "plt.tight_layout()\n",
    "plt.show()",
])

code([
    "# Strategi penanganan missing values:\n",
    "# - output_qty: isi dengan median per (line_id, shift_id)\n",
    "# - defect_qty: isi dengan median per (line_id, product_id)\n",
    "# - downtime_minutes: isi dengan median per machine_id\n",
    "# - machine_id: hapus baris karena FK kritis\n",
    "\n",
    "before_count = len(production)\n",
    "\n",
    "# Hapus baris dengan machine_id kosong (FK kritis)\n",
    "production = production.dropna(subset=['machine_id'])\n",
    "print(f'Baris dihapus (machine_id kosong): {before_count - len(production)}')\n",
    "\n",
    "# Isi output_qty dengan median per (line_id, shift_id)\n",
    "production['output_qty'] = production.groupby(['line_id', 'shift_id'])['output_qty'].transform(\n",
    "    lambda x: x.fillna(x.median())\n",
    ")\n",
    "\n",
    "# Isi defect_qty dengan median per (line_id, product_id)\n",
    "production['defect_qty'] = production.groupby(['line_id', 'product_id'])['defect_qty'].transform(\n",
    "    lambda x: x.fillna(x.median())\n",
    ")\n",
    "\n",
    "# Isi downtime_minutes dengan median per machine_id\n",
    "production['downtime_minutes'] = production.groupby('machine_id')['downtime_minutes'].transform(\n",
    "    lambda x: x.fillna(x.median())\n",
    ").round(1)\n",
    "\n",
    "print(f'\\nMissing values setelah penanganan:')\n",
    "print(production.isnull().sum().sum(), '(seharusnya 0)')",
])

md(["---\n", "## 4. Penghapusan Duplikat"])
code([
    "# Cek duplikat berdasarkan semua kolom kecuali production_id\n",
    "cols_check = [c for c in production.columns if c != 'production_id']\n",
    "duplicates = production.duplicated(subset=cols_check, keep='first')\n",
    "print(f'Jumlah baris duplikat: {duplicates.sum()}')\n",
    "if duplicates.sum() > 0:\n",
    "    print('\\nContoh baris duplikat (5 pertama):')\n",
    "    display(production[duplicates].head())",
])
code([
    "# Hapus duplikat\n",
    "before_dup = len(production)\n",
    "production = production.drop_duplicates(subset=cols_check, keep='first').reset_index(drop=True)\n",
    "print(f'Baris dihapus (duplikat): {before_dup - len(production)}')\n",
    "print(f'Jumlah baris sekarang: {len(production):,}')",
])

md(["---\n", "## 5. Validasi dan Koreksi Tipe Data"])
code([
    "# Konversi production_date ke datetime\n",
    "production['production_date'] = pd.to_datetime(production['production_date'])\n",
    "\n",
    "# Pastikan kolom numerik bertipe integer\n",
    "int_cols = ['production_id', 'line_id', 'machine_id', 'shift_id', 'product_id', 'target_qty', 'output_qty', 'defect_qty']\n",
    "for col in int_cols:\n",
    "    production[col] = production[col].astype(int)\n",
    "\n",
    "production['downtime_minutes'] = production['downtime_minutes'].astype(float).round(1)\n",
    "\n",
    "# Urutkan data berdasarkan tanggal secara ascending agar production_id selaras secara kronologis\n",
    "production = production.sort_values('production_date').reset_index(drop=True)\n",
    "production['production_id'] = range(1, len(production) + 1)\n",
    "\n",
    "print('Tipe data setelah koreksi:')\n",
    "print(production.dtypes)",
])
code([
    "# Validasi rentang tanggal\n",
    "print(f'Tanggal awal  : {production[\"production_date\"].min()}')\n",
    "print(f'Tanggal akhir : {production[\"production_date\"].max()}')\n",
    "print(f'Rentang       : {(production[\"production_date\"].max() - production[\"production_date\"].min()).days + 1} hari')",
])

md(["---\n", "## 6. Deteksi dan Penanganan Outlier"])
code([
    "# Visualisasi distribusi\n",
    "fig, axes = plt.subplots(1, 3, figsize=(16, 5))\n",
    "for ax, col, title in zip(axes, ['output_qty', 'defect_qty', 'downtime_minutes'],\n",
    "                           ['Output (unit)', 'Defect (unit)', 'Downtime (menit)']):\n",
    "    sns.boxplot(data=production, y=col, ax=ax, color='#3498db')\n",
    "    ax.set_title(f'Distribusi {title}', fontweight='bold')\n",
    "    ax.set_ylabel(title)\n",
    "plt.suptitle('Boxplot Sebelum Penanganan Outlier', fontsize=14, fontweight='bold', y=1.02)\n",
    "plt.tight_layout()\n",
    "plt.show()",
])
code([
    "# Deteksi outlier dengan IQR method\n",
    "def detect_outliers_iqr(df, col):\n",
    "    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)\n",
    "    IQR = Q3 - Q1\n",
    "    return df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)], Q1 - 1.5*IQR, Q3 + 1.5*IQR\n",
    "\n",
    "for col in ['output_qty', 'defect_qty', 'downtime_minutes']:\n",
    "    outliers, lower, upper = detect_outliers_iqr(production, col)\n",
    "    print(f'{col}: {len(outliers)} outlier(s) | Range valid: [{lower:.1f}, {upper:.1f}]')",
])
code([
    "# Penanganan outlier: clipping ke batas IQR\n",
    "for col in ['output_qty', 'defect_qty', 'downtime_minutes']:\n",
    "    Q1, Q3 = production[col].quantile(0.25), production[col].quantile(0.75)\n",
    "    IQR = Q3 - Q1\n",
    "    lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR\n",
    "    clipped = production[col].clip(lower=lower, upper=upper)\n",
    "    if col == 'downtime_minutes':\n",
    "        clipped = clipped.round(1)\n",
    "    changed = (production[col] != clipped).sum()\n",
    "    production[col] = clipped\n",
    "    print(f'{col}: {changed} nilai di-clip ke [{lower:.1f}, {upper:.1f}]')",
])

md(["---\n", "## 7. Validasi Business Rules"])
code([
    "# Business Rule 1: output_qty >= 0\n",
    "neg_output = (production['output_qty'] < 0).sum()\n",
    "print(f'1. Output negatif: {neg_output} baris')\n",
    "production.loc[production['output_qty'] < 0, 'output_qty'] = 0\n",
    "\n",
    "# Business Rule 2: defect_qty <= output_qty\n",
    "invalid_defect = (production['defect_qty'] > production['output_qty']).sum()\n",
    "print(f'2. Defect > Output: {invalid_defect} baris')\n",
    "mask = production['defect_qty'] > production['output_qty']\n",
    "production.loc[mask, 'defect_qty'] = production.loc[mask, 'output_qty']\n",
    "\n",
    "# Business Rule 3: downtime_minutes <= 480\n",
    "invalid_dt = (production['downtime_minutes'] > 480).sum()\n",
    "print(f'3. Downtime > 480 menit: {invalid_dt} baris')\n",
    "production.loc[production['downtime_minutes'] > 480, 'downtime_minutes'] = 480\n",
    "\n",
    "# Business Rule 4: tanggal dalam rentang H2 2024\n",
    "invalid_date = ((production['production_date'] < '2024-07-01') | (production['production_date'] > '2024-12-31')).sum()\n",
    "print(f'4. Tanggal di luar rentang: {invalid_date} baris')\n",
    "\n",
    "# Business Rule 5: FK valid\n",
    "for fk_col, valid_set, name in [\n",
    "    ('line_id', set(line_dim['line_id']), 'Line'),\n",
    "    ('machine_id', set(machine_dim['machine_id']), 'Machine'),\n",
    "    ('shift_id', set(shift_dim['shift_id']), 'Shift'),\n",
    "    ('product_id', set(product_dim['product_id']), 'Product'),\n",
    "]:\n",
    "    invalid = (~production[fk_col].isin(valid_set)).sum()\n",
    "    print(f'5. {name} ID tidak valid: {invalid} baris')",
])
code([
    "# Verifikasi akhir\n",
    "print('=== Verifikasi Business Rules (Pasca Cleaning) ===')\n",
    "print(f'Output negatif      : {(production[\"output_qty\"] < 0).sum()}')\n",
    "print(f'Defect > Output     : {(production[\"defect_qty\"] > production[\"output_qty\"]).sum()}')\n",
    "print(f'Downtime > 480 min  : {(production[\"downtime_minutes\"] > 480).sum()}')\n",
    "print(f'Missing values      : {production.isnull().sum().sum()}')\n",
    "checks = [(production['output_qty'] >= 0).all(), (production['defect_qty'] <= production['output_qty']).all(),\n",
    "           (production['downtime_minutes'] <= 480).all(), production.isnull().sum().sum() == 0]\n",
    "print('\\nSemua business rules terpenuhi!' if all(checks) else '\\nMasih ada pelanggaran!')",
])

md(["---\n", "## 8. Export Data Bersih"])
code([
    "production.to_csv(os.path.join(CLEAN_DIR, 'production_fact_cleaned.csv'), index=False)\n",
    "line_dim.to_csv(os.path.join(CLEAN_DIR, 'line_dim_cleaned.csv'), index=False)\n",
    "machine_dim.to_csv(os.path.join(CLEAN_DIR, 'machine_dim_cleaned.csv'), index=False)\n",
    "shift_dim.to_csv(os.path.join(CLEAN_DIR, 'shift_dim_cleaned.csv'), index=False)\n",
    "product_dim.to_csv(os.path.join(CLEAN_DIR, 'product_dim_cleaned.csv'), index=False)\n",
    "\n",
    "print('Data bersih disimpan ke:', CLEAN_DIR)\n",
    "for f in os.listdir(CLEAN_DIR):\n",
    "    size = os.path.getsize(os.path.join(CLEAN_DIR, f)) / 1024\n",
    "    print(f'  {f:40s} {size:8.1f} KB')",
])

md(["---\n", "## 9. Ringkasan Perubahan"])
code([
    "# Muat ulang data mentah untuk perbandingan\n",
    "raw = pd.read_csv(os.path.join(RAW_DIR, 'production_fact.csv'))\n",
    "\n",
    "# Hitung metrik raw data dengan aman\n",
    "raw_valid = raw.dropna(subset=['defect_qty', 'output_qty'])\n",
    "raw_defect_gt_output = (raw_valid['defect_qty'] > raw_valid['output_qty']).sum()\n",
    "\n",
    "summary = pd.DataFrame({\n",
    "    'Metrik': ['Jumlah baris', 'Missing values', 'Duplikat', 'Output negatif', 'Defect > Output', 'Downtime > 480'],\n",
    "    'Sebelum': [\n",
    "        f'{len(raw):,}', f'{raw.isnull().sum().sum():,}',\n",
    "        f'{raw.duplicated(subset=[c for c in raw.columns if c != \"production_id\"]).sum():,}',\n",
    "        f'{(raw[\"output_qty\"].dropna() < 0).sum():,}',\n",
    "        f'{raw_defect_gt_output:,}',\n",
    "        f'{(raw[\"downtime_minutes\"].dropna() > 480).sum():,}',\n",
    "    ],\n",
    "    'Sesudah': [\n",
    "        f'{len(production):,}', f'{production.isnull().sum().sum():,}',\n",
    "        f'{production.duplicated(subset=[c for c in production.columns if c != \"production_id\"]).sum():,}',\n",
    "        f'{(production[\"output_qty\"] < 0).sum():,}',\n",
    "        f'{(production[\"defect_qty\"] > production[\"output_qty\"]).sum():,}',\n",
    "        f'{(production[\"downtime_minutes\"] > 480).sum():,}',\n",
    "    ]\n",
    "})\n",
    "\n",
    "print('=' * 60)\n",
    "print('RINGKASAN DATA CLEANING')\n",
    "print('=' * 60)\n",
    "display(summary)",
])
code(["# Preview data bersih\n", "print('Preview data bersih:')\n", "production.head(10)"])
code(["production.describe()"])

md([
    "---\n",
    "## Kesimpulan Data Cleaning\n",
    "\n",
    "Data produksi PT Voltec Indonesia telah dibersihkan:\n",
    "\n",
    "1. **Missing values** ditangani dengan median grouping per konteks bisnis\n",
    "2. **Duplikat** dihapus berdasarkan semua kolom kecuali production_id\n",
    "3. **Tipe data** dikonversi ke format yang sesuai\n",
    "4. **Outlier** ditangani dengan IQR clipping\n",
    "5. **Business rules** divalidasi dan dikoreksi\n",
    "\n",
    "Data bersih siap untuk EDA, SQL Analysis, dan Dashboard Power BI.",
])

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"},
    },
    "nbformat": 4,
    "nbformat_minor": 4,
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cleaning.ipynb")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print(f"Notebook saved to: {out_path}")
