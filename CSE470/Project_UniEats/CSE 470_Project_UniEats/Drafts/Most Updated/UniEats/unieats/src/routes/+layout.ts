// src/routes/+layout.ts
import { browser } from '$app/environment';
import type { LayoutLoad } from './$types';
import { supabase as clientSupabase } from '$lib/supabase';

export const load: LayoutLoad = async ({ data, depends }) => {
  depends('supabase:auth');

  const { session } = data;

  if (browser) {
    const { data: { session: clientSession } } = await clientSupabase.auth.getSession();
    return { session: clientSession };
  }

  return { session };
};
