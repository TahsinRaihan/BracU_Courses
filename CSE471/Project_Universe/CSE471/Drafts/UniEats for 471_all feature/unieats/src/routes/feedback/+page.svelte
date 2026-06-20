<script lang="ts">
  export let form: { success?: boolean; message?: string } | undefined;
</script>

<div class="p-8 max-w-lg mx-auto">
  <h1 class="text-2xl font-semibold mb-4">Feedback / Complaints</h1>

  {#if form?.success}
    <div class="mb-4 rounded border border-green-300 bg-green-50 p-3 text-green-700">
      ✅ Thanks for your feedback!
    </div>
  {:else if form?.message}
    <div class="mb-4 rounded border border-red-300 bg-red-50 p-3 text-red-700">
      {form.message}
    </div>
  {/if}

  <form method="post" class="space-y-3">
    <textarea
      name="content"
      rows="5"
      placeholder="Your message..."
      class="w-full border p-2 rounded"
      required
    ></textarea>
    <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded">
      Submit Feedback
    </button>
  </form>
</div>
