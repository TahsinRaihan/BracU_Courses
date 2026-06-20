// src/lib/services/orderService.ts
import type { SupabaseClient } from '@supabase/supabase-js';
import * as repository from '../repositories/orderRepository';
import { supabase } from '$lib/supabase';
import { cafeteria_notification } from '$lib/stores/cafeteria_nottification';
import { invalidate } from '$app/navigation'; // Import invalidate

interface OrderItem {
	quantity: number;
	price_at_order: number;
	menu_item: {
		id?: string; // Optional, as it's not always selected
		name: string; // Added name
		price?: number; // Optional, as it's not always selected
	}[]; // Changed to array
}

interface ScheduledOrder {
    orderId: string;
    at: string;
    qty: number;
    item: {
        id: string;
        name: string;
        price: number;
    };
    payment_method: string | null;
}

interface Order {
	id: string;
	created_at?: string; // Optional for scheduled orders
	scheduled_at: string;
	status: string;
	order_items: OrderItem[];
	payment_method?: string; // For scheduled orders
}



export async function loadScheduledOrders(userId: string) { // Added userId
	if (!userId) {
		cafeteria_notification.notify('User ID not found', 'error');
		return [];
	}
	const orders = await repository.getScheduledOrders(userId);

	if (!orders) {
		return [];
	}

	const menuItemIds = orders.map(order => order.menu_item_id);
	const { data: menuItemsData, error: menuItemsError } = await supabase
		.from('menu_items')
		.select('id, name, price')
		.in('id', menuItemIds);

	if (menuItemsError) {
		console.error('Error fetching menu items for scheduled orders:', menuItemsError);
		return [];
	}

	const menuItemsMap = new Map(menuItemsData.map(item => [item.id, item]));

	// Transform the data to match the ScheduledOrder interface expected by the frontend
	const mappedOrders = orders.map((order: any) => ({
		orderId: order.id,
		at: order.scheduled_at,
		qty: order.quantity || 0,
		item: menuItemsMap.get(order.menu_item_id) || { id: '', name: '', price: 0 },
		payment_method: null
	}));

	return mappedOrders;
}

export async function cancelOrder(orderId: string, isScheduled: boolean) {
    console.log('orderService.cancelOrder: orderId:', orderId); // Debugging log
	const { error } = await repository.cancelOrder(orderId, isScheduled);
	if (error) {
		cafeteria_notification.notify(`Error cancelling order: ${error.message || 'Unknown error'}`, 'error');
	} else {
		cafeteria_notification.notify('Order cancelled successfully!', 'success');
	}
	return { error };
}

export async function confirmScheduledOrders(
	scheduled: ScheduledOrder[], // Change parameter name from orderIds to scheduled
	paymentMethod: string,
	transactionId: string,
	userId: string // Add userId as a parameter
) {
    // No user authentication check here, rely on userId being passed

	const orderIdsToConfirm = scheduled.map((o) => o.orderId); // Rename the local variable
	const { error } = await repository.confirmScheduledOrders(orderIdsToConfirm, paymentMethod, transactionId, userId); // Uses passed userId
	console.log('Error from repository.confirmScheduledOrders:', error);

	if (error) {
        cafeteria_notification.notify(`Failed to confirm scheduled orders: ${error.message || 'Unknown error'}`, 'error'); // Added notification
		return { error };
	}

	const totalAmount = scheduled.reduce((sum, o) => sum + o.qty * o.item.price, 0);
	const itemCount = scheduled.reduce((sum, o) => sum + o.qty, 0);

		console.log('Scheduled orders confirmed successfully. Total:', totalAmount, 'Items:', itemCount); // Added success log
	return { error: null, totalAmount, itemCount };
}

// NEW: scheduleSingleOrder function
export async function scheduleSingleOrder(
    userId: string,
    menuItemId: string,
    quantity: number,
    scheduledAt: string
) {
    const { error } = await repository.createScheduledOrder({
        userId,
        menuItemId,
        quantity,
        scheduledAt
    });

    if (!error) {
        invalidate('/cafeteria/cart'); // Invalidate cart data
    }
    return { error };
}