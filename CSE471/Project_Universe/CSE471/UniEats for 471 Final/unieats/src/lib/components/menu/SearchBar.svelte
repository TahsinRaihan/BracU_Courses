
<script lang="ts">
  export let search = '';
  export let suggestions: string[] = [];
</script>

<div class="sticky top-0 bg-white/90 backdrop-blur p-4 z-20 shadow">
  <input
    type="text"
    bind:value={search}
    placeholder="🔍 Search dishes..."
    on:input
    list="suggestions"
    class="w-full p-3 border border-[#e5c8a8] rounded-lg text-lg"
  />
  <datalist id="suggestions">
    {#each suggestions as s (s)}
      <option value={s}></option>
    {/each}
  </datalist>
</div>
