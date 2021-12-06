CREATE TABLE samples(
    qr_code_key TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    batch_id TEXT,
    protein_concentration TEXT,
    date_entered TEXT NOT NULL
);