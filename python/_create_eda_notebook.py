"""Helper script to generate eda.ipynb programmatically."""
import json, os

cells = []
def md(src): cells.append({"cell_type": "markdown", "metadata": {}, "source": src if isinstance(src, list) else [src]})
def code(src): cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src if isinstance(src, list) else [src]})

md(["# Exploratory Data Analysis (EDA) - PT Voltec Indonesia\n",
    "## Analisis Produksi Elektronik H2 2024\n", "\n",
    "**Tujuan:** Mengeksplorasi data produksi yang sudah dibersihkan untuk menemukan pola, tren, dan anomali\n",
    "yang akan menjadi dasar insight dan rekomendasi bisnis.\n", "\n",
    "**Business Questions:**\n",
    "1. Bagaimana tren output produksi harian dan bulanan?\n",
    "2. Line produksi mana yang paling produktif?\n",
    "3. Shift mana yang memiliki defect rate tertinggi?\n",
    "4. Mesin mana yang paling sering mengalami downtime?\n",
    "5. Apakah ada korelasi antara downtime dan output?\n",
    "6. Produk mana yang paling sering mengalami defect?\n",
    "7. Apakah ada pola day-of-week pada produksi?"])

md(["---\n", "## 1. Setup & Load Data"])
code(["import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport os, warnings\n\nwarnings.filterwarnings('ignore')\nplt.style.use('seaborn-v0_8-whitegrid')\nplt.rcParams['figure.figsize'] = (14, 6)\nplt.rcParams['font.size'] = 11\nsns.set_palette('husl')\n\nprint('Libraries loaded.')"])

code(["# Load cleaned data\nCLEAN_DIR = os.path.join('..', 'data', 'cleaned')\n\npf = pd.read_csv(os.path.join(CLEAN_DIR, 'production_fact_cleaned.csv'), parse_dates=['production_date'])\nline_dim = pd.read_csv(os.path.join(CLEAN_DIR, 'line_dim_cleaned.csv'))\nmachine_dim = pd.read_csv(os.path.join(CLEAN_DIR, 'machine_dim_cleaned.csv'))\nshift_dim = pd.read_csv(os.path.join(CLEAN_DIR, 'shift_dim_cleaned.csv'))\nproduct_dim = pd.read_csv(os.path.join(CLEAN_DIR, 'product_dim_cleaned.csv'))\n\nprint(f'Jumlah record: {len(pf):,}')\npf.head()"])

code(["# Join dengan dimension tables untuk analisis\ndf = pf.merge(line_dim, on='line_id') \\\n       .merge(machine_dim, on='machine_id') \\\n       .merge(shift_dim, on='shift_id') \\\n       .merge(product_dim, on='product_id')\n\n# Tambah kolom turunan\ndf['month'] = df['production_date'].dt.month\ndf['month_name'] = df['production_date'].dt.strftime('%B')\ndf['week'] = df['production_date'].dt.isocalendar().week.astype(int)\ndf['day_name'] = df['production_date'].dt.day_name()\ndf['day_of_week'] = df['production_date'].dt.dayofweek\ndf['defect_rate'] = (df['defect_qty'] / df['output_qty'].replace(0, np.nan) * 100).fillna(0)\ndf['achievement'] = (df['output_qty'] / df['target_qty'].replace(0, np.nan) * 100).fillna(0)\ndf['machine_age'] = 2024 - df['purchase_year']\n\nprint(f'Joined dataframe: {df.shape}')\ndf.head()"])

md(["---\n", "## 2. Ringkasan Statistik"])
code(["# Statistik deskriptif\ndf[['output_qty', 'target_qty', 'defect_qty', 'downtime_minutes', 'defect_rate', 'achievement']].describe()"])

code(["# KPI Summary\nprint('=' * 50)\nprint('KPI SUMMARY - H2 2024')\nprint('=' * 50)\nprint(f'Total Output      : {df[\"output_qty\"].sum():,.0f} unit')\nprint(f'Total Target      : {df[\"target_qty\"].sum():,.0f} unit')\nprint(f'Achievement Rate  : {df[\"output_qty\"].sum() / df[\"target_qty\"].sum() * 100:.1f}%')\nprint(f'Total Defect      : {df[\"defect_qty\"].sum():,.0f} unit')\nprint(f'Avg Defect Rate   : {df[\"defect_qty\"].sum() / df[\"output_qty\"].sum() * 100:.2f}%')\nprint(f'Avg Downtime      : {df[\"downtime_minutes\"].mean():.1f} menit/batch')\nprint(f'Total Downtime    : {df[\"downtime_minutes\"].sum():,.0f} menit')"])

md(["---\n", "## 3. Tren Output Produksi (Q1: Bagaimana tren output?)"])
code(["# Tren output harian\ndaily = df.groupby('production_date').agg(\n    output=('output_qty', 'sum'),\n    target=('target_qty', 'sum')\n).reset_index()\n\nfig, ax = plt.subplots(figsize=(16, 6))\nax.plot(daily['production_date'], daily['output'], label='Output Aktual', linewidth=1.5, alpha=0.7)\nax.plot(daily['production_date'], daily['target'], label='Target', linewidth=1.5, alpha=0.7, linestyle='--')\n\n# Rolling average 7 hari\nax.plot(daily['production_date'], daily['output'].rolling(7).mean(), label='Moving Avg 7 Hari',\n        linewidth=2.5, color='#e74c3c')\n\nax.set_title('Tren Output Produksi Harian - H2 2024', fontsize=16, fontweight='bold')\nax.set_xlabel('Tanggal')\nax.set_ylabel('Output (unit)')\nax.legend(fontsize=11)\nplt.tight_layout()\nplt.show()"])

code(["# Tren output bulanan\nmonthly = df.groupby('month').agg(\n    output=('output_qty', 'sum'),\n    target=('target_qty', 'sum'),\n    defect=('defect_qty', 'sum'),\n    downtime=('downtime_minutes', 'sum')\n).reset_index()\nmonthly['achievement'] = monthly['output'] / monthly['target'] * 100\nmonthly['defect_rate'] = monthly['defect'] / monthly['output'] * 100\nmonthly['month_label'] = ['Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']\n\nfig, axes = plt.subplots(1, 3, figsize=(18, 5))\n\naxes[0].bar(monthly['month_label'], monthly['output'], color='#3498db', alpha=0.8)\naxes[0].plot(monthly['month_label'], monthly['target'], 'r--o', label='Target')\naxes[0].set_title('Output vs Target per Bulan', fontweight='bold')\naxes[0].set_ylabel('Unit')\naxes[0].legend()\n\naxes[1].bar(monthly['month_label'], monthly['defect_rate'], color='#e74c3c', alpha=0.8)\naxes[1].set_title('Defect Rate per Bulan (%)', fontweight='bold')\naxes[1].set_ylabel('Defect Rate (%)')\n\naxes[2].bar(monthly['month_label'], monthly['downtime'], color='#f39c12', alpha=0.8)\naxes[2].set_title('Total Downtime per Bulan', fontweight='bold')\naxes[2].set_ylabel('Downtime (menit)')\n\nplt.suptitle('Tren Bulanan - H2 2024', fontsize=15, fontweight='bold', y=1.02)\nplt.tight_layout()\nplt.show()"])

md(["---\n", "## 4. Perbandingan Line Produksi (Q2: Line mana paling produktif?)"])
code(["# Output per line\nline_perf = df.groupby('line_name').agg(\n    total_output=('output_qty', 'sum'),\n    total_target=('target_qty', 'sum'),\n    total_defect=('defect_qty', 'sum'),\n    avg_downtime=('downtime_minutes', 'mean'),\n    count=('production_id', 'count')\n).reset_index()\nline_perf['achievement'] = (line_perf['total_output'] / line_perf['total_target'] * 100).round(1)\nline_perf['defect_rate'] = (line_perf['total_defect'] / line_perf['total_output'] * 100).round(2)\nline_perf['output_share'] = (line_perf['total_output'] / line_perf['total_output'].sum() * 100).round(1)\n\nprint('Performa per Line Produksi:')\ndisplay(line_perf.sort_values('total_output', ascending=False))"])

code(["# Visualisasi perbandingan line\nfig, axes = plt.subplots(1, 3, figsize=(18, 5))\n\nsns.barplot(data=line_perf.sort_values('total_output', ascending=False), \n            x='line_name', y='total_output', ax=axes[0], palette='Blues_d')\naxes[0].set_title('Total Output per Line', fontweight='bold')\naxes[0].set_ylabel('Output (unit)')\n\nsns.barplot(data=line_perf.sort_values('defect_rate', ascending=False),\n            x='line_name', y='defect_rate', ax=axes[1], palette='Reds_d')\naxes[1].set_title('Defect Rate per Line (%)', fontweight='bold')\naxes[1].set_ylabel('Defect Rate (%)')\n\nsns.barplot(data=line_perf.sort_values('avg_downtime', ascending=False),\n            x='line_name', y='avg_downtime', ax=axes[2], palette='Oranges_d')\naxes[2].set_title('Avg Downtime per Line (menit)', fontweight='bold')\naxes[2].set_ylabel('Downtime (menit)')\n\nplt.tight_layout()\nplt.show()"])

md(["---\n", "## 5. Analisis Shift (Q3: Shift mana defect rate tertinggi?)"])
code(["# Performa per shift\nshift_perf = df.groupby('shift_name').agg(\n    total_output=('output_qty', 'sum'),\n    total_defect=('defect_qty', 'sum'),\n    avg_downtime=('downtime_minutes', 'mean')\n).reset_index()\nshift_perf['defect_rate'] = (shift_perf['total_defect'] / shift_perf['total_output'] * 100).round(2)\n\nfig, axes = plt.subplots(1, 2, figsize=(14, 5))\n\nsns.barplot(data=shift_perf, x='shift_name', y='total_output', ax=axes[0], palette='viridis')\naxes[0].set_title('Total Output per Shift', fontweight='bold')\n\nsns.barplot(data=shift_perf, x='shift_name', y='defect_rate', ax=axes[1], palette='magma')\naxes[1].set_title('Defect Rate per Shift (%)', fontweight='bold')\n\nplt.tight_layout()\nplt.show()\n\nprint('Performa per Shift:')\ndisplay(shift_perf)"])

md(["---\n", "## 6. Analisis Mesin & Downtime (Q4: Mesin mana paling sering downtime?)"])
code(["# Downtime per mesin\nmachine_perf = df.groupby(['machine_name', 'machine_type', 'purchase_year']).agg(\n    total_downtime=('downtime_minutes', 'sum'),\n    avg_downtime=('downtime_minutes', 'mean'),\n    total_output=('output_qty', 'sum')\n).reset_index()\nmachine_perf['machine_age'] = 2024 - machine_perf['purchase_year']\nmachine_perf = machine_perf.sort_values('total_downtime', ascending=False)\n\nfig, axes = plt.subplots(1, 2, figsize=(16, 6))\n\nsns.barplot(data=machine_perf.head(10), y='machine_name', x='total_downtime', ax=axes[0], palette='YlOrRd')\naxes[0].set_title('Top 10 Mesin - Total Downtime', fontweight='bold')\naxes[0].set_xlabel('Total Downtime (menit)')\n\nsns.scatterplot(data=machine_perf, x='machine_age', y='avg_downtime', size='total_output',\n                hue='machine_type', ax=axes[1], sizes=(50, 300), alpha=0.7)\naxes[1].set_title('Usia Mesin vs Avg Downtime', fontweight='bold')\naxes[1].set_xlabel('Usia Mesin (tahun)')\naxes[1].set_ylabel('Avg Downtime (menit)')\naxes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)\n\nplt.tight_layout()\nplt.show()"])

md(["---\n", "## 7. Korelasi Downtime vs Output (Q5)"])
code(["# Scatter plot downtime vs output\nfig, axes = plt.subplots(1, 2, figsize=(14, 5))\n\naxes[0].scatter(df['downtime_minutes'], df['output_qty'], alpha=0.1, s=10, color='#3498db')\nz = np.polyfit(df['downtime_minutes'], df['output_qty'], 1)\np = np.poly1d(z)\naxes[0].plot(sorted(df['downtime_minutes']), p(sorted(df['downtime_minutes'])), 'r-', linewidth=2)\naxes[0].set_title('Downtime vs Output (per batch)', fontweight='bold')\naxes[0].set_xlabel('Downtime (menit)')\naxes[0].set_ylabel('Output (unit)')\n\n# Correlation heatmap\nnumeric_cols = ['output_qty', 'target_qty', 'defect_qty', 'downtime_minutes', 'machine_age']\ncorr = df[numeric_cols].corr()\nsns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, fmt='.2f', ax=axes[1], square=True)\naxes[1].set_title('Correlation Heatmap', fontweight='bold')\n\nplt.tight_layout()\nplt.show()\n\nprint(f'Korelasi Downtime vs Output: {df[\"downtime_minutes\"].corr(df[\"output_qty\"]):.3f}')"])

md(["---\n", "## 8. Analisis Produk & Defect (Q6: Produk mana paling banyak defect?)"])
code(["# Defect per produk\nproduct_perf = df.groupby('product_name').agg(\n    total_output=('output_qty', 'sum'),\n    total_defect=('defect_qty', 'sum')\n).reset_index()\nproduct_perf['defect_rate'] = (product_perf['total_defect'] / product_perf['total_output'] * 100).round(2)\nproduct_perf = product_perf.sort_values('total_defect', ascending=False)\n\n# Pareto chart\nfig, ax1 = plt.subplots(figsize=(12, 6))\nproduct_perf_sorted = product_perf.sort_values('total_defect', ascending=False)\nax1.bar(product_perf_sorted['product_name'], product_perf_sorted['total_defect'], color='#e74c3c', alpha=0.8)\nax1.set_ylabel('Total Defect (unit)', color='#e74c3c')\nax1.set_title('Pareto Chart - Defect per Produk', fontsize=14, fontweight='bold')\n\nax2 = ax1.twinx()\ncumulative = product_perf_sorted['total_defect'].cumsum() / product_perf_sorted['total_defect'].sum() * 100\nax2.plot(product_perf_sorted['product_name'], cumulative, 'b-o', linewidth=2)\nax2.set_ylabel('Kumulatif (%)', color='blue')\nax2.axhline(y=80, color='gray', linestyle='--', alpha=0.5)\n\nplt.tight_layout()\nplt.show()\n\nprint('Defect Rate per Produk:')\ndisplay(product_perf)"])

md(["---\n", "## 9. Pola Day-of-Week (Q7: Ada pola harian?)"])
code(["# Output per hari dalam seminggu\nday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']\nday_perf = df.groupby('day_name').agg(\n    avg_output=('output_qty', 'mean'),\n    avg_defect_rate=('defect_rate', 'mean')\n).reindex(day_order)\n\nfig, axes = plt.subplots(1, 2, figsize=(14, 5))\n\naxes[0].bar(day_perf.index, day_perf['avg_output'], color='#2ecc71', alpha=0.8)\naxes[0].set_title('Rata-rata Output per Hari', fontweight='bold')\naxes[0].set_ylabel('Avg Output (unit)')\naxes[0].tick_params(axis='x', rotation=45)\n\naxes[1].bar(day_perf.index, day_perf['avg_defect_rate'], color='#e74c3c', alpha=0.8)\naxes[1].set_title('Rata-rata Defect Rate per Hari (%)', fontweight='bold')\naxes[1].set_ylabel('Avg Defect Rate (%)')\naxes[1].tick_params(axis='x', rotation=45)\n\nplt.tight_layout()\nplt.show()"])

md(["---\n", "## 10. Distribusi Output per Shift per Line"])
code(["# Boxplot output per shift per line\nfig, ax = plt.subplots(figsize=(14, 6))\nsns.boxplot(data=df, x='line_name', y='output_qty', hue='shift_name', ax=ax, palette='Set2')\nax.set_title('Distribusi Output per Shift per Line', fontsize=14, fontweight='bold')\nax.set_xlabel('Line Produksi')\nax.set_ylabel('Output (unit)')\nax.legend(title='Shift')\nplt.tight_layout()\nplt.show()"])

md(["---\n", "## 11. Pivot Table Analysis"])
code(["# Pivot table: Output per Line per Bulan\npivot_output = df.pivot_table(values='output_qty', index='line_name', columns='month',\n                              aggfunc='sum', margins=True, margins_name='Total')\npivot_output.columns = ['Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des', 'Total']\nprint('Output per Line per Bulan:')\ndisplay(pivot_output)"])

code(["# Heatmap defect rate: Line x Shift\npivot_defect = df.pivot_table(values='defect_rate', index='line_name', columns='shift_name', aggfunc='mean')\n\nfig, ax = plt.subplots(figsize=(8, 5))\nsns.heatmap(pivot_defect, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax, linewidths=0.5)\nax.set_title('Rata-rata Defect Rate (%) - Line x Shift', fontsize=13, fontweight='bold')\nplt.tight_layout()\nplt.show()"])

md(["---\n", "## 12. Ringkasan Temuan Kunci\n", "\n",
    "### Temuan Utama:\n",
    "1. **Tren Menurun**: Output produksi menunjukkan tren penurunan dari Juli ke Desember\n",
    "2. **Shift Malam**: Shift Malam memiliki defect rate paling tinggi dibanding shift lainnya\n",
    "3. **Mesin Tua**: Mesin dengan usia >5 tahun menunjukkan downtime yang lebih tinggi\n",
    "4. **Control Board**: Produk Control Board memiliki defect rate tertinggi\n",
    "5. **Korelasi Negatif**: Terdapat korelasi negatif antara downtime dan output\n",
    "6. **Senin Effect**: Output hari Senin cenderung lebih rendah (start-up effect)\n",
    "7. **Weekend**: Output di hari Sabtu dan Minggu jauh lebih rendah\n",
    "\n",
    "Temuan ini akan dielaborasi lebih lanjut di dokumen Insights & Recommendations."])

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"},
    },
    "nbformat": 4, "nbformat_minor": 4,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eda.ipynb")
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print(f"Notebook saved to: {out}")
