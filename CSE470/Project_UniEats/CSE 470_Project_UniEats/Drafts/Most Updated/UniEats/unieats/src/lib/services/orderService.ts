// src/lib/services/orderService.ts
import * as repository from '$lib/repositories/orderRepository';
import { supabase } from '$lib/repositories/supabaseClient';
import { notifications } from '$lib/stores/notifications';

export async function getOrderHistoryWithTotals(userId: string) {
  try {
    const orders = await repository.getOrderHistory(userId);
    
    const withTotals = orders.map((o) => {
    let total = 0;
    o.order_items.forEach((item: any) => {
      const price = Number(item.price_at_order ?? 0);
      const qty = Number(item.quantity ?? 0);
      console.log(`Item: ${item.menu_item?.name}, Price: ${price}, Quantity: ${qty}, Subtotal: ${price * qty}`); // Added log
      total += price * qty;
    });
    console.log(`Order ID: ${o.id}, Calculated Total: ${total}`); // Added log

    return { ...o, total_amount: total };
  });

  return { orders: withTotals };
  } catch (error: any) {
    console.error('Error in getOrderHistoryWithTotals:', error);
    notifications.notify(`Failed to load order history: ${error.message || 'Unknown error'}`, 'error');
    return { orders: [] };
  }
}

export async function loadScheduledOrders() {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return [];
    const orders = await repository.getScheduledOrders(user.id);

    // Transform the data to match the ScheduledOrder interface expected by the frontend
    return orders.map(order => ({
        orderId: order.id,
        at: order.scheduled_at,
        qty: order.order_items[0]?.quantity || 0, // Assuming single item for now
        item: {
            id: order.order_items[0]?.menu_item?.id || '', // Assuming menu_item.id exists
            name: order.order_items[0]?.menu_item?.name || '',
            price: order.order_items[0]?.menu_item?.price || 0
        },
        payment_method: order.payment_method || null // Assuming payment_method might be on the order or null
    }));
}

export async function cancelOrder(orderId: string) {
    const { error } = await repository.cancelOrder(orderId);
    if (error) {
        notifications.notify(`Error cancelling order: ${error.message || 'Unknown error'}`, 'error');
    } else {
        notifications.notify('Order cancelled successfully!', 'success');
    }
    return { error };
}

export async function confirmScheduledOrders(scheduled: any[], paymentMethod: string, transactionId: string) {
    const orderIds = scheduled.map(o => o.orderId);
    const { error } = await repository.confirmScheduledOrders(orderIds, paymentMethod, transactionId);
    console.log('Error from repository.confirmScheduledOrders:', error); // Added log

    if (error) {
        return { error };
    }

    const totalAmount = scheduled.reduce((sum, o) => sum + o.qty * o.item.price, 0);
    const itemCount = scheduled.reduce((sum, o) => sum + o.qty, 0);

    return { error: null, totalAmount, itemCount };
}
