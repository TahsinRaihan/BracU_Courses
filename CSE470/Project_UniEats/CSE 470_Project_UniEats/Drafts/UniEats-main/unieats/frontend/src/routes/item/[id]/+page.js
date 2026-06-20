// src/routes/item/[id]/+page.js
import { error } from '@sveltejs/kit';
import { supabase } from '$lib/supabase';

export async function load({ params }) {
  const id = params.id;

  // 1) Fetch the menu item
  const { data: item, error: itemErr } = await supabase
    .from('menu_items')
    .select('*')
    .eq('id', id)
    .single();

  if (itemErr || !item) {
    throw error(404, 'Dish not found');
  }

  // 2) Fetch its reviews
  const { data: reviews, error: revErr } = await supabase
    .from('reviews')
    .select('*')
    .eq('menu_item_id', id)
    .order('created_at', { ascending: false });

  if (revErr) {
    console.error('Error loading reviews:', revErr);
  }

  return { item, reviews: reviews || [] };
}
