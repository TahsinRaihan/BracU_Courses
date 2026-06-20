<script lang="ts">
  export let form: { success?: boolean; message?: string } | undefined;
</script>

<div class="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
  <div class="max-w-xl w-full bg-white p-8 rounded-xl shadow-lg">
    <div class="flex items-center mb-6">
      <svg class="h-8 w-8 text-purple-600 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
      <h1 class="text-3xl font-bold text-gray-800">Share Your Feedback</h1>
    </div>

    <p class="text-gray-600 mb-6">
      We value your opinion! Let us know about your experience or if you have any complaints.
    </p>

    {#if form?.success}
      <div class="mb-4 rounded-md bg-green-100 p-4 text-green-800 border border-green-200">
        <strong>Thank you!</strong> Your feedback has been submitted successfully.
      </div>
    {:else if form?.message}
      <div class="mb-4 rounded-md bg-red-100 p-4 text-red-800 border border-red-200">
        <strong>Oops!</strong> {form.message}
      </div>
    {/if}

    <form method="post" class="space-y-4">
      <div>
        <label for="content" class="block text-sm font-medium text-gray-700 mb-1">Your Message</label>
        <textarea
          id="content"
          name="content"
          rows="6"
          placeholder="Tell us what you think..."
          class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 transition duration-150 ease-in-out"
          required
        ></textarea>
      </div>
      <button type="submit" class="w-full bg-purple-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-transform transform hover:scale-105">
        Submit Feedback
      </button>
    </form>
  </div>
</div>