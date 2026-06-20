<script lang="ts">
	export let show: boolean;
	export let title: string;
	export let message: string;
	export let onConfirm: () => void;
</script>

{#if show}
	<div
		class="bg-opacity-50 fixed inset-0 z-50 flex h-full w-full items-center justify-center overflow-y-auto bg-gray-600"
	>
		<div class="animate-fade-in relative w-96 rounded-md border bg-white p-8 text-center shadow-lg">
			<h3 class="mb-4 text-2xl font-bold text-green-600">{title}</h3>
			<p class="mb-6 text-gray-700">{message}</p>
			<button
				on:click={onConfirm}
				class="rounded bg-green-600 px-6 py-2 text-lg text-white hover:bg-green-700 focus:outline-none"
			>
				Awesome!
			</button>
		</div>
	</div>
{/if}

<style>
	.animate-fade-in {
		animation: fadeIn 0.3s ease-out;
	}
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(-20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
