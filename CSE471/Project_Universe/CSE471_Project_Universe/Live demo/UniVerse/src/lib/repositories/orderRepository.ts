// src/lib/repositories/orderRepository.ts
import type { SupabaseClient } from '@supabase/supabase-js';
import { supabase } from '$lib/supabase';



export async function insertOrder(order: any | any[]) {
	// eslint-disable-line @typescript-eslint/no-explicit-any
	const { error } = await supabase.from('orders').insert(order);
	return { error };
}

export async function getScheduledOrders(userId: string) {
	const { data, error: queryError } = await supabase
		.from('cart_items')
		.select(
			`
      id,
      scheduled_at,
      quantity,
      menu_item_id
    `
		)
		.eq('user_id', userId)
		.not('scheduled_at', 'is', null); // <--- ADD THIS LINE

	if (queryError) {
		console.error('Error fetching scheduled orders:', queryError);
		return [];
	}

	console.log('Raw scheduled orders from DB (simplified query):', data);
	console.log('Error object from simplified query:', queryError);

	return data || [];
}

export async function cancelOrder(orderId: string, isScheduled: boolean) {
    console.log('cancelOrder (repository): orderId:', orderId); // Debugging log
	if (isScheduled) {
		const { error } = await supabase.from('cart_items').delete().eq('id', orderId);
		console.log('orderRepository.cancelOrder result error (scheduled):', error); // Debugging log
		return { error };
	} else {
		const { error } = await supabase.from('orders').update({ status: 'cancelled' }).eq('id', orderId);
		console.log('orderRepository.cancelOrder result error (direct):', error); // Debugging log
		return { error };
	}
}

export async function confirmScheduledOrders(
	orderIds: string[],
	paymentMethod: string,
	transactionId: string | null,
	userId: string
) {
    // 1. Fetch cart items (scheduled orders)
    const { data: rawCartItems, error: cartError } = await supabase
        .from('cart_items')
        .select(`id, quantity, menu_item_id`) // Select only necessary fields from cart_items
        .in('id', orderIds);

    if (cartError) {
        console.error('Supabase error fetching raw cart items for confirmation:', cartError);
        return { error: cartError };
    }
    if (!rawCartItems || rawCartItems.length === 0) {
        console.error('No raw cart items found for confirmation.');
        return { error: { message: 'No raw cart items found' } };
    }
    console.log('Fetched raw cart items:', rawCartItems);

    // 2. Extract unique menu_item_ids
    const menuItemIds = rawCartItems.map(item => item.menu_item_id);

    // 3. Fetch menu item details separately
    const { data: menuItemsData, error: menuItemsError } = await supabase
        .from('menu_items')
        .select(`id, name, price`) // Select necessary fields from menu_items
        .in('id', menuItemIds);

    if (menuItemsError) {
        console.error('Supabase error fetching menu items for confirmation:', menuItemsError);
        return { error: menuItemsError };
    }
    if (!menuItemsData || menuItemsData.length === 0) {
        console.error('No menu items found for confirmation.');
        return { error: { message: 'No menu items found' } };
    }
    console.log('Fetched menu items:', menuItemsData);

    // Create a map for easy lookup of menu item prices
    const menuItemsMap = new Map(menuItemsData.map(item => [item.id, item]));

    // 4. Calculate totalAmount and prepare orderItems
    let totalAmount = 0;
    const orderItems = rawCartItems.map((cartItem) => {
        const menuItem = menuItemsMap.get(cartItem.menu_item_id);
        if (!menuItem) {
            console.warn(`Menu item ${cartItem.menu_item_id} not found for cart item ${cartItem.id}`);
            return null; // Or handle this error appropriately
        }
        const unitPrice = menuItem.price;
        totalAmount += cartItem.quantity * unitPrice;
        return {
            order_id: '', // Will be filled after order creation
            menu_item_id: cartItem.menu_item_id,
            item_name: menuItem.name, // Assuming name is needed for order_items
            quantity: cartItem.quantity,
            unit_price: unitPrice
        };
    }).filter(item => item !== null); // Filter out any nulls if menu items weren't found

    if (orderItems.length === 0) {
        console.error('No valid order items to confirm after mapping and filtering.');
        return { error: { message: 'No valid order items to confirm.' } };
    }
    console.log('Prepared order items:', orderItems);

    const { data: orderData, error: orderError } = await supabase
        .from('orders')
        .insert({
            user_id: userId,
            total_amount: totalAmount, // Use the calculated totalAmount
            status: paymentMethod === 'Online' ? 'completed' : 'Pending',
            payment_method: paymentMethod,
            transaction_id: transactionId,
            scheduled_at: new Date().toISOString()
        })
        .select('id')
        .single();

    if (orderError) {
        console.error('Supabase error creating order from scheduled items:', orderError);
        return { error: orderError };
    }
    if (!orderData) {
        console.error('No order data returned after creating order.');
        return { error: { message: 'No order data returned' } };
    }
    console.log('Created order data:', orderData);

	const orderId = orderData.id;

	const finalOrderItems = orderItems.map(item => ({ ...item, order_id: orderId }));

	const { error: orderItemsError } = await supabase.from('order_items').insert(finalOrderItems); // Use finalOrderItems

    if (orderItemsError) {
        console.error('Supabase error inserting order items from scheduled items:', orderItemsError);
        return { error: orderItemsError };
    }
    if (finalOrderItems.length > 0 && !finalOrderItems.every(item => item.order_id)) {
        console.error('Order items not inserted correctly (missing order_id).');
        return { error: { message: 'Order items not inserted correctly' } };
    }
    console.log('Inserted order items:', finalOrderItems);

	const { error: deleteCartItemsError } = await supabase.from('cart_items').delete().in('id', orderIds);

	if (deleteCartItemsError) {
		console.error('Error deleting cart items after confirmation:', deleteCartItemsError);
		// This is not ideal, as the order is already created.
		// You might want to log this for manual cleanup.
	}

    console.log('Scheduled order confirmation process completed successfully in repository.'); // ADD THIS LINE
	return { error: null };
}

// NEW: createScheduledOrder function
export async function createScheduledOrder({
    userId,
    menuItemId,
    quantity,
    scheduledAt
}: {
    userId: string;
    menuItemId: string;
    quantity: number;
    scheduledAt: string;
}) {
    const { data, error } = await supabase
        .from('cart_items')
        .insert([{ user_id: userId, menu_item_id: menuItemId, quantity: quantity, scheduled_at: scheduledAt }]);
    
    if (error) {
        console.error('Error creating scheduled order:', error);
        return { error: error };
    }

    return { error: null };
}