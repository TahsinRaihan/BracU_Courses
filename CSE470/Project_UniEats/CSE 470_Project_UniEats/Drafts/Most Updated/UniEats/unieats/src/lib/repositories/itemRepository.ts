
import { supabase } from '$lib/repositories/supabaseClient';

export async function getMenuItemById(id: string) {
  const { data: item, error: itemErr } = await supabase
    .from('menu_items')
    .select('*')
    .eq('id', id)
    .single();

  if (itemErr) {
    console.error('Error fetching menu item:', itemErr);
    return null;
  }
  return item;
}

export async function getReviewsByMenuItemId(menu_item_id: string) {
  const { data: reviews, error: revErr } = await supabase
    .from('reviews')
    .select('*')
    .eq('menu_item_id', menu_item_id)
    .order('created_at', { ascending: false });

  if (revErr) {
    console.error('Error loading reviews:', revErr);
    return [];
  }
  return reviews;
}
