<script lang="ts">
  export let data;
  let favorites: any[]; // eslint-disable-line @typescript-eslint/no-explicit-any
  $: ({ favorites } = data);

  const imageMap: { [key: string]: string } = {
    'Plain Khicuri': '/images/khichuri.jpg'
  };
  function imgFor(it: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    if (it.image_url) return it.image_url;
    if (imageMap[it.name]) return imageMap[it.name];
    const fileName = it.name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');
    return `/images/${fileName}.jpg`;
  }
</script>

<div class="p-8">
  <h1 class="text-2xl font-bold mb-6">❤️ Your Favorites</h1>

  {#if favorites.length}
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {#each favorites as item (item.id)}
        <a
          href={`/item/${item.id}`}
          class="block bg-white border rounded-lg overflow-hidden shadow hover:shadow-lg transition"
        >
          <img
            src={imgFor(item)}
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
    <p class="text-gray-500">You have no favorites yet.</p>
  {/if}
</div>
