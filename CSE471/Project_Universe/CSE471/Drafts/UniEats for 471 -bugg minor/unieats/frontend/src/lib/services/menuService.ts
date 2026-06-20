
import * as menuRepository from '../repositories/menuRepository';
import type { MenuItem } from '$lib/models/MenuItem';

export async function getMenuData(searchQuery: string = '') {
  const categories = await menuRepository.getCategories();
  const allItems = await menuRepository.getAllMenuItems();

  const q = searchQuery.trim().toLowerCase();
  const filteredItems = allItems.filter(i => {
    const cat = categories.find(c => c.id === i.category_id)?.name.toLowerCase() || '';
    return i.name.toLowerCase().includes(q) || cat.includes(q);
  });

  const groupedItems: { [key: string]: MenuItem[] } = {};
  for (const c of categories) groupedItems[c.id] = [];
  for (const i of filteredItems) groupedItems[i.category_id]?.push(i);

  return { categories, items: allItems, grouped: groupedItems };
}
