// src/routes/favorites/+server.ts
import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import { toggle } from '$lib/controllers/favoritesController';

export const POST: RequestHandler = async ({ request, locals }) => {
  const body = await request.json().catch(() => ({}));
  const menuItemId = Number(body.menuItemId);
  if (!menuItemId) return new Response('menuItemId required', { status: 400 });

  const userId = locals?.user?.id ?? null;
  try {
    const result = await toggle(userId, menuItemId);
    return json(result);
  } catch (e: any) {
    return new Response(e?.message ?? 'Failed to toggle favorite', { status: 401 });
  }
};
