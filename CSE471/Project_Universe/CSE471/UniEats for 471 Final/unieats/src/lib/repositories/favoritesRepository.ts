// src/lib/repositories/favoriteRepository.ts
import { supabase } from './supabaseClient';

export async function isFavorite(userId: string, menuItemId: number): Promise<boolean> {
  const { data, error } = await supabase
    .from('favorites')
    .select('id')
    .eq('user_id', userId)
    .eq('menu_item_id', menuItemId)
    .maybeSingle();

  if (error) return false;
  return !!data;
}

export async function addFavorite(userId: string, menuItemId: number) {
  const { error } = await supabase.from('favorites').insert({ user_id: userId, menu_item_id: menuItemId });
  if (error && error.code !== '23505') throw error; // ignore duplicates
}

export async function removeFavorite(userId: string, menuItemId: number) {
  const { error } = await supabase
    .from('favorites')
    .delete()
    .eq('user_id', userId)
    .eq('menu_item_id', menuItemId);
  if (error) throw error;
}

export async function toggleFavorite(userId: string, menuItemId: number): Promise<boolean> {
  const current = await isFavorite(userId, menuItemId);
  if (current) {
    await removeFavorite(userId, menuItemId);
    return false;
  }
  await addFavorite(userId, menuItemId);
  return true;
}

export async function getFavoritesByUserId(userId: string) {
  const { data, error } = await supabase
    .from('favorites')
    .select(
      `
      menu_item:menu_items (
        id,
        name,
        description,
        price,
        image_url,
        is_available,
        category_id
      )
    `
    )
    .eq('user_id', userId);

  if (error) {
    console.error('Error fetching favorites:', error);
    return [];
  }

  return data.map(fav => fav.menu_item);
}