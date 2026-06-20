<script lang="ts">
  import * as suggestionsController from '$lib/controllers/suggestionsController';
  let title = '';
  let description = '';

  async function propose() {
    const { error } = await suggestionsController.submitSuggestion(title, description);
    if (error) alert(error.message);
    else {
      alert('Thanks for your suggestion!');
      title = '';
      description = '';
    }
  }
</script>

<div class="min-h-screen p-8">
  <div class="max-w-4xl mx-auto w-full bg-gradient-to-br from-green-50 to-green-100 p-8 rounded-lg shadow-2xl transform transition-all duration-300 hover:scale-105">
    <div class="text-center mb-8 p-6 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-lg shadow-md">
      <h1 class="text-4xl font-extrabold mb-2">💡 Share Your Brilliant Ideas!</h1>
      <p class="text-lg opacity-90">
        Your creativity fuels UniEats. Suggest new items, features, or improvements!
      </p>
    </div>

    <div class="mb-6">
      <label for="title" class="block text-sm font-medium text-gray-700 mb-2">Suggestion Title</label>
      <input
        type="text"
        id="title"
        bind:value={title}
        placeholder="e.g., New Vegan Burger, Faster Delivery Option"
        class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>

    <div class="mb-6">
      <label for="description" class="block text-sm font-medium text-gray-700 mb-2">Detailed Description</label>
      <textarea
        id="description"
        bind:value={description}
        rows="6"
        placeholder="Tell us more about your suggestion. Be as detailed as possible!"
        class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      ></textarea>
    </div>

    <div class="mb-8">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Quick Suggestions (Click to add to description):</h2>
      <div class="flex flex-wrap gap-3">
        <button
          on:click={() => description += ' (Gluten-Free Option)'}
          class="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          🌾 Gluten-Free Option
        </button>
        <button
          on:click={() => description += ' (Vegan Friendly)'}
          class="px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
        >
          🌱 Vegan Friendly
        </button>
        <button
          on:click={() => description += ' (Less Oil/Healthy)'}
          class="px-4 py-2 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium hover:bg-yellow-200 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2"
        >
          🥗 Less Oil/Healthy
        </button>
        <button
          on:click={() => description += ' (More Vegetarian Options)'}
          class="px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-sm font-medium hover:bg-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
        >
          🥦 More Vegetarian Options
        </button>
        <button
          on:click={() => description += ' (New Dessert Idea)'}
          class="px-4 py-2 bg-pink-100 text-pink-800 rounded-full text-sm font-medium hover:bg-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:ring-offset-2"
        >
          🍰 New Dessert Idea
        </button>
        <button
          on:click={() => description += ' (More Spicy Options)'}
          class="px-4 py-2 bg-red-100 text-red-800 rounded-full text-sm font-medium hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          🌶️ More Spicy Options
        </button>
        <button
          on:click={() => description += ' (Breakfast Menu)'}
          class="px-4 py-2 bg-orange-100 text-orange-800 rounded-full text-sm font-medium hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
        >
          🍳 Breakfast Menu
        </button>
        <button
          on:click={() => description += ' (Local Cuisine)'}
          class="px-4 py-2 bg-teal-100 text-teal-800 rounded-full text-sm font-medium hover:bg-teal-200 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
        >
          🍜 Local Cuisine
        </button>
      </div>
    </div>

    <div>
      <button
        on:click={propose}
        class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-lg font-medium rounded-md text-white bg-gradient-to-r from-emerald-600 to-green-700 hover:from-emerald-700 hover:to-green-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-lg transform transition-all duration-300 hover:scale-105"
      >
        Submit Your Suggestion
      </button>
    </div>
  </div>
</div>
