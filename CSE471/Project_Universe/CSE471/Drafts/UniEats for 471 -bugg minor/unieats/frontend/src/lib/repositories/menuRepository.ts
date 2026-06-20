
import { supabase } from './supabaseClient';

export async function getCategories() {
  const { data: cats, error } = await supabase
    .from('categories')
    .select('*')
    .order('id');
  if (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
  return cats;
}

export async function getAllMenuItems() {
  const { data: all, error } = await supabase
    .from('menu_items')
    .select('*')
    .order('name');
  if (error) {
    console.error('Error fetching menu items:', error);
    return [];
  }
  return all;
}
