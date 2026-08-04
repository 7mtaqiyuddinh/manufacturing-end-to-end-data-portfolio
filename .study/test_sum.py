import pandas as pd

df = pd.read_csv(r"q:\Data Science\Production\data\cleaned\production_fact_cleaned.csv")
print("Total rows:", len(df))
print("Sum of output_qty:", df['output_qty'].sum())
print("Sum of defect_qty:", df['defect_qty'].sum())
print("Sum of downtime_minutes:", df['downtime_minutes'].sum())
print("Sum of downtime_minutes for machine_id 4 (WAVE-01):", df[df['machine_id'] == 4]['downtime_minutes'].sum())
print("Sum of downtime_minutes for machine_id 7 (AOI-01):", df[df['machine_id'] == 7]['downtime_minutes'].sum())
