<script lang="ts">
	export let form: { success?: boolean; message?: string } | undefined;
	export let data;
	let { suggestions } = data;

	
</script>

<div class="min-h-screen bg-gradient-to-br from-green-100 via-cyan-100 to-blue-100 p-4 sm:p-6 md:p-8">
	<div class="mx-auto max-w-4xl">
		<div class="mb-8 rounded-2xl bg-white/30 p-6 shadow-2xl backdrop-blur-lg sm:p-8">
			<div class="mb-6 flex items-center">
				<div class="mr-4 rounded-full bg-white p-3 shadow-lg">
					<svg class="h-10 w-10 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m12.728 0l-.707.707M6 12a6 6 0 1112 0 6 6 0 01-12 0z" />
					</svg>
				</div>
				<h1 class="text-5xl font-black tracking-tighter text-gray-800">Suggest an Item</h1>
			</div>

			<p class="mb-8 text-lg text-gray-700">
				Got a brilliant idea for a new dish? Let us know!
			</p>

			{#if form?.success}
				<div class="mb-4 rounded-md border border-green-200 bg-green-100 p-4 text-green-800">
					<strong>Thank you!</strong> Your suggestion has been submitted successfully.
				</div>
			{:else if form?.message}
				<div class="mb-4 rounded-md border border-red-200 bg-red-100 p-4 text-red-800">
					<strong>Oops!</strong>
					{form.message}
				</div>
			{/if}

			<form method="post" action="?/submit" class="space-y-6">
				<div class="relative">
					<label for="title" class="absolute -top-2 left-2 inline-block bg-white/30 px-1 text-xs font-medium text-gray-900">Item Name</label>
					<input id="title" name="title" type="text" placeholder="e.g., Spicy Chicken Sandwich" class="w-full rounded-lg border-gray-300 bg-white/50 py-3 shadow-sm focus:border-green-500 focus:ring-green-500" required />
				</div>

				<div class="relative">
					<label for="category" class="absolute -top-2 left-2 inline-block bg-white/30 px-1 text-xs font-medium text-gray-900">Category</label>
					<select id="category" name="category" class="w-full rounded-lg border-gray-300 bg-white/50 py-3 shadow-sm focus:border-green-500 focus:ring-green-500">
						<option>Appetizer</option>
						<option>Main Course</option>
						<option>Dessert</option>
						<option>Beverage</option>
					</select>
				</div>

				<div class="relative">
					<label for="description" class="absolute -top-2 left-2 inline-block bg-white/30 px-1 text-xs font-medium text-gray-900">Description</label>
					<textarea id="description" name="description" rows="4" placeholder="Briefly describe the item..." class="w-full rounded-lg border-gray-300 bg-white/50 shadow-sm focus:border-green-500 focus:ring-green-500"></textarea>
				</div>
				<button type="submit" class="w-full transform rounded-lg bg-gradient-to-r from-green-600 to-cyan-500 px-4 py-3 font-bold text-white shadow-lg transition-transform hover:scale-105 focus:ring-4 focus:ring-green-500 focus:ring-offset-2 focus:outline-none">
					Submit Suggestion
				</button>
			</form>
		</div>

		<div class="rounded-2xl bg-white/30 p-6 shadow-2xl backdrop-blur-lg sm:p-8">
			<h2 class="mb-6 text-4xl font-black tracking-tighter text-gray-800">Previous Suggestions</h2>
			<div class="space-y-6">
				{#each suggestions as s (s.id)}
					<div class="rounded-lg border border-gray-200/50 bg-white/50 p-5 shadow-md transition-shadow hover:shadow-xl">
						<div class="flex items-start justify-between">
							<div>
								<h3 class="text-xl font-bold text-gray-800">{s.title}</h3>
								<p class="mt-1 text-gray-600">{(s.description.split('\n\n')[1] || s.description)}</p>
							</div>
							<form method="POST" action="?/upvote" class="flex items-center space-x-2">
								<input type="hidden" name="suggestion_id" value={s.id} />
								<button type="submit" class="transform rounded-full p-2 text-2xl transition-transform hover:scale-110 hover:bg-blue-100">
									👍
								</button>
								<span class="font-bold text-gray-700">{s.likes || 0}</span>
							</form>
						</div>
						<p class="mt-3 text-right text-xs font-medium text-gray-500">
							{new Date(s.created_at).toLocaleString()}
						</p>
					</div>
				{:else}
					<p class="text-center text-gray-500">No suggestions yet. Be the first!</p>
				{/each}
			</div>
		</div>
	</div>
</div>
