
import * as service from '$lib/services/orderService';

export async function loadHistory(userId: string | null) {
  if (!userId) return { orders: [] };
  return service.getOrderHistoryWithTotals(userId);
}