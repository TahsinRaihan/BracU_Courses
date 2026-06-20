
import * as cartController from '$lib/controllers/cartController';

export async function load() {
  return cartController.loadCartPageData();
}
