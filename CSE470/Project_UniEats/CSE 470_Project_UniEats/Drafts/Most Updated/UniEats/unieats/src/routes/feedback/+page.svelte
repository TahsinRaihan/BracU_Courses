<script lang="ts">
  export let form: { success?: boolean; message?: string } | undefined;
</script>

<div class="min-h-screen p-8">
  <div class="max-w-4xl mx-auto w-full bg-gradient-to-br from-gray-50 to-gray-100 p-8 rounded-lg shadow-2xl transform transition-all duration-300 hover:scale-105">
    <div class="text-center mb-8 p-6 bg-gradient-to-r from-purple-600 to-indigo-500 text-white rounded-lg shadow-md">
      <h1 class="text-4xl font-extrabold mb-2">💬 Share Your Thoughts!</h1>
      <p class="text-lg opacity-90">
        Your feedback helps us make UniEats even better.
      </p>
    </div>

    {#if form?.success}
      <div class="mb-4 rounded-md border border-green-400 bg-green-50 p-4 text-green-700" role="alert">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium">
              Thanks for your feedback!
            </p>
          </div>
        </div>
      </div>
    {:else if form?.message}
      <div class="mb-4 rounded-md border border-red-400 bg-red-50 p-4 text-red-700" role="alert">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium">
              {form.message}
            </p>
          </div>
        </div>
      </div>
    {/if}

    <form method="post" class="space-y-6">
      <div class="mb-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">What kind of feedback is this?</h2>
        <div class="flex flex-wrap gap-3">
          <button
            type="button"
            on:click={() => { (document.getElementById('subject') as HTMLInputElement).value = 'Bug Report'; }}
            class="px-4 py-2 bg-red-100 text-red-800 rounded-full text-sm font-medium hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          >
            🐛 Bug Report
          </button>
          <button
            type="button"
            on:click={() => { (document.getElementById('subject') as HTMLInputElement).value = 'Feature Request'; }}
            class="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            ✨ Feature Request
          </button>
          <button
            type="button"
            on:click={() => { (document.getElementById('subject') as HTMLInputElement).value = 'General Inquiry'; }}
            class="px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
          >
            ❓ General Inquiry
          </button>
          <button
            type="button"
            on:click={() => { (document.getElementById('subject') as HTMLInputElement).value = 'Complaint'; }}
            class="px-4 py-2 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium hover:bg-yellow-200 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2"
          >
            😠 Complaint
          </button>
        </div>
      </div>
      <div>
        <label for="subject" class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
        <input
          type="text"
          id="subject"
          name="subject"
          placeholder="e.g., Bug Report, Feature Request, General Inquiry"
          class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          required
        />
      </div>
      <div>
        <label for="content" class="block text-sm font-medium text-gray-700 mb-2">Your Message</label>
        <textarea
          id="content"
          name="content"
          rows="6"
          placeholder="Please describe your feedback in detail..."
          class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          required
        ></textarea>
      </div>
      <div>
        <button
          type="submit"
          class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-lg font-medium rounded-md text-white bg-gradient-to-r from-purple-600 to-indigo-700 hover:from-purple-700 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-lg transform transition-all duration-300 hover:scale-105"
        >
          Submit Feedback
        </button>
      </div>
    </form>
  </div>
</div>
