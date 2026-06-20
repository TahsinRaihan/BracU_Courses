<script lang="ts">
  export let data;
  let { specials } = data;
</script>

<div class="p-8">
  <h1 class="text-2xl font-bold mb-6">✨ Today's Specials</h1>

  {#if specials.length}
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {#each specials as item (item.id)}
        <a
          href={`/item/${item.id}`}
          class="block bg-white border rounded-lg overflow-hidden shadow hover:shadow-lg transition"
        >
          <img
            src={item.image_url || '/images/default.png'}
            alt={item.name}
            class="w-full h-40 object-cover"
          />
          <div class="p-4">
            <h3 class="text-lg font-semibold">{item.name}</h3>
            <p class="mt-1 text-gray-600">{item.description}</p>
            <div class="mt-2 flex justify-between items-center">
              <span class="font-bold">৳{item.price.toFixed(2)}</span>
              <span class="text-blue-600 hover:underline">Details →</span>
            </div>
          </div>
        </a>
      {/each}
    </div>
  {:else}
    <p class="text-gray-500">No specials today.</p>
  {/if}
</div>