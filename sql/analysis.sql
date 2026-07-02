-- ==============================================================================
-- PT Voltec Indonesia - SQL Analysis
-- Analisis Produksi Elektronik H2 2024
-- ==============================================================================
-- File ini berisi 15 query analisis yang mendemonstrasikan berbagai fitur SQL:
-- SUM, COUNT, GROUP BY, ORDER BY, JOIN, CASE WHEN, Window Functions,
-- CTE, Subquery, HAVING, DATE functions, RANK, LAG, Moving Average, dll.
-- ==============================================================================


-- ============================================================
-- QUERY 1: Total Output Keseluruhan
-- Fitur: SUM(), COUNT()
-- ============================================================
SELECT
    COUNT(*) AS total_records,
    SUM(output_qty) AS total_output,
    SUM(target_qty) AS total_target,
    SUM(defect_qty) AS total_defect,
    ROUND(SUM(output_qty) * 100.0 / SUM(target_qty), 1) AS achievement_pct,
    ROUND(SUM(defect_qty) * 100.0 / SUM(output_qty), 2) AS defect_rate_pct,
    ROUND(AVG(downtime_minutes), 1) AS avg_downtime
FROM production_fact;


-- ============================================================
-- QUERY 2: Output per Line Produksi
-- Fitur: GROUP BY, ORDER BY, JOIN
-- ============================================================
SELECT
    l.line_name,
    l.supervisor,
    SUM(pf.output_qty) AS total_output,
    SUM(pf.target_qty) AS total_target,
    ROUND(SUM(pf.output_qty) * 100.0 / SUM(pf.target_qty), 1) AS achievement_pct,
    ROUND(SUM(pf.output_qty) * 100.0 / (SELECT SUM(output_qty) FROM production_fact), 1) AS output_share_pct
FROM production_fact pf
JOIN line_dim l ON pf.line_id = l.line_id
GROUP BY l.line_name, l.supervisor
ORDER BY total_output DESC;


-- ============================================================
-- QUERY 3: Defect Rate per Shift
-- Fitur: CASE WHEN, JOIN, Aggregate
-- ============================================================
SELECT
    s.shift_name,
    s.start_time,
    s.end_time,
    SUM(pf.output_qty) AS total_output,
    SUM(pf.defect_qty) AS total_defect,
    ROUND(SUM(pf.defect_qty) * 100.0 / SUM(pf.output_qty), 2) AS defect_rate_pct,
    CASE
        WHEN SUM(pf.defect_qty) * 100.0 / SUM(pf.output_qty) > 4 THEN 'HIGH'
        WHEN SUM(pf.defect_qty) * 100.0 / SUM(pf.output_qty) > 3 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS defect_category
FROM production_fact pf
JOIN shift_dim s ON pf.shift_id = s.shift_id
GROUP BY s.shift_name, s.start_time, s.end_time
ORDER BY defect_rate_pct DESC;


-- ============================================================
-- QUERY 4: Top 5 Mesin dengan Downtime Tertinggi
-- Fitur: JOIN, ORDER BY DESC, LIMIT
-- ============================================================
SELECT
    m.machine_name,
    m.machine_type,
    m.purchase_year,
    (2024 - m.purchase_year) AS machine_age,
    SUM(pf.downtime_minutes) AS total_downtime,
    ROUND(AVG(pf.downtime_minutes), 1) AS avg_downtime,
    COUNT(*) AS batch_count
FROM production_fact pf
JOIN machine_dim m ON pf.machine_id = m.machine_id
GROUP BY m.machine_name, m.machine_type, m.purchase_year
ORDER BY total_downtime DESC
LIMIT 5;


-- ============================================================
-- QUERY 5: Running Total Output Bulanan
-- Fitur: Window Function (SUM OVER)
-- ============================================================
SELECT
    month_num,
    monthly_output,
    SUM(monthly_output) OVER (ORDER BY month_num) AS running_total,
    ROUND(monthly_output * 100.0 / SUM(monthly_output) OVER (), 1) AS pct_of_total
FROM (
    SELECT
        EXTRACT(MONTH FROM production_date) AS month_num,
        SUM(output_qty) AS monthly_output
    FROM production_fact
    GROUP BY EXTRACT(MONTH FROM production_date)
) monthly_data
ORDER BY month_num;


-- ============================================================
-- QUERY 6: Ranking Line Berdasarkan Output per Bulan
-- Fitur: RANK(), DENSE_RANK(), Window Function
-- ============================================================
SELECT
    EXTRACT(MONTH FROM pf.production_date) AS month_num,
    l.line_name,
    SUM(pf.output_qty) AS monthly_output,
    RANK() OVER (
        PARTITION BY EXTRACT(MONTH FROM pf.production_date)
        ORDER BY SUM(pf.output_qty) DESC
    ) AS output_rank,
    DENSE_RANK() OVER (
        PARTITION BY EXTRACT(MONTH FROM pf.production_date)
        ORDER BY SUM(pf.output_qty) DESC
    ) AS dense_rank
FROM production_fact pf
JOIN line_dim l ON pf.line_id = l.line_id
GROUP BY EXTRACT(MONTH FROM pf.production_date), l.line_name
ORDER BY month_num, output_rank;


-- ============================================================
-- QUERY 7: Moving Average Output 7 Hari
-- Fitur: Window Function (AVG OVER ROWS)
-- ============================================================
SELECT
    production_date,
    daily_output,
    ROUND(AVG(daily_output) OVER (
        ORDER BY production_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 0) AS moving_avg_7d
FROM (
    SELECT
        production_date,
        SUM(output_qty) AS daily_output
    FROM production_fact
    GROUP BY production_date
) daily_data
ORDER BY production_date;


-- ============================================================
-- QUERY 8: Achievement Rate per Line per Bulan
-- Fitur: JOIN, GROUP BY, Calculated Fields
-- ============================================================
SELECT
    l.line_name,
    EXTRACT(MONTH FROM pf.production_date) AS month_num,
    SUM(pf.output_qty) AS total_output,
    SUM(pf.target_qty) AS total_target,
    ROUND(SUM(pf.output_qty) * 100.0 / SUM(pf.target_qty), 1) AS achievement_pct,
    CASE
        WHEN SUM(pf.output_qty) * 100.0 / SUM(pf.target_qty) >= 95 THEN 'ON TARGET'
        WHEN SUM(pf.output_qty) * 100.0 / SUM(pf.target_qty) >= 85 THEN 'BELOW TARGET'
        ELSE 'CRITICAL'
    END AS status
FROM production_fact pf
JOIN line_dim l ON pf.line_id = l.line_id
GROUP BY l.line_name, EXTRACT(MONTH FROM pf.production_date)
ORDER BY l.line_name, month_num;


-- ============================================================
-- QUERY 9: Mesin dengan Downtime di Atas Rata-rata
-- Fitur: Subquery
-- ============================================================
SELECT
    m.machine_name,
    m.machine_type,
    (2024 - m.purchase_year) AS machine_age,
    ROUND(AVG(pf.downtime_minutes), 1) AS avg_downtime
FROM production_fact pf
JOIN machine_dim m ON pf.machine_id = m.machine_id
GROUP BY m.machine_name, m.machine_type, m.purchase_year
HAVING AVG(pf.downtime_minutes) > (
    SELECT AVG(downtime_minutes) FROM production_fact
)
ORDER BY avg_downtime DESC;


-- ============================================================
-- QUERY 10: Perbandingan Output Bulan Ini vs Bulan Lalu
-- Fitur: LAG() Window Function
-- ============================================================
SELECT
    month_num,
    monthly_output,
    LAG(monthly_output) OVER (ORDER BY month_num) AS prev_month_output,
    monthly_output - LAG(monthly_output) OVER (ORDER BY month_num) AS mom_change,
    ROUND(
        (monthly_output - LAG(monthly_output) OVER (ORDER BY month_num)) * 100.0
        / LAG(monthly_output) OVER (ORDER BY month_num), 1
    ) AS mom_change_pct
FROM (
    SELECT
        EXTRACT(MONTH FROM production_date) AS month_num,
        SUM(output_qty) AS monthly_output
    FROM production_fact
    GROUP BY EXTRACT(MONTH FROM production_date)
) monthly_data
ORDER BY month_num;


-- ============================================================
-- QUERY 11: Defect Rate Trend Bulanan per Produk
-- Fitur: DATE function, JOIN, GROUP BY
-- ============================================================
SELECT
    EXTRACT(MONTH FROM pf.production_date) AS month_num,
    p.product_name,
    SUM(pf.output_qty) AS total_output,
    SUM(pf.defect_qty) AS total_defect,
    ROUND(SUM(pf.defect_qty) * 100.0 / SUM(pf.output_qty), 2) AS defect_rate_pct
FROM production_fact pf
JOIN product_dim p ON pf.product_id = p.product_id
GROUP BY EXTRACT(MONTH FROM pf.production_date), p.product_name
ORDER BY p.product_name, month_num;


-- ============================================================
-- QUERY 12: Top Performing Line-Shift Combination
-- Fitur: CTE (Common Table Expression), GROUP BY
-- ============================================================
WITH line_shift_perf AS (
    SELECT
        l.line_name,
        s.shift_name,
        SUM(pf.output_qty) AS total_output,
        ROUND(SUM(pf.defect_qty) * 100.0 / SUM(pf.output_qty), 2) AS defect_rate,
        ROUND(AVG(pf.downtime_minutes), 1) AS avg_downtime
    FROM production_fact pf
    JOIN line_dim l ON pf.line_id = l.line_id
    JOIN shift_dim s ON pf.shift_id = s.shift_id
    GROUP BY l.line_name, s.shift_name
)
SELECT
    line_name,
    shift_name,
    total_output,
    defect_rate,
    avg_downtime,
    RANK() OVER (ORDER BY total_output DESC) AS rank_by_output
FROM line_shift_perf
ORDER BY rank_by_output;


-- ============================================================
-- QUERY 13: Identifikasi Hari dengan Output Anomali (di bawah rata-rata)
-- Fitur: CTE, HAVING, AVG, Subquery
-- ============================================================
WITH daily_output AS (
    SELECT
        production_date,
        SUM(output_qty) AS total_daily_output
    FROM production_fact
    GROUP BY production_date
),
stats AS (
    SELECT
        AVG(total_daily_output) AS avg_daily,
        AVG(total_daily_output) - 1.5 * STDDEV(total_daily_output) AS lower_bound
    FROM daily_output
    -- Exclude weekends for baseline calculation
    WHERE EXTRACT(DOW FROM production_date) BETWEEN 1 AND 5
)
SELECT
    d.production_date,
    d.total_daily_output,
    ROUND(s.avg_daily, 0) AS avg_daily,
    ROUND(d.total_daily_output - s.avg_daily, 0) AS deviation
FROM daily_output d
CROSS JOIN stats s
WHERE d.total_daily_output < s.lower_bound
ORDER BY d.total_daily_output ASC
LIMIT 10;


-- ============================================================
-- QUERY 14: Ringkasan KPI per Bulan (Executive Dashboard)
-- Fitur: Multiple Aggregation, CASE WHEN
-- ============================================================
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
GROUP BY EXTRACT(MONTH FROM production_date)
ORDER BY month_num;


-- ============================================================
-- QUERY 15: Analisis Dampak Downtime terhadap Output per Line
-- Fitur: JOIN, Subquery, Calculated Fields, CTE
-- ============================================================
WITH machine_downtime AS (
    SELECT
        pf.line_id,
        l.line_name,
        m.machine_name,
        (2024 - m.purchase_year) AS machine_age,
        AVG(pf.downtime_minutes) AS avg_downtime,
        AVG(pf.output_qty) AS avg_output,
        COUNT(*) AS batch_count
    FROM production_fact pf
    JOIN line_dim l ON pf.line_id = l.line_id
    JOIN machine_dim m ON pf.machine_id = m.machine_id
    GROUP BY pf.line_id, l.line_name, m.machine_name, m.purchase_year
)
SELECT
    line_name,
    machine_name,
    machine_age,
    ROUND(avg_downtime, 1) AS avg_downtime_min,
    ROUND(avg_output, 0) AS avg_output_units,
    batch_count,
    CASE
        WHEN machine_age > 5 AND avg_downtime > 30 THEN 'PRIORITAS TINGGI - Perlu preventive maintenance segera'
        WHEN machine_age > 3 AND avg_downtime > 20 THEN 'PRIORITAS SEDANG - Jadwalkan maintenance rutin'
        ELSE 'NORMAL - Lanjutkan monitoring'
    END AS maintenance_recommendation
FROM machine_downtime
ORDER BY avg_downtime DESC;
