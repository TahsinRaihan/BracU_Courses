import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { supabase } from '$lib/supabase';
import type { User } from '@supabase/supabase-js';
import { toasts } from './notifications'

// Auth state stores
export const user = writable<User | null>(null);
export const loading = writable(true);
export const isAuthenticated = writable(false);

// Only run in browser (client-side)
if (browser) {
  // Initialize auth state
  supabase.auth.getSession().then(({ data: { session } }) => {
    user.set(session?.user ?? null);
    loading.set(false);
  });

  // Listen for auth changes
  supabase.auth.onAuthStateChange((event, session) => {
    user.set(session?.user ?? null);
    loading.set(false);
    if (event === 'SIGNED_IN') {
      // Fire and forget: trigger overdue processing server-side
      fetch('/api/process-reminders', {
        method: 'POST',
        headers: { 'accept': 'application/json' },
      }).then(async (res) => {
        // Optional: show count processed
        try {
          const json = await res.json()
          if (json?.data?.processed > 0) {
            toasts.push({
              id: crypto.randomUUID(),
              title: 'Processed overdue reminders',
              message: `Delivered ${json.data.processed} pending reminder(s)`,
              type: 'general',
            })
          }
        } catch {}
      }).catch(() => {})
    }
  });
}

// Helper: automatically update isAuthenticated when user changes
user.subscribe(($user) => {
  isAuthenticated.set(!!$user);
});