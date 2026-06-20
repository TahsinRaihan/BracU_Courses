<script>
  import '../app.css';
  import { supabase } from '$lib/supabase';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { notifications } from '$lib/stores/notifications';

  let collapsed = false;
  let notifOpen = false;
  let user = null;

  // count unread
  $: unread = $notifications.filter(n => !n.seen).length;

  onMount(async () => {
    const {
      data: { session }
    } = await supabase.auth.getSession();
    user = session?.user ?? null;
    supabase.auth.onAuthStateChange((_e, s) => {
      user = s?.user ?? null;
    });
  });

  async function logout() {
    await supabase.auth.signOut();
    goto('/login');
  }
</script>

<div class="flex flex-col h-screen">
  <!-- Top Header -->
  <header class="flex items-center justify-between bg-[#e5c8a8] p-4 z-30">
    <button
      on:click={() => (collapsed = !collapsed)}
      class="p-2 bg-white rounded"
      aria-label="Toggle sidebar"
    >
      {#if collapsed}➡️{:else}⬅️{/if}
    </button>

    <div class="text-2xl font-black">UniEats</div>

    <div class="flex items-center space-x-2">
      {#if user}
        <a
          href="/cart"
          class="px-3 py-1 bg-green-600 text-white rounded flex items-center"
          aria-label="View cart"
        >
          🛒
        </a>

        <!-- Notification Bell -->
        <button
          class="relative px-3 py-1 bg-white rounded"
          on:click={() => (notifOpen = !notifOpen)}
          aria-label="Notifications"
        >
          🔔
          {#if unread}
            <span class="absolute top-0 right-0 inline-flex items-center justify-center px-1 text-xs font-bold text-red-100 bg-red-600 rounded-full">
              {unread}
            </span>
          {/if}
        </button>

        <button
          on:click={logout}
          class="px-3 py-1 bg-red-600 text-white rounded"
        >
          Logout
        </button>
      {:else}
        <a href="/login" class="px-3 py-1 bg-blue-600 text-white rounded">Login</a>
        <a href="/signup" class="px-3 py-1 bg-green-600 text-white rounded">Sign Up</a>
      {/if}
    </div>
  </header>

  <!-- Notification Panel -->
  <aside
    class="fixed top-16 right-0 h-full bg-white shadow-lg transform transition-transform z-40"
    class:translate-x-full={!notifOpen}
    style="width:16rem;"
  >
    <div class="flex items-center justify-between p-4 border-b">
      <h2 class="font-bold">Notifications</h2>
      <button on:click={() => notifications.markAllSeen()} class="text-sm">Mark all read</button>
    </div>
    <div class="p-4 space-y-3 overflow-y-auto h-[calc(100%-4rem)]">
      {#if $notifications.length}
        {#each $notifications as note}
          <div class="p-2 rounded border-l-4"
               class:border-green-500={note.type==='success'}
               class:border-blue-500={note.type==='info'}
               class:border-red-500={note.type==='error'}>
            <div class="text-sm">{note.message}</div>
            <div class="text-xs text-gray-500">{new Date(note.timestamp).toLocaleString()}</div>
            {#if note.counter}
              <div class="text-xs text-gray-700">Pick up at Counter {note.counter}</div>
            {/if}
          </div>
        {/each}
      {:else}
        <p class="text-gray-500 text-sm">No notifications yet.</p>
      {/if}
    </div>
  </aside>

  <div class="flex flex-1 overflow-hidden">
    <!-- Sidebar (unchanged) -->
    <aside class="bg-[#e5c8a8]/20 p-4 overflow-y-auto transition-all duration-300"
           class:w-16={collapsed}
           class:w-48={!collapsed}>
      <nav class="space-y-3">
        <a href="/" class="flex items-center p-2 rounded hover:bg-white">
          <span class="text-xl">🏠</span>{#if !collapsed}<span class="ml-2">Dashboard</span>{/if}
        </a>
        <a href="/menu" class="flex items-center p-2 rounded hover:bg-white">
          <span class="text-xl">🍴</span>{#if !collapsed}<span class="ml-2">Menu</span>{/if}
        </a>
        <a href="/cart" class="flex items-center p-2 rounded hover:bg-white">
          <span class="text-xl">🛒</span>{#if !collapsed}<span class="ml-2">Cart</span>{/if}
        </a>
        <a href="/favorites" class="flex items-center p-2 rounded hover:bg-white">
          <span class="text-xl">❤️</span>{#if !collapsed}<span class="ml-2">Favorites</span>{/if}
        </a>
        <a href="/history" class="flex items-center p-2 rounded hover:bg-white">
          <span class="text-xl">📜</span>{#if !collapsed}<span class="ml-2">History</span>{/if}
        </a>
        <a href="/feedback" class="flex items-center p-2 rounded hover:bg-white">
          <span class="text-xl">🗣️</span>{#if !collapsed}<span class="ml-2">Feedback</span>{/if}
        </a>
        <a href="/suggestions" class="flex items-center p-2 rounded hover:bg-white">
          <span class="text-xl">💡</span>{#if !collapsed}<span class="ml-2">Suggestions</span>{/if}
        </a>
      </nav>
    </aside>

    <!-- Main Content (background unchanged) -->
    <main class="flex-1 overflow-y-auto p-4">
      <slot />
    </main>
  </div>
</div>
