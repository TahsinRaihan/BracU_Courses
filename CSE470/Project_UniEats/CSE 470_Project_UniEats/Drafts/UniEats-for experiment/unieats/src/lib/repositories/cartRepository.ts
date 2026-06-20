
import { supabase } from './supabaseClient';

export async function getCartItemsByUserId(userId: string) {
  const { data, error } = await supabase
    .from('cart_items')
    .select('id, quantity, menu_items(id,name,price)', { head: false })
    .match({ user_id: userId });
  if (error) {
    console.error('Error fetching cart items:', error);
    return [];
  }
  return data.map(c => ({ cartId: c.id, qty: c.quantity, item: c.menu_items }));
}

export async function updateCartItemQuantity(cartId: string, newQuantity: number) {
  const { error } = await supabase.from('cart_items').update({ quantity: newQuantity }).match({ id: cartId });
  return error;
}

export async function deleteCartItem(cartId: string) {
  const { error } = await supabase.from('cart_items').delete().match({ id: cartId });
  console.log('deleteCartItem error:', error);
  return error;
}

export async function deleteAllCartItemsByUserId(userId: string) {
  const { error } = await supabase.from('cart_items').delete().match({ user_id: userId });
  return error;
}
