
import * as service from '$lib/services/menuService';

export async function handleSearch(
  userId: string | null,
  q?: string,
  limit?: number,
  offset?: number
) {
  return service.searchMenuWithFavoriteMarking(userId, { q, limit, offset });
}


export const loadMenuPage = handleSearch;
