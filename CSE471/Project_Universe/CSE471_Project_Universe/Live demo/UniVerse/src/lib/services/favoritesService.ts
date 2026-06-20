// src/lib/services/favoritesService.ts
import * as repo from '$lib/repositories/favoritesRepository';
import { supabase } from '$lib/supabase';

export async function getFavorites(userId: string) {
	return repo.getFavoritesByUserId(supabase, userId);
}

export async function toggle(userId: string, menuItemId: string) {
	return repo.toggleFavorite(supabase, userId, menuItemId);
}