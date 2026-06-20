
import * as orderService from '../services/orderService';

export async function loadHistoryPage() {
  const orders = await orderService.getOrdersForCurrentUser();
  return { orders };
}
