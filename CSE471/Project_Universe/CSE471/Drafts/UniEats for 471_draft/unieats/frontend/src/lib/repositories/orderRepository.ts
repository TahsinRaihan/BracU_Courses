import { supabase } from './supabaseClient';

export async function getUserOrders(userId: string) {
  const { data, error } = await supabase
    .from('orders')
    .select(`
        id,
        created_at,
        scheduled_at,
        status,
        order_items (
          quantity,
          menu_items ( name, price )
        )
      `)
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching user orders:', error);
    return [];
  }
  return data || [];
}

export async function insertOrder(payload: { user_id: string; menu_item_id: string; scheduled_at: string; status: string; quantity: number; payment_method: string; transaction_id: string | null; }[]) {
  const { data, error } = await supabase.from('orders').insert(payload);
  console.log('insertOrder error:', error);
  console.log('insertOrder data:', data);
  return { data, error };
}

export async function updateOrderStatus(orderId: string, status: string) {
  const { error } = await supabase.from('orders').update({ status }).eq('id', orderId);
  console.log('updateOrderStatus error:', error);
  return error;
}

export async function updateOrderPaymentDetails(orderId: string, paymentMethod: string, transactionId: string | null) {
  const { error } = await supabase
    .from('orders')
    .update({
      payment_method: paymentMethod,
      transaction_id: transactionId
    })
    .eq('id', orderId);
  console.log('updateOrderPaymentDetails error:', error);
  return error;
}

export async function getPendingOrdersByUserId(userId: string) {
  const { data, error } = await supabase
    .from('orders')
    .select('id, scheduled_at, menu_item_id', { head: false })
    .match({ user_id: userId, status: 'pending' })
    .order('scheduled_at', { ascending: true });
  if (error) {
    console.error('Error loading pending orders:', error);
    return [];
  }
  return data;
}