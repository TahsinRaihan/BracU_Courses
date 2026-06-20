
import { supabase } from './supabaseClient';

export async function getTodaySpecials() {
  const { data, error } = await supabase
    .from('specials') // Assuming a 'specials' table
    .select('id, name, description, price, image_url')
    .eq('is_active', true) // Assuming an 'is_active' flag
    .limit(3); // As per feature description, 2-3 special items

  if (error) {
    console.error('Error fetching today\'s specials:', error);
    return [];
  }
  return data;
}
