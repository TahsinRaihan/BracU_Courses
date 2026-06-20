<script lang="ts">
  import * as NavigationMenu from "$lib/components/ui/navigation-menu/index.js";
  import { navigationMenuTriggerStyle } from "$lib/components/ui/navigation-menu/navigation-menu-trigger.svelte";
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabase';
  import { NotificationController } from '$lib/controllers/notification.controller';
  
  let { children, data } = $props();
  
  // Use server-side admin status
  let isAdmin = $derived(data.isAdmin || false);
  let currentUser = $derived(data.session?.user || null);
  
  // Notification count state
  let unreadCount = $state(0);
  let isLoading = $state(true);

  // Fetch unread notification count
  async function fetchUnreadCount() {
    if (!currentUser) return;
    
    try {
      const notificationController = new NotificationController(supabase);
      const result = await notificationController.getNotificationCount(currentUser.id);
      
      if (result.success) {
        unreadCount = result.data || 0;
      }
    } catch (error) {
      console.error('Error fetching notification count:', error);
    } finally {
      isLoading = false;
    }
  }

  // Set up real-time subscription for notifications
  let channel: any;

  onMount(() => {
    fetchUnreadCount();
    
    if (currentUser) {
      channel = supabase
        .channel('notification_count')
        .on(
          'postgres_changes',
          {
            event: '*',
            schema: 'public',
            table: 'notifications',
            filter: `user_id=eq.${currentUser.id}`
          },
          () => {
            // Refresh count when notifications change
            fetchUnreadCount();
          }
        )
        .subscribe();
    }

    return () => {
      if (channel) {
        supabase.removeChannel(channel);
      }
    };
  });
</script>


<div class="min-h-[100dvh] bg-[hsl(222.2_47.4%_11.2%)] text-white overflow-hidden">
<nav class="w-full bg-transparent text-white">
  <div class="w-full flex justify-center">
    <NavigationMenu.Root viewport={false} class="max-w-max">
      <NavigationMenu.List class="flex gap-6 p-4 justify-center">
        <NavigationMenu.Item>
          <NavigationMenu.Link>
            {#snippet child()}
              <a href="/myspace" class="px-4 py-2 text-sm font-medium hover:text-white/90 focus:outline-none">Home</a>
            {/snippet}
          </NavigationMenu.Link>
        </NavigationMenu.Item>

        <NavigationMenu.Item>
          <NavigationMenu.Link>
            {#snippet child()}
              <a href="/myspace/profile" class="px-4 py-2 text-sm font-medium hover:text-white/90 focus:outline-none">Edit Profile</a>
            {/snippet}
          </NavigationMenu.Link>
        </NavigationMenu.Item>

        <NavigationMenu.Item>
          <NavigationMenu.Link>
            {#snippet child()}
              <a href="/myspace/notifications" class="px-4 py-2 text-sm font-medium hover:text-white/90 focus:outline-none flex items-center gap-2">
                Notifications
                {#if !isLoading && unreadCount > 0}
                  <span class="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full min-w-[20px] text-center">
                    {unreadCount}
                  </span>
                {/if}
              </a>
            {/snippet}
          </NavigationMenu.Link>
        </NavigationMenu.Item>

        <NavigationMenu.Item>
          <NavigationMenu.Link>
            {#snippet child()}
              <a href="/myspace/banner-request" class="px-4 py-2 text-sm font-medium hover:text-white/90 focus:outline-none">Request Ad</a>
            {/snippet}
          </NavigationMenu.Link>
        </NavigationMenu.Item>

        <NavigationMenu.Item>
          <NavigationMenu.Trigger class="px-4 py-2 text-sm font-medium !text-white hover:!text-white focus:!text-white data-[state=open]:!text-white bg-transparent hover:!bg-transparent focus:!bg-transparent data-[state=open]:!bg-transparent ring-0 focus:ring-0 shadow-none rounded-none [&>svg]:hidden transition-colors">Account</NavigationMenu.Trigger>
          <NavigationMenu.Content>
            <ul class="grid w-[160px] gap-1 p-2 bg-[hsl(222.2_47.4%_11.2%)] text-white rounded-md">
              <li>
                {#if isAdmin}
                  <NavigationMenu.Link href="/admin" class="px-3 py-2 rounded hover:bg-white/10">Admin Dashboard</NavigationMenu.Link>
                {:else}
                  <div class="px-3 py-2 rounded text-white/50 cursor-not-allowed">Admin Dashboard</div>
                {/if}
              </li>
              <li>
                <NavigationMenu.Link href="/auth/logout" class="px-3 py-2 rounded hover:bg-white/10">Logout</NavigationMenu.Link>
              </li>
            </ul>
          </NavigationMenu.Content>
        </NavigationMenu.Item>
      </NavigationMenu.List>
    </NavigationMenu.Root>
  </div>
</nav>

<main>
  {@render children?.()}
</main>
</div>
