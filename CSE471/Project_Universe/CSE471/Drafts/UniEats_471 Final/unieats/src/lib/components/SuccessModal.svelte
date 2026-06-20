<script lang="ts">
  export let show: boolean;
  export let title: string;
  export let message: string;
  export let onConfirm: () => void;
</script>

{#if show}
<div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
  <div class="relative p-8 border w-96 shadow-lg rounded-md bg-white text-center animate-fade-in">
    <h3 class="text-2xl font-bold text-green-600 mb-4">{title}</h3>
    <p class="text-gray-700 mb-6">{message}</p>
    <button
      on:click={onConfirm}
      class="px-6 py-2 bg-green-600 text-white text-lg rounded hover:bg-green-700 focus:outline-none"
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
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>