
<script>
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabase';
  import { page } from '$app/stores';

  let categories = [];
  let items = [];
  let grouped = {};
  let search = '';

  // pick up ?search=… from URL
  $: {
    const q = new URLSearchParams($page.url.search).get('search');
    if (q !== null) search = q;
  }

 
  const imageMap = {
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

  function imgFor(item) {
    return encodeURI(imageMap[item.name] || '/images/default.png');
  }

  // background / pill colors
  const sectionBg  = ['bg-red-50','bg-green-50','bg-blue-50','bg-yellow-50','bg-purple-50','bg-pink-50'];
  const pillColors = ['bg-red-200','bg-green-200','bg-blue-200','bg-yellow-200','bg-purple-200','bg-pink-200'];

  // for search suggestions
  $: suggestions = [...categories.map(c => c.name), ...items.map(i => i.name)];

  onMount(async () => {
    // load categories
    const { data: cats } = await supabase
      .from('categories')
      .select('*')
      .order('id');
    categories = cats;

    // load menu items (including unavailable ones)
    const { data: all } = await supabase
      .from('menu_items')
      .select('*')
      .order('name');
    items = all;

    applyFilter();
  });

  let filtered = [];
  function applyFilter() {
    const q = search.trim().toLowerCase();
    filtered = items.filter(i => {
      const cat = categories.find(c => c.id === i.category_id)?.name.toLowerCase() || '';
      return i.name.toLowerCase().includes(q) || cat.includes(q);
    });
    groupItems();
  }

  function groupItems() {
    grouped = {};
    for (const c of categories) grouped[c.id] = [];
    for (const i of filtered) grouped[i.category_id]?.push(i);
  }

  function scrollTo(id) {
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
  <div class="sticky top-0 bg-white/90 backdrop-blur p-4 z-20 shadow">
    <input
      type="text"
      bind:value={search}
      placeholder="🔍 Search dishes..."
      on:input={applyFilter}
      list="suggestions"
      class="w-full p-3 border border-[#e5c8a8] rounded-lg text-lg"
    />
    <datalist id="suggestions">
      {#each suggestions as s}
        <option value={s}></option>
      {/each}
    </datalist>
  </div>

  <!-- Category Pills -->
  <div class="sticky top-20 bg-white/90 backdrop-blur py-2 z-10 overflow-x-auto">
    <div class="flex gap-2 px-4">
      <button
        type="button"
        on:click={() => { search = ''; applyFilter(); }}
        class="px-4 py-2 rounded-full border bg-gray-200"
      >All</button>
      {#each categories as c, idx}
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
  {#each categories as c, idx}
    {#if grouped[c.id]?.length}
      <section
        id={"cat-" + c.id}
        class={`px-6 py-8 ${sectionBg[idx % sectionBg.length]} mx-4 rounded-lg shadow-lg mb-8`}
      >
        <h2 class="text-3xl font-bold mb-4">{c.name}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each grouped[c.id] as item}
            <a
              href={`/item/${item.id}`}
              class="relative block border rounded-lg overflow-hidden shadow hover:shadow-md bg-white transition"
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
