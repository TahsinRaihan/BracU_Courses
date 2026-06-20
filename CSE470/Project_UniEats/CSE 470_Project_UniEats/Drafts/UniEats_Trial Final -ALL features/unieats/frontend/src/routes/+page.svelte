<script>
  import { supabase } from '$lib/supabase';
  import { onMount } from 'svelte';

  let user = null;
  let daily = [];
  let weekly = [];
  let offers = [];

  // Single imgFor that treats every item the same
  function imgFor(it) {
    // If the DB provided a URL, use it
    if (it.image_url) return it.image_url;

    // Otherwise, kebab-case the name → filename.jpg
    const fileName = it.name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');

    return `/images/${fileName}.jpg`;
  }

  onMount(async () => {
    // 1) session
    const {
      data: { session }
    } = await supabase.auth.getSession();
    user = session?.user ?? null;

    // 2) daily & weekly (case-insensitive)
    const [dRes, wRes] = await Promise.all([
      supabase.from('menu_items').select('id, name, price, image_url').ilike('tag', 'daily'),
      supabase.from('menu_items').select('id, name, price, image_url').ilike('tag', 'weekly')
    ]);

    if (!dRes.error) daily = dRes.data;
    if (!wRes.error) weekly = wRes.data;

    // 3) build pool & fallback to all items if empty
    let pool = [...daily, ...weekly];
    if (!pool.length) {
      const all = await supabase.from('menu_items').select('id, name, price, image_url');
      pool = all.error ? [] : all.data;
    }

    // 4) pick 3 random offers
    const shuffled = pool.sort(() => 0.5 - Math.random());
    offers = shuffled.slice(0, 3).map(item => {
      const isBogo = Math.random() < 0.5;
      return {
        ...item,
        title: isBogo
          ? `Buy 1 Get 1 Free on ${item.name}`
          : `${Math.floor(Math.random() * 31) + 20}% Off on ${item.name}`,
        link: `/item/${item.id}`
      };
    });
  });
</script>

<div class="p-8 space-y-12">
  <!-- OFFERS -->
  <section>
    <h2 class="text-2xl font-bold mb-4">🔥 Current Offers</h2>
    {#if offers.length}
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {#each offers as offer}
          <a
            href={offer.link}
            class="block bg-white border rounded-lg overflow-hidden shadow hover:shadow-lg transition"
          >
            <img
              src={imgFor(offer)}
              alt={offer.title}
              class="w-full h-40 object-cover"
              on:error={(e) => console.error('Image load failed:', imgFor(offer), e)}
            />
            <div class="p-4">
              <h3 class="text-lg font-semibold">{offer.title}</h3>
            </div>
          </a>
        {/each}
      </div>
    {:else}
      <p class="text-gray-500">No offers available.</p>
    {/if}
  </section>

  <!-- DAILY SPECIALS -->
  <section>
    <h2 class="text-2xl font-bold mb-4">🍽️ Daily Specials</h2>
    {#if daily.length}
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {#each daily as item}
          <a
            href={`/item/${item.id}`}
            class="block bg-white border rounded-lg overflow-hidden shadow hover:shadow-lg transition"
          >
            <img
              src={imgFor(item)}
              alt={item.name}
              class="w-full h-40 object-cover"
              on:error={(e) => console.error('Image load failed:', imgFor(item), e)}
            />
            <div class="p-4">
              <h3 class="text-lg font-semibold">{item.name}</h3>
              <p class="mt-1 text-gray-600">৳{item.price.toFixed(2)}</p>
              <div class="mt-2 text-blue-600 hover:underline">Details →</div>
            </div>
          </a>
        {/each}
      </div>
    {:else}
      <p class="text-gray-500">No daily specials available.</p>
    {/if}
  </section>

  <!-- WEEKLY SPECIALS -->
  <section>
    <h2 class="text-2xl font-bold mb-4">📅 Weekly Specials</h2>
    {#if weekly.length}
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {#each weekly as item}
          <a
            href={`/item/${item.id}`}
            class="block bg-white border rounded-lg overflow-hidden shadow hover:shadow-lg transition"
          >
            <img
              src={imgFor(item)}
              alt={item.name}
              class="w-full h-40 object-cover"
              on:error={(e) => console.error('Image load failed:', imgFor(item), e)}
            />
            <div class="p-4">
              <h3 class="text-lg font-semibold">{item.name}</h3>
              <p class="mt-1 text-gray-600">৳{item.price.toFixed(2)}</p>
              <div class="mt-2 text-blue-600 hover:underline">Details →</div>
            </div>
          </a>
        {/each}
      </div>
    {:else}
      <p class="text-gray-500">No weekly specials available.</p>
    {/if}
  </section>
</div>
