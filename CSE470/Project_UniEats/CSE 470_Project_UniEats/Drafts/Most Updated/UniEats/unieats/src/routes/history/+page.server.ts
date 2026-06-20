
import type { Actions, PageServerLoad } from './$types';
import { loadHistory } from '$lib/controllers/orderController';

export const load: PageServerLoad = async ({ locals }) => {
  const userId = locals?.user?.id ?? null;
  const orders = await loadHistory(userId);
  return { orders };
};

export const actions: Actions = {};
