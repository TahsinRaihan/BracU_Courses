// src/lib/repositories/orderRepository.ts
import { supabase } from './supabaseClient';

export async function getOrderHistory(userId: string) {
  const { data, error } = await supabase
    .from('orders')
    .select(
      `
      id,
      created_at,
      scheduled_at,
      status,
      order_items (
        quantity,
        price_at_order,
        menu_item:menu_items (
          name
        )
      )
    `
    )
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching order history:', error);
    throw error; // Propagate the error
  }

  return data;
}

export async function insertOrder(order: any | any[]) { // eslint-disable-line @typescript-eslint/no-explicit-any
  const { error } = await supabase.from('orders').insert(order);
  return { error };
}

export async function getScheduledOrders(userId: string) {
  const { data, error } = await supabase
    .from('orders')
    .select(
      `
      id,
      scheduled_at,
      status,
      order_items (
        quantity,
        price_at_order,
        menu_item:menu_items (
          name,
          price
        )
      )
    `
    )
    .eq('user_id', userId)
    .in('status', ['pending'])
    .gt('scheduled_at', new Date().toISOString())
    .order('scheduled_at', { ascending: true });

  if (error) {
    console.error('Error fetching scheduled orders:', error);
    return [];
  }

  return data;
}

export async function cancelOrder(orderId: string) {
  const { error } = await supabase
    .from('orders')
    .update({ status: 'cancelled' })
    .eq('id', orderId);
  return { error };
}

export async function confirmScheduledOrders(orderIds: string[], paymentMethod: string, transactionId: string | null) {
  const { error } = await supabase
    .from('orders')
    .update({
      status: 'paid',
      payment_method: paymentMethod,
      transaction_id: transactionId,
    })
    .in('id', orderIds);
  return { error };
}