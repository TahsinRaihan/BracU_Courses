<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabase';
  import { notifications } from '$lib/stores/notifications';
  import { favorites } from '$lib/stores/favorites';
  import type { Review } from '$lib/models/Review';

  export let data;
  let { item, reviews: initialReviews } = data;

  let user: any = null;
  let orderTime = '';
  let reviews: Review[] = initialReviews;
  let rating = 5;
  let comment = '';

  // Reactive isFav derived from the store
  $: isFav = $favorites.has(item.id);

  onMount(async () => {
    const {
      data: { session }
    } = await supabase.auth.getSession();
    user = session?.user ?? null;

    if (user) {
      favorites.fetchFavorites(user.id);
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
    if (!user) return notifications.notify('Log in first', 'error');

    if (isFav) {
      await favorites.removeFavorite(user.id, item.id);
    } else {
      await favorites.addFavorite(user.id, item.id);
    }
  }

  async function addToCart() {
    if (!user) return notifications.notify('Log in first', 'error');
    if (item.is_available === false) return notifications.notify('This item is unavailable', 'error');

    const { data: existing } = await supabase
      .from('cart_items')
      .select('quantity')
      .match({ user_id: user.id, menu_item_id: item.id })
      .single();

    if (existing) {
      await supabase
        .from('cart_items')
        .update({ quantity: existing.quantity + 1 })
        .match({ user_id: user.id, menu_item_id: item.id });
    } else {
      await supabase
        .from('cart_items')
        .insert({ user_id: user.id, menu_item_id: item.id, quantity: 1 });
    }
    notifications.notify(`✅ Added ${item.name} to cart`, 'success');
  }

  async function placeOrder() {
    if (item.is_available === false) {
      return notifications.notify('This item is unavailable', 'error');
    }
    
    if (!orderTime) {
      return notifications.notify('Select date & time', 'error');
    }
    const dt = new Date(orderTime);
    if (dt <= new Date()) {
      return notifications.notify('Pick a future time', 'error');
    }

    const counter = Math.floor(Math.random() * 3) + 1;

    const { data: newOrd, error: ordErr } = await supabase
      .from('orders')
      .insert({
        user_id: user.id,
        menu_item_id: item.id,
        scheduled_at: orderTime,
        status: 'pending'
      })
      .select('id')
      .single();

    if (ordErr || !newOrd) {
      console.error('Schedule insert error', ordErr);
      return notifications.notify(`Failed to schedule: ${ordErr.message}`, 'error');
    }

    const orderId = newOrd.id;

    const orderItemsPayload = [
      {
        order_id: orderId,
        menu_item_id: item.id,
        quantity: 1,
        price_at_order: item.price
      }
    ];

    const { error: orderItemsError } = await supabase
      .from('order_items')
      .insert(orderItemsPayload);

    if (orderItemsError) {
      console.error('Order items insert error', orderItemsError);
      return notifications.notify(`Failed to add order items: ${orderItemsError.message}`, 'error');
    }

    if (ordErr || !newOrd) {
      console.error('Schedule insert error', ordErr);
      return notifications.notify(`Failed to schedule: ${ordErr.message}`, 'error');
    }

    notifications.notify(
      `🕒 Scheduled for ${dt.toLocaleString()}`,
      'success',
      { counter }
    );
  }

  async function submitReview() {
    if (!comment) return notifications.notify('Write a comment', 'error');
    await supabase.from('reviews').insert({
      user_id: user.id,
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
    notifications.notify('⭐ Review submitted', 'success');
  }
</script>

{#if !item}
  <div class="p-8 text-center">Loading…</div>
{:else}
  <div class="p-8 max-w-3xl mx-auto space-y-6">
    <div class="relative w-full h-64 rounded overflow-hidden shadow-lg">
      <img src={imgFor(item)} alt={item.name} class="object-cover w-full h-full" />
      <button
        class="absolute top-4 right-4 text-3xl"
        on:click={toggleFav}
        aria-label="Toggle favorite"
      >
        {isFav ? '❤️' : '🤍'}
      </button>
      {#if item.is_available === false}
        <div class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center text-xl font-bold">
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
        class="bg-green-600 text-white px-4 py-2 rounded"
        disabled={item.is_available === false}
      >
        + Add to Cart
      </button>

      <input
        type="datetime-local"
        bind:value={orderTime}
        class="border p-2 rounded"
        disabled={item.is_available === false}
      />

      <button
        on:click={placeOrder}
        class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        disabled={item.is_available === false}
      >
        Schedule Order
      </button>
    </div>

    <section class="space-y-4">
      <h2 class="text-2xl font-semibold">Reviews</h2>
      {#if reviews.length}
                {#each reviews as r (r.id)}
          <div class="p-4 border rounded bg-gray-50">
            <div class="flex items-center mb-2">
              {#each [1, 2, 3, 4, 5] as star (star)}
                {#if star <= r.rating}⭐{:else}☆{/if}
              {/each}
              <span class="ml-2 text-sm text-gray-600">({r.rating} out of 5)</span>
            </div>
            <p class="text-gray-800 mb-1">{r.comment}</p>
            <div class="text-xs text-gray-500">Reviewed by Anonymous on {new Date(r.created_at).toLocaleDateString()}</div>
          </div>
        {/each}
      {:else}
        <p class="text-gray-500">No reviews yet.</p>
      {/if}
    </section>

    <section class="space-y-2">
      {#if user}
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
          class="w-full border p-2 rounded"
        ></textarea>
        <button
          on:click={submitReview}
          class="bg-purple-600 text-white px-4 py-2 rounded"
        >
          Submit Review
        </button>
      {/if}
    </section>
  </div>
{/if}