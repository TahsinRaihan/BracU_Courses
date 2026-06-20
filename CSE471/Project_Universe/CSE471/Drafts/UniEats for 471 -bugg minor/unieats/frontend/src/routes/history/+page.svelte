
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
        <div class="bg-white p-4 rounded-lg shadow">
          <div class="flex justify-between items-center">
            <div>{new Date(o.created_at).toLocaleDateString()}</div>
            <div class="px-2 py-1 rounded-full text-sm {statusBadge(o.status)}">
              {o.status}
            </div>
          </div>
          <div class="mt-3 space-y-1">
            {#each o.order_items as oi (oi.menu_items.id)}
              <div class="flex justify-between">
                <span>{oi.menu_items.name} ×{oi.quantity}</span>
                <span>৳{(oi.menu_items.price * oi.quantity).toFixed(2)}</span>
              </div>
            {/each}
          </div>
          <div class="mt-3 text-right font-semibold">
            Total: ৳{o.order_items.reduce((sum: number, oi: any /* eslint-disable-line @typescript-eslint/no-explicit-any */) => sum + oi.quantity * oi.menu_items.price, 0).toFixed(2)}
          </div>
          {#if o.scheduled_at}
            <div class="mt-1 text-sm text-gray-600">
              Scheduled for {new Date(o.scheduled_at).toLocaleString()}
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {:else}
    <p class="text-gray-500">No past orders found.</p>
  {/if}
</div>
