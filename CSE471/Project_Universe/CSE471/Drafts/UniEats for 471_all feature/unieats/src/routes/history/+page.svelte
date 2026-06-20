<script lang="ts">
  export let data;
  $: orders = data.orders;
</script>

<div class="p-8 max-w-4xl mx-auto">
  <h1 class="text-4xl font-extrabold text-gray-800 mb-8 text-center">Your Order History</h1>

  {#if !orders || orders.length === 0}
    <div class="bg-white p-6 rounded-lg shadow-md text-center">
      <p class="text-gray-600 text-lg">You haven't placed any orders yet. Start exploring our menu!</p>
      <a href="/menu" class="mt-4 inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition duration-300">Browse Menu</a>
    </div>
  {:else}
    <div class="space-y-6">
      {#each orders as order (order.id)}
        <div class="bg-white p-6 rounded-xl shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 pb-4 border-b border-gray-200">
            <div>
              <h2 class="text-2xl font-bold text-gray-800 mb-1">Order #{order.id}</h2>
              <p class="text-sm text-gray-500">
                Placed on: <span class="font-medium">{new Date(order.created_at).toLocaleDateString()}</span> at <span class="font-medium">{new Date(order.created_at).toLocaleTimeString()}</span>
              </p>
              {#if order.scheduled_at}
                <p class="text-sm text-gray-500">
                  Scheduled for: <span class="font-medium">{new Date(order.scheduled_at).toLocaleString()}</span>
                </p>
              {/if}
            </div>
            <div class="text-right mt-3 sm:mt-0">
              <div class="text-2xl font-extrabold text-gray-900">৳{order.total_amount?.toFixed(2) || '0.00'}</div>
              <span class="text-sm font-semibold px-3 py-1 rounded-full capitalize"
                    class:bg-green-100={order.status === 'delivered' || order.status === 'paid'}
                    class:text-green-800={order.status === 'delivered' || order.status === 'paid'}
                    class:bg-yellow-100={order.status === 'pending'}
                    class:text-yellow-800={order.status === 'pending'}
                    class:bg-red-100={order.status === 'cancelled'}
                    class:text-red-800={order.status === 'cancelled'}>
                {order.status}
              </span>
            </div>
          </div>
          
          <div class="space-y-3 p-4 bg-gray-50 rounded">
            {#each order.order_items as item (item.menu_item.id)}
              <div class="flex justify-between items-center text-gray-700">
                <span class="text-base font-medium">{item.menu_item?.name || 'Item no longer available'}</span>
                <span class="text-sm">x{item.quantity}</span>
                <span class="text-base font-semibold">৳{(item.price_at_order * item.quantity)?.toFixed(2) || '0.00'}</span>
              </div>
            {/each}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
