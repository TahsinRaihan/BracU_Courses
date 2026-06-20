
import * as favoritesController from '$lib/controllers/favoritesController';

export async function load() {
  return favoritesController.loadFavorites();
}
