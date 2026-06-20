// src/lib/services/menuService.ts
import * as repo from '$lib/repositories/menuRepository';

export async function searchMenuWithFavoriteMarking(
  userId: string | null,
  params: repo.SearchParams
) {
  const { items, total } = await repo.searchMenu(params);
  const categories = await repo.listCategories();

  let favoriteIds: number[] = [];
  if (userId) {
    favoriteIds = await repo.listFavoriteIdsByUser(userId);
  }

  const marked = items.map((it) => ({ ...it, is_favorite: favoriteIds.includes(it.id) }));

  const grouped = marked.reduce((acc, item) => {
    const catId = item.category_id;
    if (!acc[catId]) {
      acc[catId] = [];
    }
    acc[catId].push(item);
    return acc;
  }, {} as { [key: number]: typeof marked });

  return { items: marked, total, categories, grouped };
}