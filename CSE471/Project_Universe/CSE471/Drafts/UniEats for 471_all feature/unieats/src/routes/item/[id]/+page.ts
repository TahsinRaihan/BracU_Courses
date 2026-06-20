// src/routes/item/[id]/+page.js
import * as itemController from '$lib/controllers/itemController';

export async function load({ params }) {
  return itemController.loadItemPage(params.id);
}
