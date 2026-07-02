-- ==============================================================================
-- PT Voltec Indonesia - Database Schema
-- Analisis Produksi Elektronik H2 2024
-- ==============================================================================
-- Database ini menggunakan star schema dengan 1 fact table dan 4 dimension tables.
-- Cocok untuk MySQL, PostgreSQL, atau SQLite.
-- ==============================================================================

-- Drop tables jika sudah ada (urutan: fact dulu, lalu dimension)
DROP TABLE IF EXISTS production_fact;
DROP TABLE IF EXISTS line_dim;
DROP TABLE IF EXISTS machine_dim;
DROP TABLE IF EXISTS shift_dim;
DROP TABLE IF EXISTS product_dim;

-- ==============================================================================
-- DIMENSION TABLES
-- ==============================================================================

-- Tabel dimensi line produksi
CREATE TABLE line_dim (
    line_id         INT PRIMARY KEY,
    line_name       VARCHAR(50) NOT NULL,       -- Nama line (Line A, B, C, D, E)
    supervisor      VARCHAR(100) NOT NULL,      -- Nama supervisor line
    capacity_per_shift INT NOT NULL             -- Kapasitas produksi per shift (unit)
);

-- Tabel dimensi mesin
CREATE TABLE machine_dim (
    machine_id      INT PRIMARY KEY,
    machine_name    VARCHAR(50) NOT NULL,       -- Kode mesin (SMT-01, WAVE-01, dll)
    machine_type    VARCHAR(50) NOT NULL,       -- Tipe mesin (SMT Placement, Wave Soldering, dll)
    purchase_year   INT NOT NULL,               -- Tahun pembelian mesin
    status          VARCHAR(20) NOT NULL        -- Status mesin (Active/Inactive)
);

-- Tabel dimensi shift
CREATE TABLE shift_dim (
    shift_id        INT PRIMARY KEY,
    shift_name      VARCHAR(50) NOT NULL,       -- Nama shift (Pagi, Siang, Malam)
    start_time      VARCHAR(10) NOT NULL,       -- Jam mulai shift
    end_time        VARCHAR(10) NOT NULL        -- Jam selesai shift
);

-- Tabel dimensi produk
CREATE TABLE product_dim (
    product_id      INT PRIMARY KEY,
    product_name    VARCHAR(100) NOT NULL,      -- Nama produk
    category        VARCHAR(50) NOT NULL,       -- Kategori produk
    unit_cost       DECIMAL(10,2) NOT NULL      -- Biaya per unit (Rupiah)
);

-- ==============================================================================
-- FACT TABLE
-- ==============================================================================

-- Tabel fakta produksi (1 record = 1 batch produksi per mesin per shift per hari)
CREATE TABLE production_fact (
    production_id       INT PRIMARY KEY,
    production_date     DATE NOT NULL,              -- Tanggal produksi
    line_id             INT NOT NULL,               -- FK ke line_dim
    machine_id          INT NOT NULL,               -- FK ke machine_dim
    shift_id            INT NOT NULL,               -- FK ke shift_dim
    product_id          INT NOT NULL,               -- FK ke product_dim
    target_qty          INT NOT NULL,               -- Target produksi (unit)
    output_qty          INT NOT NULL,               -- Output aktual (unit)
    defect_qty          INT NOT NULL,               -- Jumlah defect (unit)
    downtime_minutes    DECIMAL(6,1) NOT NULL,      -- Durasi downtime (menit)

    FOREIGN KEY (line_id) REFERENCES line_dim(line_id),
    FOREIGN KEY (machine_id) REFERENCES machine_dim(machine_id),
    FOREIGN KEY (shift_id) REFERENCES shift_dim(shift_id),
    FOREIGN KEY (product_id) REFERENCES product_dim(product_id)
);

-- ==============================================================================
-- INDEXES (untuk performa query)
-- ==============================================================================

CREATE INDEX idx_production_date ON production_fact(production_date);
CREATE INDEX idx_production_line ON production_fact(line_id);
CREATE INDEX idx_production_machine ON production_fact(machine_id);
CREATE INDEX idx_production_shift ON production_fact(shift_id);
CREATE INDEX idx_production_product ON production_fact(product_id);
