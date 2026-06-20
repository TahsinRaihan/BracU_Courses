<script lang="ts">
		import { derived } from 'svelte/store';
		import * as cartRepository from '$lib/repositories/cartRepository'; // Import cartRepository
	import * as cartController from '$lib/controllers/cartController';
	import * as orderService from '$lib/services/orderService'; // Import orderService
	import * as cartService from '$lib/services/cartService'; // Import cartService
	import { cafeteria_notification } from '$lib/stores/cafeteria_nottification';
	import { invalidate } from '$app/navigation';
	import SuccessModal from '$lib/components/SuccessModal.svelte';

	export let data;

	// Writable stores for cart and scheduled orders
	import { writable } from 'svelte/store';
	const localCart = writable(data?.cartItems || []);
	const localScheduled = writable(data?.scheduledOrders || []);

	// Payment state
	let directPayment = 'COD';
	let directTxn = '';
	let schedPayment = 'Online';
	let schedTxn = '';

	let loading = false; // New loading state variable
	let showSuccessModal = false;
	let successMessage = '';

	// Subtotals
	// Subtotals
	$: directSub = $localCart ? $localCart.reduce((sum, c) => sum + (c.qty * (c.item?.price ?? 0)), 0) : 0;
	$: schedSub = $localScheduled ? $localScheduled.reduce((sum, o) => sum + o.qty * o.item.price, 0) : 0;

	async function changeQty(cartId: string, diff: number) {
		const newData = await cartRepository.changeCartItemQuantity(cartId, diff);
		localCart.set(newData.cart);
	}

	async function cancelOrder(orderId: string, type: 'direct' | 'scheduled') {
		const userId = data.user?.id;
		console.log('userId from data.user?.id:', userId); // Debugging log
		if (!userId) {
			cafeteria_notification.notify('User ID is missing. Cannot cancel order.', 'error');
			return;
		}
		// Optimistic UI update
		if (type === 'direct') {
			$localCart = $localCart.filter((item) => item.cartId !== orderId);
			await cartRepository.deleteCartItem(userId, orderId); // Directly call cartRepository
		} else {
			$localScheduled = $localScheduled.filter((item) => item.orderId !== orderId);
			await orderService.cancelOrder(orderId, true); // Call orderService.cancelOrder for scheduled orders
		}

		// Invalidate to re-fetch and confirm state from backend
		invalidate('/cart');
	}

	// Update local stores when data changes (after invalidate)
	$: updateStores = (() => {
		if (data) {
			localCart.set(data.cartItems || []);
			localScheduled.set(data.scheduledOrders || []);
		}
	})();

	async function payDirect() {
		if (directPayment === 'Online' && (!directTxn || directTxn.length !== 8)) {
			cafeteria_notification.notify(
				'Please enter a valid 8-digit Transaction ID for Online payment.',
				'error'
			);
			return;
		}
		loading = true;
		try {
			const userId = data.user.id;
			const newData = await cartService.placeDirectOrders(userId, $localCart, directPayment, directTxn);
			if (newData.success) {
				successMessage = `Your direct order has been placed! Total: ৳${newData.totalAmount.toFixed(2)}.`;
				showSuccessModal = true;
				cafeteria_notification.notify(`✅ Direct order placed! Total: ৳${newData.totalAmount.toFixed(2)} for ${newData.itemCount} items.`, 'success');
				directTxn = '';
				directPayment = 'COD';
				localCart.set([]); // <-- Clear the cart immediately after order
				await invalidate('/cafeteria/cart');
			} else {
				cafeteria_notification.notify(`Error placing direct order: ${newData.error?.message || 'Unknown error'}`, 'error');
			}
		} finally {
			loading = false;
		}
	}

	async function payScheduled() {
		if (schedPayment === 'Online' && (!schedTxn || schedTxn.length !== 8)) {
			cafeteria_notification.notify(
				'Please enter a valid 8-digit Transaction ID for Online payment.',
				'error'
			);
			return;
		}
		loading = true;
		try {
			const newData = await orderService.confirmScheduledOrders(
				$localScheduled,
				schedPayment,
				schedTxn,
				data.user.id // Pass the user ID here
			);
			if (!newData.error) {
				successMessage = `Your scheduled orders have been confirmed! Total: ৳${newData.totalAmount.toFixed(2)}.`;
				showSuccessModal = true;
				cafeteria_notification.notify(`✅ Scheduled orders confirmed! Total: ৳${newData.totalAmount.toFixed(2)} for ${newData.itemCount} items.`, 'success');
				schedTxn = '';
				schedPayment = 'COD';
				await invalidate('/cafeteria/cart');
				localScheduled.set([]); // Explicitly clear the local store
			} else {
				cafeteria_notification.notify(`Error confirming scheduled orders: ${newData.error?.message || 'Unknown error'}`, 'error');
			}
		} finally {
			loading = false;
		}
	}

	
</script>

{#if data}
<div class="mx-auto max-w-3xl space-y-12 p-8">
	<h1 class="text-2xl font-semibold">Your Cart</h1>

	<!-- Scheduled Orders -->
	<section class="rounded bg-white p-6 shadow">
		<h2 class="mb-4 text-xl font-semibold">🕒 Scheduled Orders</h2>
		{#if $localScheduled.length}
			<table class="mb-4 w-full text-left">
				<thead>
					<tr><th>Item</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr>
				</thead>
				<tbody>
					{#each $localScheduled as o (o.orderId)}
						<tr class="border-b">
							<td class="py-2">{o.item.name}</td>
							<td class="py-2">৳{o.item.price}</td>
							<td class="flex items-center py-2">
								<!-- qty buttons disabled until DB column exists -->
								<span class="px-4">{o.qty}</span>
							</td>
							<td class="py-2">৳{(o.qty * o.item.price).toFixed(2)}</td>
							<td class="py-2">
								<button
									on:click={() => cancelOrder(o.orderId, 'scheduled')}
									class="rounded bg-red-600 px-3 py-1 text-white"
								>
									Cancel Order
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<div class="mb-4 text-right font-bold">Subtotal: ৳{schedSub.toFixed(2)}</div>
			<div class="space-y-4">
				<div class="font-semibold">Payment for Scheduled</div>
				<div class="flex items-center space-x-4">
					<label
						><input
							type="radio"
							bind:group={schedPayment}
							value="Online"
							class="mr-2"
						/>Online</label
					>
				</div>
				{#if schedPayment === 'Online'}
					<input
						type="text"
						bind:value={schedTxn}
						placeholder="Transaction ID"
						class="w-full rounded border p-2"
					/>
				{/if}
				<button
					on:click={payScheduled}
					class="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
					disabled={loading}
				>
					{#if loading}Processing...{:else}Pay Scheduled Orders{/if}
				</button>
			</div>
		{:else}
			<p class="text-gray-500">No scheduled orders.</p>
		{/if}
	</section>

	<!-- Direct Orders -->
	<section class="rounded bg-white p-6 shadow">
    <h2 class="mb-4 text-xl font-semibold">🛒 Direct Orders</h2>
    {#if $localCart.filter(c => !c.ordered).length}
        <table class="mb-4 w-full text-left">
            <thead>
                <tr><th>Item</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr>
            </thead>
            <tbody>
                {#each $localCart.filter(c => !c.ordered) as c (c.cartId)}
                    <tr class="border-b">
                        <td class="py-2">{c.item.name}</td>
                        <td class="py-2">৳{c.item.price}</td>
                        <td class="flex items-center py-2">
                            <button on:click={() => changeQty(c.cartId, -1)} class="px-2">➖</button>
                            <span class="px-2">{c.qty}</span>
                            <button on:click={() => changeQty(c.cartId, 1)} class="px-2">➕</button>
                        </td>
                        <td class="py-2">৳{(c.qty * c.item.price).toFixed(2)}</td>
                        <td class="py-2">
                            <button
                                on:click={() => cancelOrder(c.cartId, 'direct')}
                                class="rounded bg-red-600 px-3 py-1 text-white"
                            >
                                Cancel Order
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
        <div class="mb-4 text-right font-bold">Subtotal: ৳{directSub.toFixed(2)}</div>
        <div class="space-y-4">
				<div class="font-semibold">Payment for Direct</div>
				<div class="flex items-center space-x-4">
					<label
						><input type="radio" bind:group={directPayment} value="COD" class="mr-2" />COD</label
					>
					<label
						><input
							type="radio"
							bind:group={directPayment}
							value="Online"
							class="mr-2"
						/>Online</label
					>
				</div>
				{#if directPayment === 'Online'}
					<input
						type="text"
						bind:value={directTxn}
						placeholder="Transaction ID"
						class="w-full rounded border p-2"
					/>
				{/if}
				<button
					on:click={payDirect}
					class="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
					disabled={loading}
				>
					{#if loading}Processing...{:else}Pay Direct Orders{/if}
				</button>
			</div>
    {:else}
        <p class="text-gray-500">No direct orders.</p>
    {/if}
</section>
</div>

<SuccessModal
	show={showSuccessModal}
	title="Order Confirmed!"
	message={successMessage}
	onConfirm={() => {
		showSuccessModal = false;
	}}
/>
{/if}