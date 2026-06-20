// src/routes/favorites/+server.ts
import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import { getFavorites, toggle } from '$lib/controllers/favoritesController';

export const GET: RequestHandler = async ({ locals }) => {
	const userId = locals?.user?.id ?? null;
	console.log('GET /favorites: userId', userId); // Added log
	if (!userId) {
		return new Response('Unauthorized', { status: 401 });
	}
	try {
		const favorites = await getFavorites(userId);
		console.log('GET /favorites: fetched favorites', favorites); // Added log
		return json(favorites);
	} catch (e: unknown) {
		console.error('GET /favorites: error fetching favorites', e); // Added log
		return new Response((e instanceof Error ? e.message : 'Failed to fetch favorites'), { status: 500 });
	}
};

export const POST: RequestHandler = async ({ request, locals }) => {
	const body = await request.json().catch(() => ({}));
	const menuItemId = body.menuItemId;
	if (!menuItemId) return new Response('menuItemId required', { status: 400 });

	const userId = locals?.user?.id ?? null;
	try {
		const result = await toggle(userId, menuItemId);
		return json(result);
	} catch (e: unknown) {
		return new Response((e instanceof Error ? e.message : 'Failed to toggle favorite'), { status: 401 });
	}
};
