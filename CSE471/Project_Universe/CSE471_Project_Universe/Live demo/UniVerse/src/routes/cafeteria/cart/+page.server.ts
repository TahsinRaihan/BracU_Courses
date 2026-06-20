import { cartController } from '$lib/controllers/cartController';
import { error } from '@sveltejs/kit';
import * as orderService from '$lib/services/orderService';

export async function load({ locals }) {
    console.log('--- LOAD FUNCTION STARTED ---'); // New log for debugging
	console.log('Cart page load function re-executed!'); // Added for debugging
	const { user, session } = await locals.getSession();

	const user_id = user?.id;

	if (!user_id) {
		throw error(401, { message: 'Unauthorized' });
	}

	const cartItems = await cartController.getCartItems(user_id);
	const scheduledOrders = await orderService.loadScheduledOrders(user_id);

	return {
		cartItems,
		scheduledOrders,
		user: user // Pass the user object to the frontend
	};
}
