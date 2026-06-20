<script lang="ts">
  import '../../app.css'; // Correct path to app.css in src directory
  import { supabase } from '$lib/supabase';
  import { goto } from '$app/navigation';
  import { user, loading } from '$lib/stores/auth'; // Import the user and loading store
  import { anonymousUser } from '$lib/stores/anonymousUser'; // Import the anonymousUser store
  import { fade } from 'svelte/transition'; // Import fade transition
  import { cafeteria_notification } from '$lib/stores/cafeteria_nottification';
  import type { LayoutData } from './$types'; // Import LayoutData type

  // Remove this line if 'data' is not used in the layout
export const data: LayoutData = { user: null }; // Initialize with a default user value

 // Declare data as a prop

  let collapsed = false;
  let notifOpen = false;

  // Count unread cafeteria_notification
  $: unread = $cafeteria_notification.filter((n) => !n.seen).length;




  
</script>

{#if $loading}
  <div>Loading...</div> <!-- Display a loading indicator while the session is being loaded -->
{:else}
  <div class="flex h-screen flex-col">
    <!-- Top Header -->
    <header class="z-30 flex items-center justify-between bg-[#e5c8a8] p-4">
      <button
        on:click={() => (collapsed = !collapsed)}
        class="rounded bg-gradient-to-r from-gray-200 to-gray-300 p-2"
        aria-label="Toggle sidebar"
      >
        {#if collapsed}➡️{:else}⬅️{/if}
      </button>

      <div class="text-2xl font-black">UniEats</div>

      <div class="flex items-center space-x-2">
        {#if $anonymousUser}
          <!-- If user is logged in, show cart, cafeteria_notification, and logout button -->
          <a href="/cafeteria/cart" class="flex items-center rounded bg-gradient-to-r from-green-500 to-green-700 px-3 py-1 text-white">
            🛒
          </a>

          <!-- Notification Bell -->
          <button
            class="relative rounded bg-gradient-to-r from-yellow-200 to-yellow-300 px-3 py-1"
            on:click={() => (notifOpen = !notifOpen)}
            aria-label="cafeteria_notification"
          >
            🔔
            {#if unread}
              <span
                class="absolute top-0 right-0 inline-flex items-center justify-center rounded-full bg-red-600 px-1 text-xs font-bold text-red-100"
              >
                {unread}
              </span>
            {/if}
          </button>

          <a href="/myspace" class="rounded bg-gradient-to-r from-blue-500 to-blue-700 px-3 py-1 text-white">MySpace</a>
        {:else}
          <!-- If no user, show login and signup links -->
          <a href="/login" class="rounded bg-blue-600 px-3 py-1 text-white">Login</a>
          <a href="/signup" class="rounded bg-green-600 px-3 py-1 text-white">Sign Up</a>
        {/if}
      </div>
    </header>

    <!-- Notification Panel -->
    <aside
      class="fixed top-16 right-0 z-40 h-full transform bg-white shadow-lg transition-transform"
      class:translate-x-full={!notifOpen}
      style="width:16rem;"
    >
      <div class="flex items-center justify-between border-b p-4">
        <h2 class="font-bold">notification</h2>
        <div class="flex space-x-2">
          <button
            on:click={() => cafeteria_notification.markAllSeen()}
            class="text-sm text-blue-600 hover:underline">Mark all read</button>
          <button
            on:click={() => cafeteria_notification.dismissAll()}
            class="text-sm text-red-600 hover:underline">Clear all</button>
        </div>
      </div>
      <div class="h-[calc(100%-4rem)] space-y-3 overflow-y-auto p-4">
        {#if $cafeteria_notification.length}
          {#each $cafeteria_notification as n (n.id)}
            <div
              class="animate-fade-in flex items-start space-x-3 rounded-lg border-l-4 p-3 shadow-sm"
              class:bg-green-100={n.type === 'success'}
              class:bg-blue-100={n.type === 'info'}
              class:bg-red-100={n.type === 'error'}
              class:bg-yellow-100={n.type === 'warning'}
              class:border-green-500={n.type === 'success'}
              class:border-blue-500={n.type === 'info'}
              class:border-red-500={n.type === 'error'}
              class:border-yellow-500={n.type === 'warning'}
              class:opacity-50={n.seen}
            >
              <div class="flex-shrink-0 text-xl">
                {#if n.type === 'success'}✅{:else if n.type === 'info'}ℹ️{:else if n.type === 'error'}❌{:else if n.type === 'warning'}⚠️{/if}
              </div>
              <div class="flex-grow">
                <div class="text-sm font-medium text-gray-800">{n.message}</div>
                <div class="mt-1 text-xs text-gray-600">{new Date(n.timestamp).toLocaleString()}</div>
                {#if n.counter}
                  <div class="mt-1 text-xs text-gray-700">Pick up at Counter {n.counter}</div>
                {/if}
              </div>
              <button
                on:click={() => cafeteria_notification.dismiss(n.id)}
                class="flex-shrink-0 text-lg text-gray-400 hover:text-gray-600"
                aria-label="Dismiss notification"
              >
                &times;
              </button>
            </div>
          {/each}
        {:else}
          <p class="text-sm text-gray-500">No cafeteria_notification yet.</p>
        {/if}
      </div>
    </aside>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar (unchanged) -->
      <aside
        class="overflow-y-auto bg-[#e5c8a8]/20 p-4 transition-all duration-300"
        class:w-16={collapsed}
        class:w-48={!collapsed}
      >
        <nav class="space-y-3">
          <a href="/cafeteria" class="flex items-center rounded p-2 hover:bg-white">
            <span class="text-xl">🏠</span>{#if !collapsed}<span class="ml-2">Dashboard</span>{/if}
          </a>
          <a href="/cafeteria/menu" class="flex items-center rounded p-2 hover:bg-white">
            <span class="text-xl">🍴</span>{#if !collapsed}<span class="ml-2">Menu</span>{/if}
          </a>
          <a href="/cafeteria/cart" class="flex items-center rounded p-2 hover:bg-white">
            <span class="text-xl">🛒</span>{#if !collapsed}<span class="ml-2">Cart</span>{/if}
          </a>
          <a href="/cafeteria/favorites" class="flex items-center rounded p-2 hover:bg-white">
            <span class="text-xl">❤️</span>{#if !collapsed}<span class="ml-2">Favorites</span>{/if}
          </a>
          
          <a href="/cafeteria/feedback" class="flex items-center rounded p-2 hover:bg-white">
            <span class="text-xl">🗣️</span>{#if !collapsed}<span class="ml-2">Feedback</span>{/if}
          </a>
          <a href="/cafeteria/suggestions" class="flex items-center rounded p-2 hover:bg-white">
            <span class="text-xl">💡</span>{#if !collapsed}<span class="ml-2">Suggestions</span>{/if}
          </a>
        </nav>
      </aside>

      <!-- Main Content -->
      <main
        class="flex-1 overflow-y-auto p-4"
        in:fade={{ duration: 150 }}
        out:fade={{ duration: 150 }}
      >
        <slot />
      </main>
    </div>
  </div>
{/if}


<style>
  /* Animation for notification fade-in */
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-fade-in {
    animation: fade-in 0.3s ease-out forwards;
  }
</style>