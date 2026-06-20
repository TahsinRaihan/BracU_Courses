import * as cartRepository from '../repositories/cartRepository';
import { supabase } from '$lib/supabase';
import { cafeteria_notification } from '$lib/stores/cafeteria_nottification';
import { invalidate, goto } from '$app/navigation'; // Import invalidate and goto
// Removed: import { anonymousUser } from '$lib/stores/anonymousUser';

export async function getCartItems(userId: string) { // Renamed and added userId
    if (!userId) return [];
    return cartRepository.getCartItemsByUserId(userId);
}



export async function addToCart(userId: string, menuItemId: string, quantity: number) {
    console.log('cartService.addToCart: userId:', userId, 'menuItemId:', menuItemId, 'quantity:', quantity); // Added for debugging

    const existingCartItems = await cartRepository.getCartItemsByUserId(userId);
    const existingItem = existingCartItems.find(item => item.item.id === menuItemId);

    if (existingItem) {
        console.log('cartService.addToCart: Item exists, updating quantity.'); // Added for debugging
        const newQuantity = existingItem.qty + quantity;
        const error = await cartRepository.updateCartItemQuantity(userId, existingItem.cartId, newQuantity);
        if (!error) {
            cafeteria_notification.notify('Cart updated', 'success');
            invalidate('/cafeteria/cart'); // Invalidate cart data
        }
        return { success: !error };
    } else {
        console.log('cartService.addToCart: Item does not exist, adding new.'); // Added for debugging
        const error = await cartRepository.addToCart(userId, menuItemId, quantity);
        if (!error) {
            invalidate('/cafeteria/cart'); // Invalidate cart data
            goto('/cafeteria/cart'); // Redirect to cart page
        }
        return { success: !error };
    }
}

export async function updateCartItem(userId: string, cartId: string, quantity: number) { // Added userId
    const error = await cartRepository.updateCartItemQuantity(userId, cartId, quantity);
    if (!error) cafeteria_notification.notify('Cart updated', 'success');
    return { success: !error };
}

export async function removeCartItem(userId: string, cartId: string) { // Added userId
    console.log('cartService.removeCartItem: userId:', userId, 'cartId:', cartId); // Debugging log
    const error = await cartRepository.deleteCartItem(userId, cartId);
    if (!error) cafeteria_notification.notify('Item removed from cart', 'success');
    return { success: !error };
}

export async function changeCartItemQuantity(userId: string, cartId: string, diff: number) { // Added userId
    const cartItems = await getCartItems(userId); // Use new getCartItems
    const entry = cartItems.find(
        (c: { cartId: string; qty: number; item: any }) => c.cartId === cartId
    );
    if (!entry) return;

    const newQty = entry.qty + diff;
    if (newQty < 1) {
        const error = await cartRepository.deleteCartItem(userId, cartId); // Pass userId
        if (!error) cafeteria_notification.notify('Order cancelled', 'warning');
    } else {
        const error = await cartRepository.updateCartItemQuantity(userId, cartId, newQty); // Pass userId
        if (!error) cafeteria_notification.notify('Cart updated', 'success');
    }
}

export async function cancelCartItem(userId: string, cartId: string) { // Added userId
    const error = await cartRepository.deleteCartItem(userId, cartId); // Pass userId
    if (!error) cafeteria_notification.notify('Order cancelled', 'warning');
}

export async function placeDirectOrders(
    userId: string, // Added userId
    cart: { cartId: string; qty: number; item: { id: string; name: string; price: number } }[],
    directPayment: string,
    directTxn: string
) {
    if (!userId) {
        cafeteria_notification.notify('User ID not found', 'error');
        return { success: false, error: { message: 'User ID not found' } };
    }

    // 1. Insert into 'orders' table
    const totalAmount = cart.reduce((sum, c) => sum + c.qty * c.item.price, 0);

    const orderPayload = {
        user_id: userId,
        scheduled_at: null, // Direct orders are not scheduled
        status: directPayment === 'Online' ? 'completed' : 'pending',
        payment_method: directPayment,
        transaction_id: directPayment === 'Online' ? directTxn : null,
        total_amount: totalAmount,
    };

    console.log('Final Order Payload before insertion:', orderPayload); // Added for debugging

    const { data: orderData, error: orderError } = await supabase
        .from('orders')
        .insert([orderPayload])
        .select();

    if (orderError || !orderData || orderData.length === 0) { // Added !orderData || orderData.length === 0 check
        cafeteria_notification.notify(`Error creating order: ${orderError?.message || 'No order data returned'}`, 'error');
        console.error('Error creating order:', orderError || 'No order data returned');
        return { success: false, error: orderError || { message: 'No order data returned' } };
    }

    const orderId = orderData[0].id;

    // 2. Insert into 'order_items' table
    const orderItemsPayload = cart.map((c) => ({
        order_id: orderId,
        menu_item_id: c.item.id,
        item_name: c.item.name,
        quantity: c.qty,
        unit_price: c.item.price
    }));

    const { error: orderItemsError } = await supabase.from('order_items').insert(orderItemsPayload);

    if (orderItemsError || orderItemsPayload.length > 0 && !orderItemsPayload.every(item => item.order_id)) { // Added check for orderItems insertion
        cafeteria_notification.notify(
            `Order created, but error adding items: ${orderItemsError?.message || 'Order items not inserted correctly'}`,
            'error'
        );
        console.error('Error adding order items:', orderItemsError || 'Order items not inserted correctly');
        return { success: false, error: orderItemsError || { message: 'Order items not inserted correctly' } };
    }

    // 3. Clear cart
    const deleteError = await cartRepository.deleteAllCartItemsByUserId(userId); // Pass userId
    if (deleteError) {
        cafeteria_notification.notify(
            `Order placed, but error clearing cart: ${deleteError.message || 'Unknown error'}. Please clear your cart manually.`,
            'warning'
        );
        console.error('Error clearing cart after order:', deleteError); // Added error log
    }

    console.log('Direct order placed successfully. Total:', totalAmount, 'Items:', cart.length); // Added success log
    return { success: true, totalAmount, itemCount: cart.length };
}