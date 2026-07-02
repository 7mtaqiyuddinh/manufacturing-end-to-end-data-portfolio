-- ==============================================================================
-- PT Voltec Indonesia - Load Data dari CSV
-- ==============================================================================
-- Catatan: Sesuaikan path file sesuai lokasi data Anda.
-- Untuk MySQL gunakan LOAD DATA INFILE, untuk PostgreSQL gunakan COPY.
-- Contoh di bawah menggunakan syntax MySQL.
-- ==============================================================================

-- Untuk MySQL:
-- LOAD DATA INFILE '/path/to/data/cleaned/line_dim_cleaned.csv'
-- INTO TABLE line_dim
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- Untuk PostgreSQL:
-- COPY line_dim FROM '/path/to/data/cleaned/line_dim_cleaned.csv' WITH CSV HEADER;

-- Untuk SQLite (via command line):
-- .mode csv
-- .import --skip 1 data/cleaned/line_dim_cleaned.csv line_dim
-- .import --skip 1 data/cleaned/machine_dim_cleaned.csv machine_dim
-- .import --skip 1 data/cleaned/shift_dim_cleaned.csv shift_dim
-- .import --skip 1 data/cleaned/product_dim_cleaned.csv product_dim
-- .import --skip 1 data/cleaned/production_fact_cleaned.csv production_fact

-- ==============================================================================
-- Alternatif: INSERT manual untuk dimension tables (data kecil)
-- ==============================================================================

-- Line Dimension
INSERT INTO line_dim (line_id, line_name, supervisor, capacity_per_shift) VALUES
(1, 'Line A', 'Budi Santoso', 520),
(2, 'Line B', 'Siti Rahayu', 480),
(3, 'Line C', 'Ahmad Wijaya', 500),
(4, 'Line D', 'Dewi Kusuma', 460),
(5, 'Line E', 'Rizky Pratama', 440);

-- Shift Dimension
INSERT INTO shift_dim (shift_id, shift_name, start_time, end_time) VALUES
(1, 'Shift Pagi', '06:00', '14:00'),
(2, 'Shift Siang', '14:00', '22:00'),
(3, 'Shift Malam', '22:00', '06:00');

-- Product Dimension
INSERT INTO product_dim (product_id, product_name, category, unit_cost) VALUES
(1, 'PCB Assembly', 'Assembly', 25000.00),
(2, 'Sensor Module', 'Component', 45000.00),
(3, 'Power Supply Unit', 'Power', 78000.00),
(4, 'LED Panel', 'Display', 35000.00),
(5, 'Control Board', 'Controller', 120000.00);

-- Machine Dimension
INSERT INTO machine_dim (machine_id, machine_name, machine_type, purchase_year, status) VALUES
(1,  'SMT-01',     'SMT Placement',  2018, 'Active'),
(2,  'SMT-02',     'SMT Placement',  2021, 'Active'),
(3,  'SMT-03',     'SMT Placement',  2023, 'Active'),
(4,  'WAVE-01',    'Wave Soldering', 2017, 'Active'),
(5,  'WAVE-02',    'Wave Soldering', 2020, 'Active'),
(6,  'WAVE-03',    'Wave Soldering', 2022, 'Active'),
(7,  'AOI-01',     'Inspection',     2019, 'Active'),
(8,  'AOI-02',     'Inspection',     2023, 'Active'),
(9,  'ICT-01',     'Testing',        2018, 'Active'),
(10, 'ICT-02',     'Testing',        2021, 'Active'),
(11, 'REFLOW-01',  'Reflow Oven',    2016, 'Active'),
(12, 'REFLOW-02',  'Reflow Oven',    2020, 'Active'),
(13, 'REFLOW-03',  'Reflow Oven',    2024, 'Active'),
(14, 'PRESS-01',   'Press',          2019, 'Active'),
(15, 'PACK-01',    'Packaging',      2022, 'Active');
