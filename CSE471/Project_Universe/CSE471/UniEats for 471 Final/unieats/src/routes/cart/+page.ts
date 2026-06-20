
import * as cartController from '$lib/controllers/cartController';

export async function load() {
  console.log('Cart page load function executed!');
  return cartController.loadCartPageData();
}
