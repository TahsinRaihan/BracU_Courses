
<script lang="ts">
  export let data;
  let orders: any[]; // eslint-disable-line @typescript-eslint/no-explicit-any
  $: ({ orders } = data);

  function statusBadge(s: string) {
    return {
      paid: 'bg-green-200 text-green-800',
      pending: 'bg-yellow-200 text-yellow-800',
      cancelled: 'bg-red-200 text-red-800'
    }[s] ?? 'bg-gray-200 text-gray-800';
  }
</script>

<div class="p-8 space-y-6">
  <h1 class="text-2xl font-bold">Order History</h1>

  {#if orders.length}
    <div class="grid gap-6">
      {#each orders as o (o.id)}
        <div class="bg-white p-6 rounded-lg shadow-md border border-gray-200 transition-all duration-200 hover:shadow-lg hover:border-blue-300">
          <div class="flex justify-between items-center mb-3 pb-2 border-b border-gray-200">
            <h3 class="text-xl font-bold text-gray-800">Order on {new Date(o.created_at).toLocaleDateString()}</h3>
            <div class="flex items-center space-x-2 px-3 py-1 rounded-full text-sm {statusBadge(o.status)}">
              {#if o.status === 'paid'}✅{:else if o.status === 'pending'}⏳{:else if o.status === 'cancelled'}❌{/if}
              <span class="font-medium">{o.status.toUpperCase()}</span>
            </div>
          </div>
          <div class="space-y-2">
            {#each o.order_items as oi (oi.menu_items.id)}
              <div class="flex justify-between text-gray-700">
                <span class="font-semibold">{oi.menu_items.name} <span class="text-sm text-gray-500">×{oi.quantity}</span></span>
                <span class="font-bold">
                  ৳{oi.menu_items.price !== null && oi.menu_items.price !== undefined && oi.menu_items.price > 0
                    ? (oi.menu_items.price * oi.quantity).toFixed(2)
                    : 'N/A'}
                </span>
              </div>
            {/each}
          </div>
          <div class="mt-4 pt-3 border-t border-gray-200 flex justify-between items-center">
            <span class="text-lg font-bold text-gray-900">Total:</span>
            <span class="text-2xl font-extrabold text-gray-900">৳{o.order_items.reduce((sum: number, oi: any /* eslint-disable-line @typescript-eslint/no-explicit-any */) =>
              sum + (oi.menu_items.price !== null && oi.menu_items.price !== undefined ? oi.menu_items.price : 0) * oi.quantity, 0).toFixed(2)}</span>
          </div>
          {#if o.scheduled_at}
            <div class="mt-2 text-sm text-gray-600 text-right">
              <span class="font-semibold">Scheduled for:</span> <span class="font-bold">{new Date(o.scheduled_at).toLocaleString()}</span>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {:else}
    <p class="text-gray-500">No past orders found.</p>
  {/if}
</div>
