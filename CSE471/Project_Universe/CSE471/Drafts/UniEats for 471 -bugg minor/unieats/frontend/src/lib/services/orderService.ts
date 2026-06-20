import * as orderRepository from '../repositories/orderRepository';
import { supabase } from '../repositories/supabaseClient'; // Assuming supabaseClient is needed for auth
import { notifications } from '$lib/stores/notifications';

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

export async function confirmScheduledOrders(scheduledOrders: { orderId: string; payment_method: string; }[], schedPayment: string, schedTxn: string) {
  for (const o of scheduledOrders) {
    const error = await orderRepository.updateOrderPaymentDetails(
      o.orderId,
      o.payment_method ?? schedPayment,
      schedPayment === 'Online' ? schedTxn : null
    );
    if (error) {
      notifications.notify('Error confirming scheduled order', 'error');
      return;
    }
  }
  notifications.notify('Scheduled orders confirmed', 'success');
}