<script lang="ts">
  import { page } from '$app/stores';
  import SearchBar from '$lib/components/menu/SearchBar.svelte';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import type { Category } from '$lib/models/Category';
  import type { MenuItem } from '$lib/models/MenuItem';

  export let data: {
    items: (MenuItem & { is_favorite: boolean })[];
    total: number;
    categories: Category[];
    grouped: { [key: number]: (MenuItem & { is_favorite: boolean })[] };
    searchQuery: string;
  };

  let { categories, items, grouped, searchQuery } = data;

  let search = searchQuery;
  let searchTimeout: ReturnType<typeof setTimeout>; // Correct type for setTimeout return

  // Reactive filtered data
  let filteredItems = data.items;
  let filteredGrouped = data.grouped;

  $: {
    if (search) {
      const lowerCaseSearch = search.toLowerCase();
      filteredItems = data.items.filter(item => 
        item.name.toLowerCase().includes(lowerCaseSearch) || 
        item.description.toLowerCase().includes(lowerCaseSearch)
      );
      // Re-group filtered items
      filteredGrouped = {};
      for (const item of filteredItems) {
        if (!filteredGrouped[item.category_id]) {
          filteredGrouped[item.category_id] = [];
        }
        filteredGrouped[item.category_id].push(item);
      }
    } else {
      filteredItems = data.items;
      filteredGrouped = data.grouped;
    }
  }

  console.log('Menu page loaded. Initial searchQuery:', searchQuery);

  $: suggestions = [...data.categories.map((c: Category) => c.name), ...data.items.map((i: MenuItem) => i.name)];

  function debounceSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      // No longer navigate, just update the search variable
      // const url = new URL($page.url);
      // url.searchParams.set('search', search);
      // goto(url, { keepFocus: true, replaceState: true });
    }, 300);
  }

  onMount(() => {
    if (search) {
      const firstMatch = document.querySelector(`[data-item-name*="${search}" i]`);
      if (firstMatch) {
        firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  });

  const imageMap: { [key: string]: string } = {
    'Chicken Biryani':        '/images/chicken-biryani.jpg',
    'Polao Rice':             '/images/polao-rice.jpg',
    'Fried Rice':             '/images/fried-rice.jpg',
    'Plain White Rice':       '/images/plain-white-rice.jpg',
    'Plain Khichuri':         '/images/khichuri.jpg',
    'Kacchi':                 '/images/kacchi.jpg',
    'Chicken Curry':          '/images/chicken-curry.jpg',
    'Beef Curry':             '/images/beef-curry.jpg',
    'Fish Curry':             '/images/fish-curry.jpg',
    'Egg Curry':              '/images/egg-curry.jpg',
    'Mixed Vegetable Curry':  '/images/mixed-vegetable-curry.jpg',
    'Masoor Dal':             '/images/masoor-dal.jpg',
    'Moong Dal':              '/images/moong-dal.jpg',
    'Chana Masala':           '/images/chana-masala.jpg',
    'Roti':                   '/images/roti.jpg',
    'Paratha':                '/images/paratha.jpg',
    'Butter Naan':            '/images/butter-naan.jpg',
    'Vegetable Samosa':       '/images/vegetable-samosa.jpg',
    'Fuchka (Pani Puri)':     '/images/fuchka-pani-puri.jpg',
    'Vegetable Pakora':       '/images/vegetable-pakora.jpg',
    'Singara':                '/images/singara.jpg',
    'Milk Tea':               '/images/milk-tea.jpg',
    'Sweet Lassi':            '/images/sweet-lassi.jpg',
    'Soft Drinks (Coke/Sprite)': '/images/soft-drinks.jpg',
    'Mishti Doi':             '/images/mishti-doi.jpg',
    'Firni':                  '/images/firni.jpg',
    'Mint Chutney':           '/images/mint-chutney.jpg',
    'Pizza Slice':            '/images/pizza-slice.jpg',
    'Sandwich':               '/images/sandwich.jpg',
    'Burger':                 '/images/burger.jpg',
    'Shawarma':               '/images/shawarma.jpg'
  };

  function imgFor(item: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    return encodeURI(imageMap[item.name] || '/images/default.png');
  }

  // background / pill colors
  const sectionBg  = ['bg-red-50','bg-green-50','bg-blue-50','bg-yellow-50','bg-purple-50','bg-pink-50'];
  const pillColors = ['bg-red-200','bg-green-200','bg-blue-200','bg-yellow-200','bg-purple-200','bg-pink-200'];

  function scrollTo(id: number) {
    document.getElementById(`cat-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
</script>

<div class="h-full overflow-y-auto">
  <!-- Hero Banner -->
  <div
    class="h-64 bg-cover bg-center relative"
    style="background-image:url('https://source.unsplash.com/1200x400/?bangladesh%20canteen')"
  >
    <div class="absolute inset-0 bg-black/60 flex items-center justify-center">
      <h1 class="text-5xl italic text-white font-black">"Savor the Flavors of Home"</h1>
    </div>
  </div>

  <!-- Search Bar -->
  <SearchBar bind:search={search} suggestions={suggestions} on:input={debounceSearch} />

  <!-- Category Pills -->
  <div class="sticky top-20 bg-white/90 backdrop-blur py-2 z-10 overflow-x-auto">
    <div class="flex gap-2 px-4">
      <button
        type="button"
        on:click={() => { 
          search = ''; 
          const url = new URL($page.url);
          url.searchParams.set('search', '');
          goto(url, { keepFocus: true });
        }}
        class="px-4 py-2 rounded-full border bg-gray-200"
      >All</button>
      {#each categories as c, idx (c.id)}
        {#if grouped[c.id]?.length}
          <button
            type="button"
            on:click={() => scrollTo(c.id)}
            class={`px-4 py-2 rounded-full border ${pillColors[idx % pillColors.length]}`}
          >
            {c.name}
          </button>
        {/if}
      {/each}
    </div>
  </div>

  <!-- Menu Sections -->
        {#each categories as c, idx (c.id)}
    {#if filteredGrouped[c.id]?.length}
      <section
        id={"cat-" + c.id}
        class={`px-6 py-8 ${sectionBg[idx % sectionBg.length]} mx-4 rounded-lg shadow-lg mb-8`}
      >
        <h2 class="text-3xl font-bold mb-4">{c.name}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each filteredGrouped[c.id] as item (item.id)}
            <a
              href={`/item/${item.id}`}
              class="relative block border rounded-lg overflow-hidden shadow-md hover:shadow-lg bg-white transition-all duration-300"
              data-item-name={item.name}
            >
              <img
                src={imgFor(item)}
                alt={item.name}
                class="w-full h-48 object-cover bg-gray-100"
              />

              {#if item.is_available === false}
                <div
                  class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center text-xl font-bold"
                >
                  Out of Stock
                </div>
              {/if}

              <div class="p-4">
                <div class="flex justify-between">
                  <h3 class="font-semibold">{item.name}</h3>
                  <span class="text-lg">৳{item.price}</span>
                </div>
                <p class="text-sm mt-2">{item.description}</p>
                <div class="mt-2 text-blue-600 hover:underline">Details →</div>
              </div>
            </a>
          {/each}
        </div>
      </section>
    {/if}
  {/each}
</div>


<style>
  /* For Webkit-based browsers (Chrome, Safari) */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  ::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
</style>