
import * as favoritesService from '../services/favoritesService';

export async function loadFavorites() {
  const favorites = await favoritesService.getFavoritesForCurrentUser();
  return { favorites };
}
