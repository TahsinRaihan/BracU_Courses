
import { supabase } from './supabaseClient';

export async function getUserFavorites(userId: string) {
  const { data, error } = await supabase
    .from('favorites')
    .select('menu_items(id, name, description, price, image_url)')
    .eq('user_id', userId);

  if (error) {
    console.error('Error loading favorites:', error);
    return [];
  }
  return data.map(f => f.menu_items);
}
