// src/lib/controllers/menuController.ts
import * as service from '$lib/services/menuService';

export async function handleSearch(
  userId: string | null,
  q?: string,
  limit?: number,
  offset?: number
) {
  return service.searchMenuWithFavoriteMarking(userId, { q, limit, offset });
}

// Some of your pages call this name; keep it as an alias for compatibility
export const loadMenuPage = handleSearch;
