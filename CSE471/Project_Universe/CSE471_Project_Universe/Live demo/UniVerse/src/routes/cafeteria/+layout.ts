// src/routes/cafeteria/+layout.ts
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ parent }) => {
  const { user } = await parent();
  return { user };
};
