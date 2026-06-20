// src/lib/server/supabaseClient.ts
// SERVER-ONLY Supabase client. Do NOT import this file from .svelte, +page.ts, or any browser code.
import { createClient } from '@supabase/supabase-js';

// Works with your existing Vite env keys
const url = process.env.VITE_SUPABASE_URL || import.meta.env.VITE_SUPABASE_URL;
const anon = process.env.VITE_SUPABASE_ANON_KEY || import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!url || !anon) {
  throw new Error('Missing VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY');
}

export const supabase = createClient(url as string, anon as string, {
  auth: {
    persistSession: false, // server does not persist
    autoRefreshToken: false
  }
});
