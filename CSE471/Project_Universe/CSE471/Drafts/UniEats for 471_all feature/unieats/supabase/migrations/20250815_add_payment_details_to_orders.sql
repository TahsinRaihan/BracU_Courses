-- Add payment_method and transaction_id to orders table
ALTER TABLE orders
ADD COLUMN payment_method TEXT,
ADD COLUMN transaction_id TEXT;