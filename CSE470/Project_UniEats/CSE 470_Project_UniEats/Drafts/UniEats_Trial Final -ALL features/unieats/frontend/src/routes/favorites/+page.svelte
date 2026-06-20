<script>
  import { supabase } from '$lib/supabase';
  import { onMount } from 'svelte';

  let favorites = [];

  onMount(async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;
    const { data, error } = await supabase
      .from('favorites')
      .select('menu_items(id, name, description, price, image_url)')
      .eq('user_id', user.id);
    if (error) {
      console.error('Error loading favorites:', error);
    } else {
      favorites = data.map(f => f.menu_items);
    }
  });

  const imageMap = {
    'Plain Khicuri': '/images/khichuri.jpg'
  };
  function imgFor(it) {
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
      {#each favorites as item}
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
