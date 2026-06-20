import { getFavorites } from '$lib/controllers/favoritesController';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ parent }) => {
  const { session } = await parent();
  const userId = session?.user?.id;

  if (!userId) {
    return { favorites: [] };
  }

  return { favorites: await getFavorites(userId) };
};