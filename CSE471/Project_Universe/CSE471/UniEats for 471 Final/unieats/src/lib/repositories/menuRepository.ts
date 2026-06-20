// src/lib/repositories/menuRepository.ts
import { supabase } from './supabaseClient';
import type { MenuItem } from '$lib/models';

export type SearchParams = {
  q?: string;
  limit?: number;
  offset?: number;
};

export async function searchMenu({ q, limit = 24, offset = 0 }: SearchParams) {
  let query = supabase
    .from('menu_items')
    .select('id, name, description, price, image_url, is_available, category_id', { count: 'exact' })
    .order('name', { ascending: true })
    .range(offset, offset + limit - 1);

  if (q && q.trim()) {
    const term = q.trim();
    query = query.or(`name.ilike.%${term}%,description.ilike.%${term}%`);
  }

  const { data, error, count } = await query;
  if (error) throw error;
  return { items: (data as MenuItem[]) ?? [], total: count ?? 0 };
}

export async function listFavoriteIdsByUser(userId: string): Promise<number[]> {
  const { data, error } = await supabase
    .from('favorites')
    .select('menu_item_id')
    .eq('user_id', userId);

  if (error) return [];
  return (data ?? []).map((r) => r.menu_item_id);
}

export async function listCategories() {
  const { data, error } = await supabase.from('categories').select('*');
  if (error) {
    console.error('Error listing categories:', error);
    return [];
  }
  return data;
}