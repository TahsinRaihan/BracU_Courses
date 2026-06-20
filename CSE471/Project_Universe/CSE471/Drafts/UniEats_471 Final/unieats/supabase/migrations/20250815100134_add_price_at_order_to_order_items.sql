-- Add price_at_order column to order_items table
ALTER TABLE order_items
ADD COLUMN price_at_order NUMERIC(10, 2) NOT NULL DEFAULT 0.00;