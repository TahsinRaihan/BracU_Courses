
import * as menuService from '../services/menuService';

export async function loadMenuPage(searchQuery: string = '') {
  const { categories, items, grouped } = await menuService.getMenuData(searchQuery);
  return { categories, items, grouped };
}
