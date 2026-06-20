// src/routes/menu/+server.ts
import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import { handleSearch } from '$lib/controllers/menuController';

export const GET: RequestHandler = async ({ url, locals }) => {
  const q = url.searchParams.get('q') ?? undefined;
  const limit = Number(url.searchParams.get('limit') ?? '24');
  const offset = Number(url.searchParams.get('offset') ?? '0');

  const userId = locals?.user?.id ?? null;
  const data = await handleSearch(userId, q, limit, offset);
  return json(data);
};
