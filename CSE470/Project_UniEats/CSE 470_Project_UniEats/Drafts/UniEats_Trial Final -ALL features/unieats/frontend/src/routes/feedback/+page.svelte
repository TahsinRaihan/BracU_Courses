<script>
  import { supabase } from '$lib/supabase';
  let content = '';

  async function send() {
    const user = (await supabase.auth.getUser()).data.user;
    const { error } = await supabase.from('feedback').insert({
      user_id: user.id,
      content
    });
    if (error) alert(error.message);
    else {
      alert('Thanks for your feedback!');
      content = '';
    }
  }
</script>

<div class="p-8 max-w-lg mx-auto">
  <h1 class="text-2xl font-semibold mb-4">Feedback / Complaints</h1>
  <textarea
    bind:value={content}
    rows="5"
    placeholder="Your message..."
    class="w-full border p-2 rounded mb-4"
  ></textarea>
  <button on:click={send} class="bg-purple-600 text-white px-4 py-2 rounded">
    Submit Feedback
  </button>
</div>
