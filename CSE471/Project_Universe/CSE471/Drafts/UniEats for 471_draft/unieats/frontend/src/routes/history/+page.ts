
import * as orderController from '$lib/controllers/orderController';

export async function load() {
  const data = await orderController.loadHistoryPage();
  console.log('Order History Load Data:', data);
  if (data.orders && data.orders.length > 0) {
    console.log('First Order Items:', data.orders[0].order_items);
  }
  return data;
}
