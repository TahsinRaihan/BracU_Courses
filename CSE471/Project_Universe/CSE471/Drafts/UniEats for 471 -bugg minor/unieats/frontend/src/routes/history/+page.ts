
import * as orderController from '$lib/controllers/orderController';

export async function load() {
  return orderController.loadHistoryPage();
}
