import type { SupabaseClient } from '@supabase/supabase-js';
import { supabase } from '$lib/supabase';

interface CartItemData {
	id: string;
	quantity: number;
	menu_items: {
		id: string;
		name: string;
		price: number;
	}[]; // Changed to array
}

export async function getCartItemsByUserId(userId: string) {
    const { data: cartData, error: cartError } = await supabase
        .from('cart_items')
        .select('id, quantity, menu_item_id') // Select menu_item_id instead of joining
        .eq('user_id', userId)
		.is('scheduled_at', null);

    console.log('cartData from Supabase:', cartData); // Debugging log

    if (cartError) {
        console.error('Error fetching cart items:', cartError);
        return [];
    }

    // Fetch menu item details separately
    const menuItemIds = cartData.map(item => item.menu_item_id);
    const { data: menuItemsData, error: menuItemsError } = await supabase
        .from('menu_items')
        .select('id, name, price')
        .in('id', menuItemIds);

    console.log('menuItemsData from Supabase:', menuItemsData); // Debugging log

    if (menuItemsError) {
        console.error('Error fetching menu items:', menuItemsError);
        return [];
    }

    // Map cart items with their corresponding menu item details
    return cartData.map(cartItem => {
        const menuItem = menuItemsData.find(menu => menu.id === cartItem.menu_item_id);
        return {
            cartId: cartItem.id,
            qty: cartItem.quantity,
            item: menuItem || null // Assign the found menu item, or null if not found
        };
    });
}

// NEW: Add to cart
export async function addToCart(userId: string, menuItemId: string, quantity: number) {
    const { data, error } = await supabase
        .from('cart_items')
        .insert([{ user_id: userId, menu_item_id: menuItemId, quantity: quantity }]);
    return error;
}

// MODIFIED: updateCartItemQuantity to include userId
export async function updateCartItemQuantity(userId: string, cartId: string, newQuantity: number) {
	const { error } = await supabase
		.from('cart_items')
		.update({ quantity: newQuantity })
		.match({ id: cartId, user_id: userId }); // Added user_id to match
	return error;
}

// MODIFIED: deleteCartItem to include userId
export async function deleteCartItem(userId: string, cartId: string) {
    console.log('deleteCartItem: userId:', userId, 'cartId:', cartId); // Debugging log
	const { error } = await supabase
		.from('cart_items')
		.delete()
		.match({ id: cartId, user_id: userId }); // Added user_id to match
    if (error) {
        console.error('cartRepository.deleteCartItem error:', error); // Added for debugging
    }
    console.log('cartRepository.deleteCartItem result error:', error); // Debugging log
	return error;
}

export async function deleteAllCartItemsByUserId(userId: string) {
	const { error } = await supabase.from('cart_items').delete().match({ user_id: userId });
	return error;
}