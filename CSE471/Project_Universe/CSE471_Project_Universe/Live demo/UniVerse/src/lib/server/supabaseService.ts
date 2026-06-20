import { createClient } from '@supabase/supabase-js'
import { env } from '$env/dynamic/private'
import { PUBLIC_SUPABASE_URL } from '$env/static/public'

// Server-only Supabase client with service role key to bypass RLS for backend jobs
const serviceRoleKey = env.SUPABASE_SERVICE_ROLE_KEY

if (!serviceRoleKey) {
  // In dev, surface a clear error instead of failing mysteriously downstream
  throw new Error('SUPABASE_SERVICE_ROLE_KEY is not set in server environment')
}

export const serviceSupabase = createClient(PUBLIC_SUPABASE_URL, serviceRoleKey, {
  auth: { persistSession: false }
})


