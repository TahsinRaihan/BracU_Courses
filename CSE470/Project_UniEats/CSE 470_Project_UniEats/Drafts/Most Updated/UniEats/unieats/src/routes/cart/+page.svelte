<script lang="ts">
  import * as cartController from '$lib/controllers/cartController';
  import { notifications } from '$lib/stores/notifications';
  import { invalidate } from '$app/navigation';
  import SuccessModal from '$lib/components/SuccessModal.svelte';

  export let data;
  let localCart: any[] = []; 
  let localScheduled: any[] = []; 

  
  $: if (data) {
    localCart = data.cart;
    localScheduled = data.scheduled;
  }

  // Payment state
  let directPayment = 'COD';
  let directTxn     = '';
  let schedPayment  = 'COD';
  let schedTxn      = '';

  let loading = false; 
  let showSuccessModal = false;
  let successMessage = '';

 
  $: directSub = localCart.reduce((sum, c) => sum + c.qty * c.item.price, 0);
  $: schedSub  = localScheduled.reduce((sum, o) => sum + o.qty * o.item.price, 0);

  async function changeQty(cartId: string, diff: number) {
    const newData = await cartController.changeCartItemQuantity(cartId, diff);
    localCart = newData.cart;
    localScheduled = newData.scheduled;
  }

  async function cancelOrder(orderId: string, type: 'direct' | 'scheduled') {
 
    if (type === 'direct') {
      localCart = localCart.filter(item => item.cartId !== orderId);
    } else {
      localScheduled = localScheduled.filter(item => item.orderId !== orderId);
    }


    await cartController.cancelOrder(orderId, type);


    invalidate('/cart');
  }

  async function payDirect() {
    if (directPayment === 'Online' && (!directTxn || directTxn.length !== 8)) {
      notifications.notify('Please enter a valid 8-digit Transaction ID for Online payment.', 'error');
      return;
    }
    loading = true; 
    try {
      const newData = await cartController.payDirectOrders(localCart, directPayment, directTxn);
      localCart = newData.cart;
      localScheduled = newData.scheduled;
      successMessage = `Your direct order has been placed! Total: ৳${directSub.toFixed(2)}.`;
      showSuccessModal = true;
    } finally {
      loading = false; // Always reset loading state
    }
  }

  async function payScheduled() {
    if (schedPayment === 'Online' && (!schedTxn || schedTxn.length !== 8)) {
      notifications.notify('Please enter a valid 8-digit Transaction ID for Online payment.', 'error');
      return;
    }
    loading = true; 
    try {
      const newData = await cartController.payScheduledOrders(localScheduled, schedPayment, schedTxn);
      localCart = newData.cart;
      localScheduled = newData.scheduled;
      successMessage = `Your scheduled orders have been confirmed! Total: ৳${schedSub.toFixed(2)}.`;
      showSuccessModal = true;
    } finally {
      loading = false; 
    }
  }

  function statusBadge(s: string) { 
    return {
      paid: 'bg-green-200 text-green-800',
      pending: 'bg-yellow-200 text-yellow-800',
      cancelled: 'bg-red-200 text-red-800'
    }[s] ?? 'bg-gray-200 text-gray-800';
  }
</script>

<div class="p-8 max-w-3xl mx-auto space-y-12">
  <h1 class="text-2xl font-semibold">Your Cart</h1>

  <!-- Scheduled Orders -->
  <section class="bg-white p-6 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">🕒 Scheduled Orders</h2>
    {#if localScheduled.length}
      <table class="w-full text-left mb-4">
        <thead>
          <tr><th>Item</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr>
        </thead>
        <tbody>
          {#each localScheduled as o (o.orderId)}
            <tr class="border-b">
              <td class="py-2">{o.item.name}</td>
              <td class="py-2">৳{o.item.price}</td>
              <td class="py-2 flex items-center">
                
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
          class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading}
        >
          {#if loading}Processing...{:else}Pay Scheduled Orders{/if}
        </button>
      </div>
    {:else}
      <p class="text-gray-500">No scheduled orders.</p>
    {/if}
  </section>

  
  <section class="bg-white p-6 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">🛒 Direct Orders</h2>
    {#if localCart.length}
      <table class="w-full text-left mb-4">
        <thead>
          <tr><th>Item</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr>
        </thead>
        <tbody>
          {#each localCart as c (c.cartId)}
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
          class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
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
  onConfirm={() => { showSuccessModal = false; }}
/>