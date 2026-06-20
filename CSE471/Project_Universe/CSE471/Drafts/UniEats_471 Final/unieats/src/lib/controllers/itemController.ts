
import * as itemService from '../services/itemService';
import { error } from '@sveltejs/kit';

export async function loadItemPage(id: string) {
  const itemDetails = await itemService.getItemDetails(id);

  if (!itemDetails || !itemDetails.item) {
    throw error(404, 'Dish not found');
  }

  return { item: itemDetails.item, reviews: itemDetails.reviews || [] };
}
