
import * as cartRepository from '../repositories/cartRepository';
import * as orderRepository from '../repositories/orderRepository';
import { supabase } from '../repositories/supabaseClient';
import { notifications } from '$lib/stores/notifications';

export async function loadCartItems() {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return [];
  return cartRepository.getCartItemsByUserId(user.id);
}

export async function changeCartItemQuantity(cartId: string, diff: number) {
  const cartItems = await loadCartItems();
  const entry = cartItems.find(c => c.cartId === cartId);
  if (!entry) return;

  const newQty = entry.qty + diff;
  if (newQty < 1) {
    const error = await cartRepository.deleteCartItem(cartId);
    if (!error) notifications.notify('Order cancelled', 'warning');
  } else {
    const error = await cartRepository.updateCartItemQuantity(cartId, newQty);
    if (!error) notifications.notify('Cart updated', 'success');
  }
}

export async function cancelCartItem(cartId: string) {
  const error = await cartRepository.deleteCartItem(cartId);
  if (!error) notifications.notify('Order cancelled', 'warning');
}

export async function placeDirectOrders(cart: { cartId: string; qty: number; item: { id: string; name: string; price: number; }; }[], directPayment: string, directTxn: string) {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    notifications.notify('Log in first', 'error');
    return;
  }

  // 1. Insert into 'orders' table
  const orderPayload = {
    user_id: user.id,
    scheduled_at: new Date().toISOString(),
    status: directPayment === 'Online' ? 'paid' : 'pending',
    payment_method: directPayment,
    transaction_id: directPayment === 'Online' ? directTxn : null,
    menu_item_id: cart[0].item.id // Add menu_item_id from the first item in the cart
  };

  console.log('Order Payload:', orderPayload); // Added for debugging

  console.log('Order Payload:', orderPayload); // Added for debugging

  console.log('Order Payload:', orderPayload); // Added for debugging

  console.log('Order Payload:', orderPayload); // Added for debugging

  const { data: orderData, error: orderError } = await supabase
    .from('orders')
    .insert([orderPayload])
    .select();

  if (orderError) {
    notifications.notify(`Error creating order: ${orderError.message || 'Unknown error'}`, 'error');
    return;
  }

  const orderId = orderData[0].id;

  // 2. Insert into 'order_items' table
  const orderItemsPayload = cart.map(c => ({
    order_id: orderId,
    menu_item_id: c.item.id,
    quantity: c.qty,
    price_at_order: c.item.price
  }));

  const { error: orderItemsError } = await supabase
    .from('order_items')
    .insert(orderItemsPayload);

  if (orderItemsError) {
    notifications.notify(`Order created, but error adding items: ${orderItemsError.message || 'Unknown error'}`, 'error');
    // Optionally, you might want to delete the created order here if items fail to insert
    return;
  }

  // 3. Clear cart
  const deleteError = await cartRepository.deleteAllCartItemsByUserId(user.id);
  if (deleteError) {
    notifications.notify(`Order placed, but error clearing cart: ${deleteError.message || 'Unknown error'}. Please clear your cart manually.`, 'warning');
  }

  // 4. Success notification
  const totalAmount = cart.reduce((sum, c) => sum + c.qty * c.item.price, 0);
  const itemCount = cart.reduce((sum, c) => sum + c.qty, 0);
  notifications.notify(
    `✅ Direct order placed! Total: ৳${totalAmount.toFixed(2)} for ${itemCount} items.`,
    'success',
    { total: totalAmount, items: itemCount }
  );
}
