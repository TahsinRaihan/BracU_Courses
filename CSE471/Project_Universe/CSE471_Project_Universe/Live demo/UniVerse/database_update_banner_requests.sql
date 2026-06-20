-- Update banner_requests table to add scheduling fields
-- Run this in your Supabase SQL Editor

-- Add new columns for scheduling
ALTER TABLE public.banner_requests 
ADD COLUMN IF NOT EXISTS schedule_type text DEFAULT 'immediate' CHECK (schedule_type = ANY (ARRAY['immediate'::text, 'scheduled'::text])),
ADD COLUMN IF NOT EXISTS scheduled_start_date timestamp with time zone,
ADD COLUMN IF NOT EXISTS duration_hours integer,
ADD COLUMN IF NOT EXISTS duration_minutes integer;

-- Update existing records to have the default schedule_type
UPDATE public.banner_requests 
SET schedule_type = 'immediate' 
WHERE schedule_type IS NULL;

-- Add comments for documentation
COMMENT ON COLUMN public.banner_requests.schedule_type IS 'Whether the banner starts immediately when approved or at a scheduled time';
COMMENT ON COLUMN public.banner_requests.scheduled_start_date IS 'The scheduled start date and time for the banner (only used when schedule_type is scheduled)';
COMMENT ON COLUMN public.banner_requests.duration_hours IS 'Duration in hours (alternative to duration_days for more precise timing)';
COMMENT ON COLUMN public.banner_requests.duration_minutes IS 'Duration in minutes (alternative to duration_days for more precise timing)';
