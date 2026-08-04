import pandas as pd

df = pd.read_csv(r"q:\Data Science\Production\data\cleaned\production_fact_cleaned.csv")
# Group by machine_id and show count, sum, mean of downtime_minutes
machine_dim = pd.read_csv(r"q:\Data Science\Production\data\cleaned\machine_dim_cleaned.csv")
merged = df.merge(machine_dim, on='machine_id')
summary = merged.groupby('machine_name').agg(
    count=('downtime_minutes', 'count'),
    sum=('downtime_minutes', 'sum'),
    mean=('downtime_minutes', 'mean')
).reset_index()
print(summary)
