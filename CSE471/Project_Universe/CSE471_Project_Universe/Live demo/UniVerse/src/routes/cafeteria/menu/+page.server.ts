import type { PageServerLoad } from './$types';
import * as menuController from '$lib/controllers/menuController';

export const load: PageServerLoad = async ({ url, locals: { supabase, user } }) => {
    const searchQuery = url.searchParams.get('search') || '';
    const userId = user?.id ?? null; // Get userId from locals

    const menuData = await menuController.loadMenuPage(supabase, userId, searchQuery);

    return {
        ...menuData,
        searchQuery
    };
};