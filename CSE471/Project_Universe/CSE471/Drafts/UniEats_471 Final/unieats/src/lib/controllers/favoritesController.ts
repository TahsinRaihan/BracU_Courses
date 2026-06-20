
import * as service from '$lib/services/favoritesService';

export async function getFavorites(userId: string) {
  return service.getFavorites(userId);
}

export async function toggle(userId: string | null, menuItemId: number) {
  if (!userId) throw new Error('Not authenticated');
  return service.toggle(userId, menuItemId);
}