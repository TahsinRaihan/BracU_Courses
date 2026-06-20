import * as menuController from '$lib/controllers/menuController';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ url, parent }) => {
    console.log('Menu page load function re-running due to URL change.'); // Added log
    const { session } = await parent();
    const userId = session?.user?.id ?? null;
    const searchQuery = url.searchParams.get('search') || '';
    
    const menuData = await menuController.loadMenuPage(userId, searchQuery);
    
    return {
        ...menuData,
        searchQuery
    };
};