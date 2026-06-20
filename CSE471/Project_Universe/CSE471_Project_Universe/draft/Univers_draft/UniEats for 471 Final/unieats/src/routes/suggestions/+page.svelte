<script lang="ts">
  export let form: { success?: boolean; message?: string } | undefined;
</script>

<div class="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
  <div class="max-w-xl w-full bg-white p-8 rounded-xl shadow-lg">
    <div class="flex items-center mb-6">
      <svg class="h-8 w-8 text-green-600 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m12.728 0l-.707.707M6 12a6 6 0 1112 0 6 6 0 01-12 0z" />
      </svg>
      <h1 class="text-3xl font-bold text-gray-800">Suggest a New Item</h1>
    </div>

    <p class="text-gray-600 mb-6">
      Have a great idea for a new menu item? We'd love to hear it!
    </p>

    {#if form?.success}
      <div class="mb-4 rounded-md bg-green-100 p-4 text-green-800 border border-green-200">
        <strong>Thank you!</strong> Your suggestion has been submitted successfully.
      </div>
    {:else if form?.message}
      <div class="mb-4 rounded-md bg-red-100 p-4 text-red-800 border border-red-200">
        <strong>Oops!</strong> {form.message}
      </div>
    {/if}

    <form method="post" class="space-y-4">
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Item Name</label>
        <input
          id="title"
          name="title"
          type="text"
          placeholder="e.g., Spicy Chicken Sandwich"
          class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-green-500 focus:border-green-500 transition duration-150 ease-in-out"
          required
        />
      </div>
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
        <textarea
          id="description"
          name="description"
          rows="4"
          placeholder="Briefly describe the item..."
          class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-green-500 focus:border-green-500 transition duration-150 ease-in-out"
        ></textarea>
      </div>
      <button type="submit" class="w-full bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-transform transform hover:scale-105">
        Submit Suggestion
      </button>
    </form>
  </div>
</div>