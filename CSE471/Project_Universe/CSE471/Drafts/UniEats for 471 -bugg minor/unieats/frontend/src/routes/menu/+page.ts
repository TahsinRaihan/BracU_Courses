
import * as menuController from '$lib/controllers/menuController';

export async function load({ url }) {
  const searchQuery = url.searchParams.get('search') || '';
  return menuController.loadMenuPage(searchQuery);
}
