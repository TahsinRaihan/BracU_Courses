
import * as cartService from '../services/cartService';
import * as orderService from '../services/orderService';

export async function loadCartPageData() {
  const cart = await cartService.loadCartItems();
  const scheduled = await orderService.loadScheduledOrders();
  console.log('loadCartPageData - Cart:', cart);
  console.log('loadCartPageData - Scheduled:', scheduled);
  return { cart, scheduled };
}

export async function changeCartItemQuantity(cartId: string, diff: number) {
  await cartService.changeCartItemQuantity(cartId, diff);
  return loadCartPageData(); // Reload data after action
}

export async function cancelOrder(orderId: string, type: 'direct' | 'scheduled') {
  if (type === 'direct') {
    await cartService.cancelCartItem(orderId);
  } else {
    await orderService.cancelOrder(orderId);
  }
  return loadCartPageData(); // Reload data after action
}

export interface CartItem { cartId: string; qty: number; item: { id: string; name: string; price: number; }; }
export interface ScheduledOrder { orderId: string; at: string; qty: number; item: { id: string; name: string; price: number; }; payment_method: string; }

export async function payDirectOrders(cart: CartItem[], directPayment: string, directTxn: string) {
  await cartService.placeDirectOrders(cart, directPayment, directTxn);
  return loadCartPageData(); // Reload data after action
}

export async function payScheduledOrders(scheduled: ScheduledOrder[], schedPayment: string, schedTxn: string) {
  await orderService.confirmScheduledOrders(scheduled, schedPayment, schedTxn);
  return loadCartPageData(); // Reload data after action
}
