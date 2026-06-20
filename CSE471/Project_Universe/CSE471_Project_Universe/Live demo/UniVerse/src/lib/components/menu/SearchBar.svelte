<script lang="ts">
	export let search = '';
	export let suggestions: string[] = [];
</script>

<div class="sticky top-0 z-20 bg-white/90 p-4 shadow backdrop-blur">
	<input
		type="text"
		bind:value={search}
		placeholder="🔍 Search dishes..."
		on:input
		list="suggestions"
		class="w-full rounded-lg border border-[#e5c8a8] p-3 text-lg"
	/>
	<datalist id="suggestions">
		{#each suggestions as s (s)}
			<option value={s}></option>
		{/each}
	</datalist>
</div>
