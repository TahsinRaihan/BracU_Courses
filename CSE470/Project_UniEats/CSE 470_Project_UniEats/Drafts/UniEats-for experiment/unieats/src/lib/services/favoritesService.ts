// src/lib/services/favoritesService.ts
import * as repo from '$lib/repositories/favoritesRepository';

export async function getFavorites(userId: string) {
  return repo.getFavoritesByUserId(userId);
}

export async function toggle(userId: string, menuItemId: number) {
    return repo.toggleFavorite(userId, menuItemId);
}