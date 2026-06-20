import { createClient } from '@supabase/supabase-js';
import { VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY } from '$env/static/private';
import type { Handle } from '@sveltejs/kit';

if (!VITE_SUPABASE_URL || !VITE_SUPABASE_ANON_KEY) {
  throw new Error('Missing VITE_SUPABASE_URL or VITE_SUPABASE_ANON_KEY in $env/static/private. Ensure they are set in your .env file and exposed correctly.');
}

export const handle: Handle = async ({ event, resolve }) => {
  event.locals.supabase = createClient(VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY, {
    auth: {
      persistSession: false,
      autoRefreshToken: false,
      detectSessionInUrl: false,
      storage: {
        getItem: (key) => event.cookies.get(key),
        setItem: (key, value) => event.cookies.set(key, value, { path: '/' }),
        removeItem: (key) => event.cookies.delete(key, { path: '/' }),
      },
    },
  });

  const {
    data: { session },
  } = await event.locals.supabase.auth.getSession();

  event.locals.user = session?.user || null;

  return resolve(event);
};