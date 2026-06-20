<script lang="ts">
  import '../app.css';
  import { supabase } from '$lib/supabase';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { notifications } from '$lib/stores/notifications';
  import { fade } from 'svelte/transition'; // Import fade transition

  let collapsed = false;
  let notifOpen = false;
  let user: any = null; // eslint-disable-line @typescript-eslint/no-explicit-any

  // count unread
  $: unread = $notifications.filter(n => !n.seen).length;

  onMount(async () => {
    const {
      data: { session }
    } = await supabase.auth.getSession();
    user = session?.user ?? null;
    supabase.auth.onAuthStateChange((_e: string, s: any) => { // eslint-disable-line @typescript-eslint/no-explicit-any
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
      <div class="flex space-x-2">
        <button on:click={() => notifications.markAllSeen()} class="text-sm text-blue-600 hover:underline">Mark all read</button>
        <button on:click={() => notifications.dismissAll()} class="text-sm text-red-600 hover:underline">Clear all</button>
      </div>
    </div>
    <div class="p-4 space-y-3 overflow-y-auto h-[calc(100%-4rem)]">
      {#if $notifications.length}
              {#each $notifications as n (n.id)}
          <div class="p-3 rounded-lg shadow-sm flex items-start space-x-3 border-l-4 animate-fade-in"
               class:bg-green-100={n.type==='success'}
               class:bg-blue-100={n.type==='info'}
               class:bg-red-100={n.type==='error'}
               class:bg-yellow-100={n.type==='warning'}
               class:border-green-500={n.type==='success'}
               class:border-blue-500={n.type==='info'}
               class:border-red-500={n.type==='error'}
               class:border-yellow-500={n.type==='warning'}
               class:opacity-50={n.seen}>
            <div class="flex-shrink-0 text-xl">
              {#if n.type === 'success'}✅{:else if n.type === 'info'}ℹ️{:else if n.type === 'error'}❌{:else if n.type === 'warning'}⚠️{/if}
            </div>
            <div class="flex-grow">
              <div class="text-sm font-medium text-gray-800">{n.message}</div>
              <div class="text-xs text-gray-600 mt-1">{new Date(n.timestamp).toLocaleString()}</div>
              {#if n.counter}
                <div class="text-xs text-gray-700 mt-1">Pick up at Counter {n.counter}</div>
              {/if}
            </div>
            <button
              on:click={() => notifications.dismiss(n.id)}
              class="flex-shrink-0 text-gray-400 hover:text-gray-600 text-lg"
              aria-label="Dismiss notification"
            >
              &times;
            </button>
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

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-4" in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
      <slot />
    </main>
  </div>
</div>