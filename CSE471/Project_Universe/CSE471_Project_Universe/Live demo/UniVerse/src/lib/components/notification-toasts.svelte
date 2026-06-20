<script lang="ts">
  import { toasts } from '$lib/stores/notifications'
</script>

<div class="fixed top-4 right-4 z-50 flex flex-col gap-3">
  {#each $toasts as t (t.id)}
    <div class="w-80 rounded-md border border-white/10 bg-black/80 text-white shadow-lg backdrop-blur p-3">
      <div class="text-sm font-semibold">{t.title}</div>
      <div class="text-xs opacity-80 mt-1">{t.message}</div>
    </div>
  {/each}
  {#if !$toasts || $toasts.length === 0}
    <!-- empty -->
  {/if}
  
</div>


