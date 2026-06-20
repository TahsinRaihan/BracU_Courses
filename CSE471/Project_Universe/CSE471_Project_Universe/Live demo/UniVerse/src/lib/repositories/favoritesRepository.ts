import type { SupabaseClient } from '@supabase/supabase-js';
import type { MenuItem } from '$lib/models';

export async function isFavorite(supabase: SupabaseClient, userId: string, menuItemId: string): Promise<boolean> {
	const { data, error } = await supabase
		.from('favorites')
		.select('id')
		.eq('user_id', userId)
		.eq('menu_item_id', menuItemId)
		.maybeSingle();

	if (error) return false;
	return !!data;
}

export async function addFavorite(supabase: SupabaseClient, userId: string, menuItemId: string) {
	const { error } = await supabase
		.from('favorites')
		.insert({ user_id: userId, menu_item_id: menuItemId });
	if (error && error.code !== '23505') throw error; // ignore duplicates
}

export async function removeFavorite(supabase: SupabaseClient, userId: string, menuItemId: string) {
	const { error } = await supabase
		.from('favorites')
		.delete()
		.eq('user_id', userId)
		.eq('menu_item_id', menuItemId);
	if (error) throw error;
}

export async function toggleFavorite(supabase: SupabaseClient, userId: string, menuItemId: string): Promise<boolean> {
	const current = await isFavorite(supabase, userId, menuItemId);
	if (current) {
		await removeFavorite(supabase, userId, menuItemId);
		return false;
	}
	await addFavorite(supabase, userId, menuItemId);
	return true;
}

export async function getFavoritesByUserId(supabase: SupabaseClient, userId: string) {
	const { data, error } = await supabase
		.from('favorites')
		.select(
			`
      user_id,
      menu_item_id
    `
		);

	if (error) {
		console.error('Error fetching favorites:', error);
		return [];
	}

  console.log('Raw favorites data from Supabase:', data);

	return data.map((fav: { menu_item: MenuItem }) => fav.menu_item);
}