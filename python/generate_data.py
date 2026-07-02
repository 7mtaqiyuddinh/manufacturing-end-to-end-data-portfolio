"""
==============================================================================
PT Voltec Indonesia - Synthetic Production Data Generator
==============================================================================

Script ini menghasilkan data sintetis untuk analisis produksi elektronik.
Data dirancang agar memiliki pola-pola realistis yang bisa ditemukan
saat proses Exploratory Data Analysis (EDA) dan SQL Analysis.

Pola yang di-inject:
  1. Tren output menurun ~12% dari Oktober ke Desember 2024
  2. Shift 3 (malam) memiliki defect rate lebih tinggi
  3. Mesin lama (pre-2020) memiliki downtime lebih tinggi
  4. Produk "Control Board" memiliki defect rate tertinggi
  5. Line A memiliki output tertinggi tapi declining di Desember
  6. Output hari Senin lebih rendah (start-up effect)
  7. Korelasi negatif antara downtime dan output

Output:
  - data/raw/production_fact.csv
  - data/raw/line_dim.csv
  - data/raw/machine_dim.csv
  - data/raw/shift_dim.csv
  - data/raw/product_dim.csv

Author : [Your Name]
Date   : 2024
==============================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings

warnings.filterwarnings("ignore")
np.random.seed(42)

# ==============================================================================
# Konfigurasi Path
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)


# ==============================================================================
# 1. DIMENSION TABLES
# ==============================================================================

def create_line_dim():
    """Membuat tabel dimensi line produksi."""
    data = {
        "line_id": [1, 2, 3, 4, 5],
        "line_name": ["Line A", "Line B", "Line C", "Line D", "Line E"],
        "supervisor": [
            "Budi Santoso", "Siti Rahayu", "Ahmad Wijaya",
            "Dewi Kusuma", "Rizky Pratama",
        ],
        "capacity_per_shift": [520, 480, 500, 460, 440],
    }
    return pd.DataFrame(data)


def create_machine_dim():
    """Membuat tabel dimensi mesin."""
    data = {
        "machine_id": list(range(1, 16)),
        "machine_name": [
            "SMT-01", "SMT-02", "SMT-03",
            "WAVE-01", "WAVE-02", "WAVE-03",
            "AOI-01", "AOI-02",
            "ICT-01", "ICT-02",
            "REFLOW-01", "REFLOW-02", "REFLOW-03",
            "PRESS-01", "PACK-01",
        ],
        "machine_type": [
            "SMT Placement", "SMT Placement", "SMT Placement",
            "Wave Soldering", "Wave Soldering", "Wave Soldering",
            "Inspection", "Inspection",
            "Testing", "Testing",
            "Reflow Oven", "Reflow Oven", "Reflow Oven",
            "Press", "Packaging",
        ],
        "purchase_year": [
            2018, 2021, 2023,
            2017, 2020, 2022,
            2019, 2023,
            2018, 2021,
            2016, 2020, 2024,
            2019, 2022,
        ],
        "status": ["Active"] * 15,
    }
    return pd.DataFrame(data)


def create_shift_dim():
    """Membuat tabel dimensi shift."""
    data = {
        "shift_id": [1, 2, 3],
        "shift_name": ["Shift Pagi", "Shift Siang", "Shift Malam"],
        "start_time": ["06:00", "14:00", "22:00"],
        "end_time": ["14:00", "22:00", "06:00"],
    }
    return pd.DataFrame(data)


def create_product_dim():
    """Membuat tabel dimensi produk."""
    data = {
        "product_id": [1, 2, 3, 4, 5],
        "product_name": [
            "PCB Assembly", "Sensor Module", "Power Supply Unit",
            "LED Panel", "Control Board",
        ],
        "category": ["Assembly", "Component", "Power", "Display", "Controller"],
        "unit_cost": [25000, 45000, 78000, 35000, 120000],
    }
    return pd.DataFrame(data)


# ==============================================================================
# 2. FACT TABLE - PRODUCTION DATA
# ==============================================================================

def generate_production_fact(line_dim, machine_dim, shift_dim, product_dim):
    """
    Menghasilkan data fakta produksi dengan pola realistis.
    Setiap record = 1 batch produksi (date x line x shift x machine x product).
    Target: ~30.000 baris.
    """
    # Rentang tanggal: H2 2024 (1 Juli - 31 Desember)
    dates = pd.date_range(start="2024-07-01", end="2024-12-31", freq="D")

    # Mapping mesin ke line (3 mesin per line)
    line_machine_map = {
        1: [1, 2, 3],    # Line A: SMT-01, SMT-02, SMT-03
        2: [4, 5, 6],    # Line B: WAVE-01, WAVE-02, WAVE-03
        3: [7, 8, 9],    # Line C: AOI-01, AOI-02, ICT-01
        4: [10, 11, 12], # Line D: ICT-02, REFLOW-01, REFLOW-02
        5: [13, 14, 15], # Line E: REFLOW-03, PRESS-01, PACK-01
    }

    line_capacity = dict(zip(line_dim["line_id"], line_dim["capacity_per_shift"]))
    machine_years = dict(zip(machine_dim["machine_id"], machine_dim["purchase_year"]))

    # Produk yang diproduksi oleh tiap line (2-3 produk per line)
    line_products = {
        1: [1, 2, 5],    # Line A: PCB Assembly, Sensor Module, Control Board
        2: [2, 3, 4],    # Line B: Sensor Module, Power Supply, LED Panel
        3: [3, 1, 5],    # Line C: Power Supply, PCB Assembly, Control Board
        4: [4, 2, 3],    # Line D: LED Panel, Sensor Module, Power Supply
        5: [5, 1, 4],    # Line E: Control Board, PCB Assembly, LED Panel
    }

    product_defect_base = {
        1: 0.030, 2: 0.035, 3: 0.025, 4: 0.028, 5: 0.065,
    }

    shift_defect_mult = {1: 0.8, 2: 1.0, 3: 1.6}
    shift_output_mult = {1: 1.05, 2: 1.00, 3: 0.90}

    records = []
    pid = 1

    for date in dates:
        dow = date.dayofweek
        month = date.month

        # Tren bulanan: stabil Jul-Sep, menurun Oct-Dec
        trend_map = {7: 1.02, 8: 1.00, 9: 0.99, 10: 0.96, 11: 0.91, 12: 0.85}
        monthly_trend = trend_map[month]

        # Day-of-week effect
        if dow == 0:      dow_factor = 0.88   # Senin
        elif dow == 5:    dow_factor = 0.55   # Sabtu
        elif dow == 6:    dow_factor = 0.30   # Minggu
        else:             dow_factor = 1.00   # Sel-Jum

        for line_id, machine_ids in line_machine_map.items():
            line_factor = 1.0
            if line_id == 1 and month == 12:
                line_factor = 0.80

            products = line_products[line_id]
            capacity = line_capacity[line_id]

            for shift_id in [1, 2, 3]:
                for machine_id in machine_ids:
                    machine_age = 2024 - machine_years[machine_id]

                    # Hitung downtime berdasarkan usia mesin (shared across products)
                    if machine_age > 5:
                        dt_base = np.random.exponential(scale=45)
                    elif machine_age > 3:
                        dt_base = np.random.exponential(scale=25)
                    else:
                        dt_base = np.random.exponential(scale=12)
                    downtime = max(0, min(dt_base + np.random.normal(0, 5), 480))
                    downtime = round(downtime, 1)

                    # Setiap mesin produce semua produk yang ditangani line-nya
                    for product_id in products:
                        # Hitung target (per mesin per produk)
                        per_machine_cap = capacity / len(machine_ids)
                        per_product_cap = per_machine_cap / len(products)
                        target = int(per_product_cap * shift_output_mult[shift_id] * dow_factor)

                        # Hitung output
                        dt_penalty = 1 - (downtime / 480) * 0.7
                        noise = np.random.normal(1.0, 0.08)
                        output = int(
                            per_product_cap * monthly_trend * shift_output_mult[shift_id]
                            * dow_factor * line_factor * dt_penalty * noise
                        )
                        output = max(0, output)

                        # Hitung defect
                        dr = (product_defect_base[product_id]
                              * shift_defect_mult[shift_id]
                              * (1 + machine_age * 0.02)
                              * monthly_trend ** (-0.5))
                        dr *= np.random.lognormal(0, 0.3)
                        dr = min(dr, 0.25)
                        defect = max(0, min(int(output * dr), output))

                        records.append({
                            "production_id": pid,
                            "production_date": date.strftime("%Y-%m-%d"),
                            "line_id": line_id,
                            "machine_id": machine_id,
                            "shift_id": shift_id,
                            "product_id": product_id,
                            "target_qty": target,
                            "output_qty": output,
                            "defect_qty": defect,
                            "downtime_minutes": downtime,
                        })
                    pid += 1

    return pd.DataFrame(records)


# ==============================================================================
# 3. INJECT DATA QUALITY ISSUES (untuk latihan cleaning)
# ==============================================================================

def inject_data_issues(df):
    """
    Menyisipkan masalah kualitas data yang realistis untuk latihan cleaning.
    """
    df_dirty = df.copy()
    n = len(df_dirty)
    print(f"\n  Jumlah baris asli: {n:,}")

    # Missing values
    for col, pct in [("output_qty", 0.02), ("defect_qty", 0.015),
                     ("downtime_minutes", 0.01), ("machine_id", 0.005)]:
        idx = np.random.choice(n, size=int(n * pct), replace=False)
        df_dirty.loc[idx, col] = np.nan
    print(f"  Missing values disisipi: ~{int(n * 0.045)}")

    # Duplikat (~80 baris)
    dup_idx = np.random.choice(n, size=80, replace=False)
    df_dirty = pd.concat([df_dirty, df_dirty.iloc[dup_idx].copy()], ignore_index=True)
    print(f"  Duplikat disisipi: 80")

    # Nilai negatif (error input) - 20 baris
    neg_idx = np.random.choice(len(df_dirty), size=20, replace=False)
    df_dirty.loc[neg_idx, "output_qty"] = df_dirty.loc[neg_idx, "output_qty"].apply(
        lambda x: -abs(np.random.randint(10, 100)) if pd.notna(x) else x
    )
    print(f"  Nilai negatif disisipi: 20")

    # Outlier downtime > 480
    out_idx = np.random.choice(len(df_dirty), size=15, replace=False)
    df_dirty.loc[out_idx, "downtime_minutes"] = np.random.uniform(500, 900, size=15)
    print(f"  Outlier downtime disisipi: 15")

    # Defect > Output (invalid)
    inv_idx = np.random.choice(len(df_dirty), size=18, replace=False)
    for idx in inv_idx:
        if pd.notna(df_dirty.loc[idx, "output_qty"]) and df_dirty.loc[idx, "output_qty"] > 0:
            df_dirty.loc[idx, "defect_qty"] = (
                abs(df_dirty.loc[idx, "output_qty"]) + np.random.randint(50, 200)
            )
    print(f"  Defect > Output disisipi: 18")

    # Shuffle dan re-assign ID
    df_dirty = df_dirty.sample(frac=1, random_state=42).reset_index(drop=True)
    df_dirty["production_id"] = range(1, len(df_dirty) + 1)
    print(f"  Jumlah baris akhir: {len(df_dirty):,}")
    return df_dirty


# ==============================================================================
# 4. MAIN
# ==============================================================================

def main():
    print("=" * 60)
    print("PT Voltec Indonesia - Data Generator")
    print("=" * 60)

    print("\n[1/4] Membuat dimension tables...")
    line_dim = create_line_dim()
    machine_dim = create_machine_dim()
    shift_dim = create_shift_dim()
    product_dim = create_product_dim()
    for name, df in [("line_dim", line_dim), ("machine_dim", machine_dim),
                     ("shift_dim", shift_dim), ("product_dim", product_dim)]:
        print(f"  {name:15s}: {len(df)} baris")

    print("\n[2/4] Menghasilkan production_fact...")
    pf = generate_production_fact(line_dim, machine_dim, shift_dim, product_dim)
    print(f"  production_fact : {len(pf):,} baris")

    print("\n[3/4] Menyisipkan masalah kualitas data...")
    pf_dirty = inject_data_issues(pf)

    print("\n[4/4] Menyimpan ke CSV...")
    line_dim.to_csv(os.path.join(RAW_DIR, "line_dim.csv"), index=False)
    machine_dim.to_csv(os.path.join(RAW_DIR, "machine_dim.csv"), index=False)
    shift_dim.to_csv(os.path.join(RAW_DIR, "shift_dim.csv"), index=False)
    product_dim.to_csv(os.path.join(RAW_DIR, "product_dim.csv"), index=False)
    pf_dirty.to_csv(os.path.join(RAW_DIR, "production_fact.csv"), index=False)

    print(f"\n  Files disimpan di: {RAW_DIR}")
    for f in os.listdir(RAW_DIR):
        size_kb = os.path.getsize(os.path.join(RAW_DIR, f)) / 1024
        print(f"    {f:30s} {size_kb:8.1f} KB")

    print("\n" + "=" * 60)
    print("RINGKASAN DATA")
    print("=" * 60)
    print(f"\nPeriode       : 1 Juli - 31 Desember 2024 ({len(pd.date_range('2024-07-01','2024-12-31'))} hari)")
    print(f"Total records : {len(pf_dirty):,}")
    print(f"Lines / Mesin / Shift / Produk : {len(line_dim)} / {len(machine_dim)} / {len(shift_dim)} / {len(product_dim)}")
    print(f"\n--- Statistik Data Bersih (sebelum inject issues) ---")
    print(f"Total Output  : {pf['output_qty'].sum():,.0f} unit")
    print(f"Total Target  : {pf['target_qty'].sum():,.0f} unit")
    ach = pf['output_qty'].sum() / pf['target_qty'].sum() * 100
    print(f"Achievement   : {ach:.1f}%")
    print(f"Avg Defect %  : {(pf['defect_qty'].sum() / pf['output_qty'].sum() * 100):.2f}%")
    print(f"Avg Downtime  : {pf['downtime_minutes'].mean():.1f} menit/shift")
    print("\n[DONE] Data generation selesai!")
    print("=" * 60)


if __name__ == "__main__":
    main()
