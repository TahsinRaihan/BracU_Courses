
<script>
  import { supabase } from '$lib/supabase';
  import { onMount } from 'svelte';
  import { notifications } from '$lib/stores/notifications';

  let cart = [];
  let scheduled = [];

  // Payment state
  let directPayment = 'COD';
  let directTxn     = '';
  let schedPayment  = 'COD';
  let schedTxn      = '';

  // Load direct cart items
  async function loadCart() {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;
    const { data, error } = await supabase
      .from('cart_items')
      .select('id, quantity, menu_items(id,name,price)')
      .match({ user_id: user.id });
    if (!error) {
      cart = data.map(c => ({ cartId: c.id, qty: c.quantity, item: c.menu_items }));
    }
  }

  // Load scheduled orders via two-step fetch
  async function loadScheduled() {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    // 1) fetch pending orders
    const { data: ords = [], error: ordErr } = await supabase
      .from('orders')
      .select('id, scheduled_at, menu_item_id')
      .match({ user_id: user.id, status: 'pending' })
      .order('scheduled_at', { ascending: true });
    if (ordErr) {
      console.error('Error loading scheduled orders:', ordErr);
      return;
    }

    // 2) fetch menu item details
    scheduled = await Promise.all(
      ords.map(async o => {
        const { data: mi, error: miErr } = await supabase
          .from('menu_items')
          .select('id,name,price')
          .eq('id', o.menu_item_id)
          .single();
        if (miErr) {
          console.error('Error loading menu item for order', o.id, miErr);
          return null;
        }
        // default qty to 1
        return { orderId: o.id, at: o.scheduled_at, qty: 1, item: mi };
      })
    ).then(arr => arr.filter(x => x));
  }

  onMount(() => {
    loadCart();
    loadScheduled();
    const unsub = notifications.subscribe(() => loadScheduled());
    return unsub;
  });

  // Change direct quantity
  async function changeQty(cartId, diff) {
    const entry = cart.find(c => c.cartId === cartId);
    const newQty = entry.qty + diff;
    if (newQty < 1) {
      await supabase.from('cart_items').delete().match({ id: cartId });
      notifications.notify('Order cancelled', 'info');
    } else {
      await supabase.from('cart_items').update({ quantity: newQty }).match({ id: cartId });
      notifications.notify('Cart updated', 'success');
    }
    await loadCart();
  }

  // Cancel any order
  async function cancelOrder(orderId, type) {
    if (type === 'direct') {
      await supabase.from('cart_items').delete().match({ id: orderId });
    } else {
      await supabase.from('orders').update({ status: 'cancelled' }).eq('id', orderId);
    }
    notifications.notify('Order cancelled', 'info');
    await loadCart();
    await loadScheduled();
  }

  // Pay direct orders
  async function payDirect() {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return notifications.notify('Log in first', 'error');
    const payload = cart.map(c => ({
      user_id:          user.id,
      menu_item_id:     c.item.id,
      scheduled_at:     new Date().toISOString(),
      status:           'pending',
      quantity:         c.qty,
      payment_method:   directPayment,
      transaction_id:   directPayment === 'Online' ? directTxn : null
    }));
    await supabase.from('orders').insert(payload);
    await supabase.from('cart_items').delete().match({ user_id: user.id });
    notifications.notify('Direct orders placed', 'success');
    await loadCart();
    await loadScheduled();
  }

  // Pay scheduled orders
  async function payScheduled() {
    for (const o of scheduled) {
      await supabase
        .from('orders')
        .update({
          payment_method: o.payment_method ?? schedPayment,
          transaction_id: schedPayment === 'Online' ? schedTxn : null
        })
        .eq('id', o.orderId);
    }
    notifications.notify('Scheduled orders confirmed', 'success');
    await loadScheduled();
  }

  // Subtotals
  $: directSub = cart.reduce((sum, c) => sum + c.qty * c.item.price, 0);
  $: schedSub  = scheduled.reduce((sum, o) => sum + o.qty * o.item.price, 0);
</script>

<div class="p-8 max-w-3xl mx-auto space-y-12">
  <h1 class="text-2xl font-semibold">Your Cart</h1>

  <!-- Scheduled Orders -->
  <section class="bg-white p-6 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">🕒 Scheduled Orders</h2>
    {#if scheduled.length}
      <table class="w-full text-left mb-4">
        <thead>
          <tr><th>Item</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr>
        </thead>
        <tbody>
          {#each scheduled as o}
            <tr class="border-b">
              <td class="py-2">{o.item.name}</td>
              <td class="py-2">৳{o.item.price}</td>
              <td class="py-2 flex items-center">
                <!-- qty buttons disabled until DB column exists -->
                <span class="px-4">{o.qty}</span>
              </td>
              <td class="py-2">৳{(o.qty * o.item.price).toFixed(2)}</td>
              <td class="py-2">
                <button
                  on:click={() => cancelOrder(o.orderId, 'scheduled')}
                  class="bg-red-600 text-white px-3 py-1 rounded"
                >
                  Cancel Order
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
      <div class="text-right font-bold mb-4">Subtotal: ৳{schedSub.toFixed(2)}</div>
      <div class="space-y-4">
        <div class="font-semibold">Payment for Scheduled</div>
        <div class="flex items-center space-x-4">
          <label><input type="radio" bind:group={schedPayment} value="COD" class="mr-2"/>COD</label>
          <label><input type="radio" bind:group={schedPayment} value="Online" class="mr-2"/>Online</label>
        </div>
        {#if schedPayment === 'Online'}
          <input
            type="text"
            bind:value={schedTxn}
            placeholder="Transaction ID"
            class="w-full border p-2 rounded"
          />
        {/if}
        <button
          on:click={payScheduled}
          class="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Pay Scheduled Orders
        </button>
      </div>
    {:else}
      <p class="text-gray-500">No scheduled orders.</p>
    {/if}
  </section>

  <!-- Direct Orders -->
  <section class="bg-white p-6 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">🛒 Direct Orders</h2>
    {#if cart.length}
      <table class="w-full text-left mb-4">
        <thead>
          <tr><th>Item</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr>
        </thead>
        <tbody>
          {#each cart as c}
            <tr class="border-b">
              <td class="py-2">{c.item.name}</td>
              <td class="py-2">৳{c.item.price}</td>
              <td class="py-2 flex items-center">
                <button on:click={() => changeQty(c.cartId, -1)} class="px-2">➖</button>
                <span class="px-2">{c.qty}</span>
                <button on:click={() => changeQty(c.cartId, 1)} class="px-2">➕</button>
              </td>
              <td class="py-2">৳{(c.qty * c.item.price).toFixed(2)}</td>
              <td class="py-2">
                <button
                  on:click={() => cancelOrder(c.cartId, 'direct')}
                  class="bg-red-600 text-white px-3 py-1 rounded"
                >
                  Cancel Order
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
      <div class="text-right font-bold mb-4">Subtotal: ৳{directSub.toFixed(2)}</div>
      <div class="space-y-4">
        <div class="font-semibold">Payment for Direct</div>
        <div class="flex items-center space-x-4">
          <label><input type="radio" bind:group={directPayment} value="COD" class="mr-2"/>COD</label>
          <label><input type="radio" bind:group={directPayment} value="Online" class="mr-2"/>Online</label>
        </div>
        {#if directPayment === 'Online'}
          <input
            type="text"
            bind:value={directTxn}
            placeholder="Transaction ID"
            class="w-full border p-2 rounded"
          />
        {/if}
        <button
          on:click={payDirect}
          class="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Pay Direct Orders
        </button>
      </div>
    {:else}
      <p class="text-gray-500">No direct orders.</p>
    {/if}
  </section>
</div>
