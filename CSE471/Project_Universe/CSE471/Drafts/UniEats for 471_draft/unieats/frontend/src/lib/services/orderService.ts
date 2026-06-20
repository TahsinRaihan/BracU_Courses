import * as orderRepository from '../repositories/orderRepository';
import { supabase } from '../repositories/supabaseClient'; // Assuming supabaseClient is needed for auth
import { notifications } from '$lib/stores/notifications';
import type { ScheduledOrder } from '../controllers/cartController';

export async function getOrdersForCurrentUser() {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    return [];
  }
  return orderRepository.getUserOrders(user.id);
}

export async function loadScheduledOrders() {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return [];

  const ords = await orderRepository.getPendingOrdersByUserId(user.id);

  const scheduled = await Promise.all(
    ords.map(async o => {
      const { data: mi, error: miErr } = await supabase
        .from('menu_items')
        .select('id,name,price')
        .eq('id', o.menu_item_id)
        .single();
      if (miErr) {
        console.error('Error loading menu item for order', o.id, miErr);
        return null;
      }
      // default qty to 1
      return { orderId: o.id, at: o.scheduled_at, qty: 1, item: mi };
    })
  ).then(arr => arr.filter(x => x));
  return scheduled;
}

export async function cancelOrder(orderId: string) {
  const error = await orderRepository.updateOrderStatus(orderId, 'cancelled');
  if (!error) notifications.notify('Order cancelled', 'info');
}

export async function confirmScheduledOrders(scheduledOrders: ScheduledOrder[], schedPayment: string, schedTxn: string) {
  for (const o of scheduledOrders) {
    const error = await orderRepository.updateOrderPaymentDetails(
      o.orderId,
      o.payment_method ?? schedPayment,
      schedPayment === 'Online' ? schedTxn : null
    );
    if (error && error.message) {
      notifications.notify('Error confirming scheduled order', 'error');
      return;
    }
    // Update status to 'paid' after successful payment details update
    const statusUpdateError = await orderRepository.updateOrderStatus(o.orderId, 'paid');
    if (statusUpdateError && statusUpdateError.message) {
      notifications.notify('Error updating order status to paid', 'error');
      return;
    }
  }
  const totalAmount = scheduledOrders.reduce((sum, o) => sum + o.qty * o.item.price, 0);
  const itemCount = scheduledOrders.reduce((sum, o) => sum + o.qty, 0);
  notifications.notify(
    `✅ Scheduled orders confirmed! Total: ৳${totalAmount.toFixed(2)} for ${itemCount} items.`, 
    'success',
    { total: totalAmount, items: itemCount }
  );
}