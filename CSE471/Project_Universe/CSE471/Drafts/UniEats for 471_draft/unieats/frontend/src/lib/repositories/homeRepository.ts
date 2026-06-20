
import { supabase } from './supabaseClient';

export async function getDailyMenuItems() {
  const { data, error } = await supabase.from('menu_items').select('id, name, price, image_url').ilike('tag', 'daily');
  if (error) {
    console.error('Error fetching daily menu items:', error);
    return [];
  }
  return data;
}

export async function getWeeklyMenuItems() {
  const { data, error } = await supabase.from('menu_items').select('id, name, price, image_url').ilike('tag', 'weekly');
  if (error) {
    console.error('Error fetching weekly menu items:', error);
    return [];
  }
  return data;
}

export async function getAllMenuItems() {
  const { data, error } = await supabase.from('menu_items').select('id, name, price, image_url');
  if (error) {
    console.error('Error fetching all menu items:', error);
    return [];
  }
  return data;
}
