import type { PageServerLoad } from './$types';
import { requireAdmin } from '$lib/server/auth';

export const load: PageServerLoad = async (event) => {
  const session = await requireAdmin(event);
  return {
    session,
    isAdmin: true
  };
};
