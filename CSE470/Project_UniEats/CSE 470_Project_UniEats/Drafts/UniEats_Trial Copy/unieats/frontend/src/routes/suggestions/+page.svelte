<script>
  import { supabase } from '$lib/supabase';
  let title = '';
  let description = '';

  async function propose() {
    const user = (await supabase.auth.getUser()).data.user;
    const { error } = await supabase.from('suggestions').insert({
      user_id: user.id,
      title,
      description
    });
    if (error) alert(error.message);
    else {
      alert('Thanks for your suggestion!');
      title = '';
      description = '';
    }
  }
</script>

<div class="p-8 max-w-lg mx-auto">
  <h1 class="text-2xl font-semibold mb-4">Suggest New Items</h1>
  <input
    type="text"
    bind:value={title}
    placeholder="Title"
    class="w-full border p-2 rounded mb-2"
  />
  <textarea
    bind:value={description}
    rows="4"
    placeholder="Description..."
    class="w-full border p-2 rounded mb-4"
  ></textarea>
  <button on:click={propose} class="bg-green-600 text-white px-4 py-2 rounded">
    Submit Suggestion
  </button>
</div>
