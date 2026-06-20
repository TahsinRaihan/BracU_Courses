<script lang="ts">
  import * as feedbackController from '$lib/controllers/feedbackController';
  let content = '';

  async function send() {
    const { error } = await feedbackController.submitFeedback(content);
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
