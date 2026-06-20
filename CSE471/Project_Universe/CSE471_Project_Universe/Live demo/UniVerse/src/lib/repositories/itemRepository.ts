import { supabase } from '$lib/supabase';

export async function getMenuItemById(id: string) {
	console.log('Fetching menu item with ID:', id);
	const { data: item, error: itemErr } = await supabase
		.from('menu_items')
		.select('*')
		.eq('id', id)
		.single();

	if (itemErr) {
		console.error('Error fetching menu item:', itemErr);
		return null;
	}
	console.log('Fetched menu item:', item);
	return item;
}

export async function getReviewsByMenuItemId(menu_item_id: string) {
	console.log('Fetching reviews for menu item ID:', menu_item_id);
	const { data: reviews, error: revErr } = await supabase
		.from('reviews')
		.select('*')
		.eq('menu_item_id', menu_item_id)
		.order('created_at', { ascending: false });

	if (revErr) {
		console.error('Error loading reviews:', revErr);
		return [];
	}
	console.log('Fetched reviews:', reviews);
	return reviews;
}
