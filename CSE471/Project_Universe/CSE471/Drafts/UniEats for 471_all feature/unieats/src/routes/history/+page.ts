import * as orderController from '$lib/controllers/orderController';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ parent }) => {
  const { session } = await parent();
  const userId = session?.user?.id;

  if (!userId) {
    return { orders: [] };
  }

  const historyData = await orderController.loadHistory(userId);
  return historyData;
};