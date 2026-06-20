<script>
  import { supabase } from '$lib/supabase';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  let item, reviews=[], orderTime='', pending=null, rating=5, comment='';
  $: id = page.params.id;
  onMount(async () => {
    item = (await supabase.from('menu_items').select().eq('id',id).single()).data;
    reviews = (await supabase.from('reviews').select().eq('menu_item_id',id)).data;
    pending = (await supabase.from('orders')
      .select().eq('user_id',supabase.auth.user().id)
      .eq('status','pending').limit(1)).data[0];
  });
  async function preorder() {
    await supabase.from('orders').insert({ user_id:supabase.auth.user().id, scheduled_at:orderTime });
    alert('Pre-ordered!');
    pending=true;
  }
  async function cancel() {
    await supabase.from('orders').update({status:'cancelled'}).eq('id',pending.id);
    alert('Cancelled');
    pending=null;
  }
  async function addReview() {
    await supabase.from('reviews').insert({ user_id:supabase.auth.user().id, menu_item_id:id, rating, comment });
    reviews = (await supabase.from('reviews').select().eq('menu_item_id',id)).data;
  }
</script>

<div class="p-8 max-w-md mx-auto">
  <h1 class="text-2xl">{item.name}</h1>
  <p>{item.description}</p>
  <p class="mb-4">${item.price}</p>

  <div class="mb-6">
    <input type="datetime-local" bind:value={orderTime} class="border p-2 mr-2"/>
    <button on:click={preorder} class="bg-green-500 px-4 py-2">Order</button>
    {#if pending}<button on:click={cancel} class="bg-red-500 px-4 py-2 ml-2">Cancel</button>{/if}
  </div>

  <h2 class="font-semibold mb-2">Reviews</h2>
  <ul class="mb-4">{#each reviews as r}<li>{r.rating}★ — {r.comment}</li>{/each}</ul>
  <input type="number" min="1" max="5" bind:value={rating} class="border p-1 w-16 mr-2"/>
  <textarea bind:value={comment} class="border p-2 w-full mb-2" placeholder="Comment…"/>
  <button on:click={addReview} class="bg-blue-500 px-4 py-2">Submit</button>
</div>
