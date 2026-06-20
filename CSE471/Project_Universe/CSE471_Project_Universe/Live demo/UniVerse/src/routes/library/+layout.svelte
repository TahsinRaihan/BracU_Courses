<script lang="ts">
	let { children } = $props();
</script>

<div
	class="min-h-screen w-full bg-background text-foreground"
	style="scrollbar-gutter: stable both-edges;"
>
	<main class="w-full max-w-none">
		{@render children?.()}
	</main>
</div>
