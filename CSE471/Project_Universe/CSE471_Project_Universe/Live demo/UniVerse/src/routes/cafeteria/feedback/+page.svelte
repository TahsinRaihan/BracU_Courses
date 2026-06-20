<script lang="ts">
	export let form: { success?: boolean; message?: string } | undefined;
	export let data;
	let { feedback } = data;
</script>

<div class="min-h-screen bg-gradient-to-br from-purple-100 via-red-100 to-yellow-100 p-4 sm:p-6 md:p-8">
	<div class="mx-auto max-w-4xl">
		<div class="mb-8 rounded-2xl bg-white/30 p-6 shadow-2xl backdrop-blur-lg sm:p-8">
			<div class="mb-6 flex items-center">
				<div class="mr-4 rounded-full bg-white p-3 shadow-lg">
					<svg class="h-10 w-10 text-purple-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
					</svg>
				</div>
				<h1 class="text-5xl font-black tracking-tighter text-gray-800">Share Your Thoughts</h1>
			</div>

			<p class="mb-8 text-lg text-gray-700">
				Your voice matters. Help us improve by sharing your feedback or complaints.
			</p>

			{#if form?.success}
				<div class="mb-4 rounded-md border border-green-200 bg-green-100 p-4 text-green-800">
					<strong>Thank you!</strong> Your feedback has been submitted successfully.
				</div>
			{:else if form?.message}
				<div class="mb-4 rounded-md border border-red-200 bg-red-100 p-4 text-red-800">
					<strong>Oops!</strong>
					{form.message}
				</div>
			{/if}

			<form method="post" class="space-y-6">
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
					<div class="relative">
						<label for="type" class="absolute -top-2 left-2 inline-block bg-white/30 px-1 text-xs font-medium text-gray-900">Type</label>
						<select id="type" name="type" class="w-full rounded-lg border-gray-300 bg-white/50 py-3 shadow-sm focus:border-purple-500 focus:ring-purple-500">
							<option>Feedback</option>
							<option>Complaint</option>
						</select>
					</div>
					<div class="relative">
						<label for="category" class="absolute -top-2 left-2 inline-block bg-white/30 px-1 text-xs font-medium text-gray-900">Category</label>
						<select id="category" name="category" class="w-full rounded-lg border-gray-300 bg-white/50 py-3 shadow-sm focus:border-purple-500 focus:ring-purple-500">
							<option>Food Quality</option>
							<option>Service</option>
							<option>Cleanliness</option>
							<option>Other</option>
						</select>
					</div>
				</div>

				<div class="relative">
					<label for="content" class="absolute -top-2 left-2 inline-block bg-white/30 px-1 text-xs font-medium text-gray-900">Your Message</label>
					<textarea id="content" name="content" rows="6" placeholder="Tell us what you think..." class="w-full rounded-lg border-gray-300 bg-white/50 shadow-sm transition duration-150 ease-in-out focus:border-purple-500 focus:ring-purple-500" required></textarea>
				</div>
				<button type="submit" class="w-full transform rounded-lg bg-gradient-to-r from-purple-600 to-red-500 px-4 py-3 font-bold text-white shadow-lg transition-transform hover:scale-105 focus:ring-4 focus:ring-purple-500 focus:ring-offset-2 focus:outline-none">
					Submit Feedback
				</button>
			</form>
		</div>

		<div class="rounded-2xl bg-white/30 p-6 shadow-2xl backdrop-blur-lg sm:p-8">
			<h2 class="mb-6 text-4xl font-black tracking-tighter text-gray-800">Previous Feedback</h2>
			<div class="space-y-6">
				{#each feedback as fb (fb.id)}
					<div class="rounded-lg border border-gray-200/50 bg-white/50 p-5 shadow-md transition-shadow hover:shadow-xl">
						<p class="text-lg text-gray-800">{(fb.content.split('\n\n')[1] || fb.content)}</p>
						<p class="mt-3 text-right text-xs font-medium text-gray-500">
							{new Date(fb.created_at).toLocaleString()}
						</p>
					</div>
				{:else}
					<p class="text-center text-gray-500">No feedback yet. Be the first!</p>
				{/each}
			</div>
		</div>
	</div>
</div>