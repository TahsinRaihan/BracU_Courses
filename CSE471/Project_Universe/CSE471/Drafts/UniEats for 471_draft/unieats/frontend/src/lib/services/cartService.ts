
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
    if (!error) notifications.notify('Order cancelled', 'info');
  } else {
    const error = await cartRepository.updateCartItemQuantity(cartId, newQty);
    if (!error) notifications.notify('Cart updated', 'success');
  }
}

export async function cancelCartItem(cartId: string) {
  const error = await cartRepository.deleteCartItem(cartId);
  if (!error) notifications.notify('Order cancelled', 'info');
}

export async function placeDirectOrders(cart: { cartId: string; qty: number; item: { id: string; name: string; price: number; }; }[], directPayment: string, directTxn: string) {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return notifications.notify('Log in first', 'error');

  const payload = cart.map(c => ({
    user_id:          user.id,
    menu_item_id:     c.item.id,
    scheduled_at:     new Date().toISOString(),
    status:           directPayment === 'Online' ? 'paid' : 'pending',
    quantity:         c.qty,
    payment_method:   directPayment,
    transaction_id:   directPayment === 'Online' ? directTxn : null
  }));

  const { error: insertError } = await orderRepository.insertOrder(payload);
  if (insertError && insertError.message) {
    notifications.notify('Error placing direct orders', 'error');
    return;
  }

  const deleteError = await cartRepository.deleteAllCartItemsByUserId(user.id);
  if (!deleteError) {
    const totalAmount = cart.reduce((sum, c) => sum + c.qty * c.item.price, 0);
    const itemCount = cart.reduce((sum, c) => sum + c.qty, 0);
    notifications.notify(
      `✅ Direct order placed! Total: ৳${totalAmount.toFixed(2)} for ${itemCount} items.`, 
      'success',
      { total: totalAmount, items: itemCount }
    );
  }
}
