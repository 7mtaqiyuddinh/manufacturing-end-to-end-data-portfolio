-- ==============================================================================
-- PT Voltec Indonesia - Database Views
-- Analisis Produksi Elektronik H2 2024
-- ==============================================================================
-- File ini berisi DDL untuk membuat views analisis di database.
-- Views ini digunakan untuk menyederhanakan akses data bagi visualisasi
-- di Power BI atau report analytics rutin.
-- ==============================================================================

-- Drop views jika sudah ada
DROP VIEW IF EXISTS v_monthly_executive_kpi;
DROP VIEW IF EXISTS v_line_shift_performance;
DROP VIEW IF EXISTS v_machine_maintenance_priority;
DROP VIEW IF EXISTS v_product_defect_summary;


-- ==============================================================================
-- 1. VIEW: Ringkasan Eksekutif Bulanan (Monthly Executive KPI)
-- ==============================================================================
-- Menyajikan KPI produksi bulanan yang mencakup pencapaian target (achievement rate)
-- dan tingkat defect (defect rate).
-- ==============================================================================
CREATE VIEW v_monthly_executive_kpi AS
SELECT
    EXTRACT(MONTH FROM production_date) AS month_num,
    SUM(output_qty) AS total_output,
    SUM(target_qty) AS total_target,
    ROUND(SUM(output_qty) * 100.0 / SUM(target_qty), 1) AS achievement_pct,
    SUM(defect_qty) AS total_defect,
    ROUND(SUM(defect_qty) * 100.0 / SUM(output_qty), 2) AS defect_rate_pct,
    ROUND(AVG(downtime_minutes), 1) AS avg_downtime,
    ROUND(SUM(downtime_minutes), 0) AS total_downtime,
    COUNT(DISTINCT production_date) AS working_days,
    CASE
        WHEN SUM(output_qty) * 100.0 / SUM(target_qty) >= 95 THEN 'GREEN'
        WHEN SUM(output_qty) * 100.0 / SUM(target_qty) >= 85 THEN 'YELLOW'
        ELSE 'RED'
    END AS status_flag
FROM production_fact
GROUP BY EXTRACT(MONTH FROM production_date);


-- ==============================================================================
-- 2. VIEW: Performa Kombinasi Lini & Shift (Line-Shift Performance)
-- ==============================================================================
-- Mengidentifikasi kombinasi lini perakitan dan shift kerja yang memiliki output 
-- tertinggi serta tingkat defect paling kritis.
-- ==============================================================================
CREATE VIEW v_line_shift_performance AS
SELECT
    l.line_name,
    s.shift_name,
    SUM(pf.output_qty) AS total_output,
    SUM(pf.target_qty) AS total_target,
    ROUND(SUM(pf.output_qty) * 100.0 / SUM(pf.target_qty), 1) AS achievement_pct,
    SUM(pf.defect_qty) AS total_defect,
    ROUND(SUM(pf.defect_qty) * 100.0 / SUM(pf.output_qty), 2) AS defect_rate_pct,
    ROUND(AVG(pf.downtime_minutes), 1) AS avg_downtime_min
FROM production_fact pf
JOIN line_dim l ON pf.line_id = l.line_id
JOIN shift_dim s ON pf.shift_id = s.shift_id
GROUP BY l.line_name, s.shift_name;


-- ==============================================================================
-- 3. VIEW: Prioritas Pemeliharaan Mesin (Machine Maintenance Priority)
-- ==============================================================================
-- Mengklasifikasikan mesin yang membutuhkan perawatan berdasarkan umur mesin
-- dan rata-rata durasi downtime.
-- ==============================================================================
CREATE VIEW v_machine_maintenance_priority AS
WITH machine_stats AS (
    SELECT
        pf.line_id,
        l.line_name,
        m.machine_name,
        m.machine_type,
        (2024 - m.purchase_year) AS machine_age,
        AVG(pf.downtime_minutes) AS avg_downtime,
        AVG(pf.output_qty) AS avg_output,
        COUNT(*) AS batch_count
    FROM production_fact pf
    JOIN line_dim l ON pf.line_id = l.line_id
    JOIN machine_dim m ON pf.machine_id = m.machine_id
    GROUP BY pf.line_id, l.line_name, m.machine_name, m.machine_type, m.purchase_year
)
SELECT
    line_name,
    machine_name,
    machine_type,
    machine_age,
    ROUND(avg_downtime, 1) AS avg_downtime_min,
    ROUND(avg_output, 0) AS avg_output_units,
    batch_count,
    CASE
        WHEN machine_age > 5 AND avg_downtime > 30 THEN 'PRIORITAS TINGGI - Perlu preventive maintenance segera'
        WHEN machine_age > 3 AND avg_downtime > 20 THEN 'PRIORITAS SEDANG - Jadwalkan maintenance rutin'
        ELSE 'NORMAL - Lanjutkan monitoring'
    END AS maintenance_recommendation
FROM machine_stats;


-- ==============================================================================
-- 4. VIEW: Ringkasan Defect dan Biaya Kerugian per Produk (Product Defect & Cost Summary)
-- ==============================================================================
-- Menganalisis tingkat kecacatan produk beserta kerugian finansial akibat defect.
-- Berguna bagi Quality Control & Divisi Keuangan.
-- ==============================================================================
CREATE VIEW v_product_defect_summary AS
SELECT
    p.product_name,
    p.category,
    SUM(pf.output_qty) AS total_output,
    SUM(pf.defect_qty) AS total_defect,
    ROUND(SUM(pf.defect_qty) * 100.0 / SUM(pf.output_qty), 2) AS defect_rate_pct,
    p.unit_cost AS cost_per_unit_idr,
    ROUND(SUM(pf.defect_qty) * p.unit_cost, 0) AS total_defect_cost_idr
FROM production_fact pf
JOIN product_dim p ON pf.product_id = p.product_id
GROUP BY p.product_name, p.category, p.unit_cost;
