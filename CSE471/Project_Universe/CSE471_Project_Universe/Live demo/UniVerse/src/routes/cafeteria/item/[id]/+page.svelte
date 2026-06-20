<script lang="ts">
	import { onMount } from 'svelte';
	import { supabase } from '$lib/supabase';
	import { cafeteria_notification } from '$lib/stores/cafeteria_nottification';
	import { get } from 'svelte/store';
	import { favorites } from '$lib/stores/favorites';
	// import { user } from '$lib/stores/auth'; // Import the user store - not directly used here
	// import { anonymousUser } from '$lib/stores/anonymousUser'; // No longer needed for cart/order
	// Define the Review type locally
	type Review = {
		id: number;
		user_id: number;
		menu_item_id: number;
		rating: number;
		comment: string;
		created_at: string;
	};
	import { cartController } from '$lib/controllers/cartController'; // Directly import the named export
	import * as orderService from '$lib/services/orderService'; // Import orderService
	import { invalidate } from '$app/navigation'; // Import invalidate

	export let data;
	let { item, reviews: initialReviews } = data;

	let orderTime = '';
	let reviews: Review[] = initialReviews;
	let rating = 5;
	let comment = '';

	// Reactive isFav derived from the store
	$: isFav = $favorites.has(item.id);

	onMount(async () => {
		// if ($anonymousUser) { // Use the anonymous user store
		// 	favorites.fetchFavorites($anonymousUser);
		// }
		// Fetch favorites using the actual user ID from data.user.id
		if (data.user) {
			favorites.fetchFavorites(data.user.id);
		}
	});

	function imgFor(it: any) {
		if (it.image_url) return it.image_url;
		return `/images/${it.name
			.toLowerCase()
			.replace(/[^a-z0-9]+/g, '-')
			.replace(/(^-|-$)/g, '')}.jpg`;
	}

	async function toggleFav() {
		// Use data.user.id for favorites
		if (!data.user) return cafeteria_notification.notify('User not logged in', 'error');

		if (isFav) {
			await favorites.removeFavorite(data.user.id, item.id);
		} else {
			await favorites.addFavorite(data.user.id, item.id);
		}
	}

	async function addToCart() {
		if (!data.user)
			return cafeteria_notification.notify('User not logged in', 'error');
		if (item.is_available === false)
			return cafeteria_notification.notify('This item is unavailable', 'error');

		const userId = data.user.id;

		// Check if a notification for this item already exists
		const existingNotifications = get(cafeteria_notification);
		const notificationExists = existingNotifications.some(
			(n) => n.meta?.itemId === item.id && n.type === 'success'
		);

		if (notificationExists) {
			cafeteria_notification.notify('Item is already in the cart', 'info');
			return;
		}

		const { success } = await cartController.addToCart(userId, item.id, 1);
		if (success) {
			cafeteria_notification.notify(`✅ Added ${item.name} to cart`, 'success', { itemId: item.id });
			invalidate('/cafeteria/cart');
		} else {
			cafeteria_notification.notify(`Failed to add ${item.name} to cart`, 'error');
		}
	}

	import * as cartService from '$lib/services/cartService'; // Import cartService

// ... (rest of the script)

	async function placeOrder() {
		if (!data.user) return cafeteria_notification.notify('User not logged in', 'error');
		if (item.is_available === false) {
			return cafeteria_notification.notify('This item is unavailable', 'error');
		}

		if (!orderTime) {
			return cafeteria_notification.notify('Select date & time', 'error');
		}
		const dt = new Date(orderTime);
		if (dt <= new Date()) {
			return cafeteria_notification.notify('Pick a future time', 'error');
		}

		// Validate working hours (8 AM to 5 PM)
		const hour = dt.getHours();
		if (hour < 8 || hour >= 17) { // 17 is 5 PM
			return cafeteria_notification.notify('Orders can only be scheduled between 8 AM and 5 PM', 'error');
		}

		const userId = data.user.id; // Get user ID from data prop

		// Use orderService.scheduleSingleOrder
		const { error: orderError } = await orderService.scheduleSingleOrder(
			userId,
			item.id,
			1, // Quantity
			orderTime // Scheduled time
		);

		if (orderError) {
			console.error('Schedule insert error', orderError);
			return cafeteria_notification.notify(`Failed to schedule: ${orderError.message || 'Unknown error'}`, 'error');
		}

		
		const pickupCounter = Math.floor(Math.random() * 3) + 1; // Generates 1, 2, or 3
		cafeteria_notification.notify(`Order is Scheduled. Pickup from counter ${pickupCounter}`, 'success');
		invalidate('/cafeteria/cart'); // Invalidate cart data to refresh the cart page
	}

// ... (rest of the script and HTML)

	async function submitReview() {
		if (!data.user) return cafeteria_notification.notify('User not logged in', 'error');
		if (!comment) return cafeteria_notification.notify('Write a comment', 'error');

		const userId = data.user.id; // Get user ID from data prop

		await supabase.from('reviews').insert({
			user_id: userId, // Use actual user ID
			menu_item_id: item.id,
			rating,
			comment
		});
		const { data: revs = [] } = await supabase
			.from('reviews')
			.select('*')
			.eq('menu_item_id', item.id)
			.order('created_at', { ascending: false });
		reviews = revs || [];
		rating = 5;
		comment = '';
		cafeteria_notification.notify('⭐ Review submitted', 'success');
	}
</script>

{#if !item}
	<div class="p-8 text-center">Loading…</div>
{:else}
	<div class="mx-auto max-w-3xl space-y-6 p-8">
		<div class="relative h-64 w-full overflow-hidden rounded shadow-lg">
			<img src={imgFor(item)} alt={item.name} class="h-full w-full object-cover" />
			<button
				class="absolute top-4 right-4 text-3xl"
				on:click={toggleFav}
				aria-label="Toggle favorite"
			>
				{isFav ? '❤️' : '🤍'}
			</button>
			{#if item.is_available === false}
				<div
					class="bg-opacity-75 absolute inset-0 flex items-center justify-center bg-white text-xl font-bold"
				>
					Out of Stock
				</div>
			{/if}
		</div>

		<h1 class="text-3xl font-bold">{item.name}</h1>
		<p class="text-gray-700">{item.description}</p>
		<p class="text-xl font-semibold">৳{item.price.toFixed(2)}</p>

		<div class="flex flex-wrap items-center gap-4">
			<button
				on:click={addToCart}
				class="rounded bg-green-600 px-4 py-2 text-white"
				disabled={item.is_available === false}
			>
				+ Add to Cart
			</button>

			<input
				type="datetime-local"
				bind:value={orderTime}
				class="rounded border p-2"
				disabled={item.is_available === false}
			/>

			<button
				on:click={placeOrder}
				class="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
				disabled={item.is_available === false}
			>
				Schedule Order
			</button>
		</div>

		<section class="space-y-4">
			<h2 class="text-2xl font-semibold">Reviews</h2>
			{#if reviews.length}
				{#each reviews as r (r.id)}
					<div class="rounded border bg-gray-50 p-4">
						<div class="mb-2 flex items-center">
							{#each [1, 2, 3, 4, 5] as star (star)}
								{#if star <= r.rating}⭐{:else}☆{/if}
							{/each}
							<span class="ml-2 text-sm text-gray-600">({r.rating} out of 5)</span>
						</div>
						<p class="mb-1 text-gray-800">{r.comment}</p>
						<div class="text-xs text-gray-500">
							Reviewed by Anonymous on {new Date(r.created_at).toLocaleDateString()}
						</div>
					</div>
				{/each}
			{:else}
				<p class="text-gray-500">No reviews yet.</p>
			{/if}
		</section>

		<section class="space-y-2">
			{#if data.user}
				<h2 class="text-xl font-semibold">Leave a Review</h2>
				<div class="flex items-center space-x-1 text-2xl">
					{#each [1, 2, 3, 4, 5] as n (n)}
						<button
							type="button"
							class="focus:outline-none"
							on:click={() => (rating = n)}
							aria-label="{n} star"
						>
							{#if n <= rating}★{:else}☆{/if}
						</button>
					{/each}
				</div>
				<textarea
					bind:value={comment}
					placeholder="Your comment..."
					class="w-full rounded border p-2"
				></textarea>
				<button on:click={submitReview} class="rounded bg-purple-600 px-4 py-2 text-white">
					Submit Review
				</button>
			{/if}
		</section>
	</div>
{/if}