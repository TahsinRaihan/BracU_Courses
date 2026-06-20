
import * as itemRepository from '../repositories/itemRepository';

export async function getItemDetails(id: string) {
  const item = await itemRepository.getMenuItemById(id);
  if (!item) {
    return null;
  }
  const reviews = await itemRepository.getReviewsByMenuItemId(id);
  return { item, reviews };
}
