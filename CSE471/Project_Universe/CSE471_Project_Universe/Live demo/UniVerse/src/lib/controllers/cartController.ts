import * as cartService from '../services/cartService';
// Removed: import * as orderService from '../services/orderService';
// Removed: import { notifications } from '$lib/stores/notifications';

export const cartController = { // Export as a named object
    getCartItems: async (userId: string) => {
        return cartService.getCartItems(userId);
    },

    addToCart: async (userId: string, menuItemId: string, quantity: number) => {
        return cartService.addToCart(userId, menuItemId, quantity);
    },

    updateCartItem: async (userId: string, cartId: string, quantity: number) => {
        return cartService.updateCartItem(userId, cartId, quantity);
    },

    removeCartItem: async (userId: string, cartId: string) => {
        return cartService.removeCartItem(userId, cartId);
    }
};

// Removed other functions and interfaces
