<script lang="ts">
  import * as Table from "$lib/components/ui/table/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import type { PageData } from './$types';
  import { supabase } from '$lib/supabase'
  import { browser } from '$app/environment'
  
  let { data }: { data: PageData } = $props();
  
  let notifications = $state(data.notifications || []);
  let loading = $state(false);
  let errorMessage = $state('');
  let successMessage = $state('');
  let sessionBootstrapTrigger = $state(0);
  let pollingInterval: any = null;

  let channel: any = null;
  if (browser) {
    $effect(() => {
      // Include sessionBootstrapTrigger in dependencies to re-run when session is bootstrapped
      sessionBootstrapTrigger;
      const userId = data.session?.user?.id;
      console.log('Effect triggered - userId:', userId);
      
      if (!userId) {
        // No user yet, ensure we are not subscribed
        if (channel) {
          supabase.removeChannel(channel);
          channel = null;
        }
        
        // Try to bootstrap client auth from server session so Realtime works in this tab
        fetch('/api/session')
          .then((r) => r.json())
          .then((j) => {
            const s = j?.session;
            console.log('Session bootstrap response:', j);
            if (s?.access_token && s?.refresh_token) {
              // Set the auth session for the client SDK
              supabase.auth.setSession({
                access_token: s.access_token,
                refresh_token: s.refresh_token,
              }).then((result) => {
                console.log('Auth session set result:', result);
                // After setting session, try to get the user and start subscription
                if (result.data.user) {
                  console.log('User authenticated after bootstrap:', result.data.user.id);
                  // Force a re-run of the effect by updating a reactive variable
                  sessionBootstrapTrigger++;
                }
              });
            } else {
              console.log('No session tokens available for bootstrap');
            }
          })
          .catch((err) => {
            console.error('Session bootstrap error:', err);
          });
        return;
      }

      // Recreate the channel whenever the userId changes
      if (channel) {
        supabase.removeChannel(channel);
        channel = null;
      }

      channel = supabase
        .channel(`realtime:notifications-${userId}`)
        .on('postgres_changes', { 
          event: 'INSERT', 
          schema: 'public', 
          table: 'notifications'
        }, (payload: any) => {
          console.log('Realtime INSERT event triggered:', payload);
          const row = (payload as any).new;
          if (!row) {
            console.log('No row data in INSERT payload');
            return;
          }
          console.log('Realtime INSERT received:', row);
          console.log('Current userId:', userId, 'Row userId:', row.user_id, 'Match:', row.user_id === userId);
          if (row.user_id === userId) {
            console.log('Adding notification to list:', row);
            notifications = [row, ...notifications];
          } else {
            console.log('User ID mismatch - not adding to list');
          }
        })
        .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'notifications' }, (payload: any) => {
          const row = (payload as any).new;
          if (!row) return;
          console.log('Realtime UPDATE received:', row);
          if (row.user_id === userId) {
            notifications = notifications.map((n) => (n.id === row.id ? { ...n, ...row } : n));
          }
        })
        .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'notifications' }, (payload: any) => {
          const row = (payload as any).old;
          if (!row) return;
          console.log('Realtime DELETE received:', row);
          if (row.user_id === userId) {
            notifications = notifications.filter((n) => n.id !== row.id);
          }
        })
        .subscribe((status) => {
          console.log('Realtime subscription status:', status);
        });

      console.log('Realtime subscription started for notifications page');

      // Start polling for new notifications every 5 seconds as backup
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
      
      pollingInterval = setInterval(async () => {
        try {
          const { data: newNotifications, error } = await supabase
            .from('notifications')
            .select('*')
            .eq('user_id', userId)
            .order('created_at', { ascending: false });
          
          if (error) {
            console.error('Polling error:', error);
            return;
          }
          
          // Check if we have new notifications
          const currentIds = new Set(notifications.map(n => n.id));
          const newItems = newNotifications?.filter(n => !currentIds.has(n.id)) || [];
          
          if (newItems.length > 0) {
            console.log('Polling found new notifications:', newItems);
            notifications = [...newItems, ...notifications];
          }
        } catch (error) {
          console.error('Polling error:', error);
        }
      }, 5000);

      return () => {
        if (channel) {
          supabase.removeChannel(channel);
          channel = null;
        }
        if (pollingInterval) {
          clearInterval(pollingInterval);
          pollingInterval = null;
        }
      };
    });
  }

  async function markAsRead(notificationId: string) {
    loading = true;
    errorMessage = '';
    successMessage = '';

    try {
      const formData = new FormData();
      formData.append('notificationId', notificationId);

      const response = await fetch('?/markAsRead', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      console.log('Server response:', result);
      let actionResult: any;
      try {
        actionResult = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
      } catch {
        actionResult = result.data;
      }
      console.log('Parsed action result:', actionResult);
      
      // For SvelteKit actions, the result is often an array where the first element is the actual result
      const actualResult = Array.isArray(actionResult) ? actionResult[0] : actionResult;
      const success = actualResult && (actualResult.success === true || actualResult.success === 1);
      console.log('Action result success:', actionResult?.success);
      console.log('Action result error:', actionResult?.error);

      if (success) {
        successMessage = 'Notification marked as read';
        notifications = notifications.map(notification => 
          notification.id === notificationId 
            ? { ...notification, is_read: true }
            : notification
        );
      } else {
        errorMessage = (actualResult && actualResult.error) || 'Failed to mark notification as read';
      }
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'An error occurred';
    } finally {
      loading = false;
    }
  }

  async function markAllAsRead() {
    loading = true;
    errorMessage = '';
    successMessage = '';

    try {
      const formData = new FormData();
      // Add a dummy field since SvelteKit actions expect form data
      formData.append('action', 'markAllAsRead');

      const response = await fetch('?/markAllAsRead', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      let actionResult: any;
      try {
        actionResult = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
      } catch {
        actionResult = result.data;
      }
      
      // For SvelteKit actions, the result is often an array where the first element is the actual result
      const actualResult = Array.isArray(actionResult) ? actionResult[0] : actionResult;
      const success = actualResult && (actualResult.success === true || actualResult.success === 1);

      if (success) {
        successMessage = 'All notifications marked as read';
        notifications = notifications.map(notification => ({ ...notification, is_read: true }));
      } else {
        errorMessage = (actualResult && actualResult.error) || 'Failed to mark all notifications as read';
      }
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'An error occurred';
    } finally {
      loading = false;
    }
  }

  async function deleteNotification(notificationId: string) {
    if (!confirm('Are you sure you want to delete this notification?')) {
      return;
    }

    loading = true;
    errorMessage = '';
    successMessage = '';

    try {
      const formData = new FormData();
      formData.append('notificationId', notificationId);

      const response = await fetch('?/deleteNotification', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      console.log('Delete notification - raw response:', result);

      let actionResult: any;
      try {
        actionResult = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
      } catch {
        actionResult = result.data;
      }
      console.log('Delete notification - parsed actionResult:', actionResult);
      
      // For SvelteKit actions, the result is often an array where the first element is the actual result
      const actualResult = Array.isArray(actionResult) ? actionResult[0] : actionResult;
      console.log('Delete notification - actualResult:', actualResult);
      
      const success = actualResult && (actualResult.success === true || actualResult.success === 1);
      console.log('Delete notification - success check:', success, 'actionResult.success:', actionResult?.success);

      if (success) {
        successMessage = 'Notification deleted';
        notifications = notifications.filter(notification => notification.id !== notificationId);
        console.log('Delete notification - removed from frontend list');
      } else {
        errorMessage = (actualResult && actualResult.error) || 'Failed to delete notification';
        console.log('Delete notification - error message:', errorMessage);
      }
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'An error occurred';
      console.error('Delete notification - catch error:', error);
    } finally {
      loading = false;
    }
  }

  function getTypeIcon(type: string): string {
    switch (type) {
      case 'event': return '📅';
      case 'study_room': return '📚';
      case 'transaction': return '💰';
      case 'food_order': return '🍕';
      case 'banner_request': return '📢';
      default: return '📌';
    }
  }

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleString();
  }

  function stripTimeFromReminder(message: string): string {
    // Removes patterns like ", 5:30:00 AM" or ", 17:05:00" from the message part after the date
    return message.replace(/,\s*\d{1,2}:\d{2}:\d{2}(\s*[AP]M)?\.?/g, '');
  }

  function getDisplayMessage(notification: any): string {
    return notification.message;
  }

  const unreadCount = $derived(notifications.filter((n) => !n.is_read).length);
</script>

<div class="w-full min-h-[100dvh] pt-16 bg-[hsl(222.2_47.4%_11.2%)] text-white">
  <!-- Universe Link -->
  <a href="/" class="absolute top-4 left-4 z-10 text-sm font-extrabold leading-tight text-white hover:opacity-90 focus:outline-none focus-visible:ring-2 focus-visible:ring-white/60">
    UNI<br/>VERSE
  </a>
  
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-semibold">Notifications</h1>
      {#if unreadCount > 0}
        <button
          onclick={markAllAsRead}
          disabled={loading}
          class="px-4 py-2 text-sm font-medium text-white border border-white/20 rounded-md hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Marking...' : `Mark All as Read (${unreadCount})`}
        </button>
      {/if}
    </div>

    <!-- Messages -->
    {#if errorMessage}
      <div class="mb-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
        {errorMessage}
      </div>
    {/if}
    
    {#if successMessage}
      <div class="mb-4 p-4 bg-green-500/20 border border-green-500/50 rounded-lg text-green-200">
        {successMessage}
      </div>
    {/if}

    {#if data.error}
      <div class="mb-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
        {data.error}
      </div>
    {/if}
    
    <!-- Notifications Table -->
    {#if notifications.length > 0}
      <Card.Root>
        <Card.Content class="p-0">
          <Table.Root>
            <Table.Header>
              <Table.Row class="border-[hsl(214.3_31.8%_91.4%)]/20">
                <Table.Head class="text-[hsl(222.2_47.4%_11.2%)] font-medium">Type</Table.Head>
                <Table.Head class="text-[hsl(222.2_47.4%_11.2%)] font-medium">Title</Table.Head>
                <Table.Head class="text-[hsl(222.2_47.4%_11.2%)] font-medium">Message</Table.Head>
                <Table.Head class="text-[hsl(222.2_47.4%_11.2%)] font-medium">Date</Table.Head>
                <Table.Head class="text-[hsl(222.2_47.4%_11.2%)] font-medium">Status</Table.Head>
                <Table.Head class="text-[hsl(222.2_47.4%_11.2%)] font-medium">Actions</Table.Head>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {#each notifications as notification (notification.id)}
                <Table.Row class="border-[hsl(214.3_31.8%_91.4%)]/20 hover:bg-[hsl(214.3_31.8%_91.4%)]/5">
                  <Table.Cell class="text-2xl">
                    {getTypeIcon(notification.type)}
                  </Table.Cell>
                  <Table.Cell class="font-medium text-[hsl(222.2_47.4%_11.2%)]">
                    {notification.title}
                  </Table.Cell>
                  <Table.Cell class="text-[hsl(222.2_47.4%_11.2%)] max-w-xs">
                    <button 
                      class="truncate cursor-pointer hover:text-blue-300 transition-colors text-left w-full bg-transparent border-none p-0"
                      title={getDisplayMessage(notification)}
                      onclick={() => {
                        const msg = getDisplayMessage(notification);
                        if (notification.type === 'event' || msg.length > 50) {
                          alert(msg);
                        }
                      }}
                      onkeydown={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                          e.preventDefault();
                          const msg = getDisplayMessage(notification);
                          if (notification.type === 'event' || msg.length > 50) {
                            alert(msg);
                          }
                        }
                      }}
                    >
                      {getDisplayMessage(notification)}
                    </button>
                  </Table.Cell>
                  <Table.Cell class="text-[hsl(222.2_47.4%_11.2%)] text-sm">
                    {formatDate(notification.created_at)}
                  </Table.Cell>
                  <Table.Cell>
                    {#if notification.is_read}
                      <span class="px-2 py-1 text-xs rounded-full bg-green-500/20 text-[hsl(222.2_47.4%_11.2%)] font-medium">
                        Read
                      </span>
                    {:else}
                      <span class="px-2 py-1 text-xs rounded-full bg-blue-500/20 text-[hsl(222.2_47.4%_11.2%)] font-medium">
                        Unread
                      </span>
                    {/if}
                  </Table.Cell>
                  <Table.Cell>
                    <div class="flex gap-2">
                      {#if !notification.is_read}
                        <button
                          onclick={() => markAsRead(notification.id)}
                          disabled={loading}
                          class="px-2 py-1 text-xs font-medium text-[hsl(222.2_47.4%_11.2%)] border border-[hsl(222.2_47.4%_11.2%)]/20 rounded hover:bg-[hsl(222.2_47.4%_11.2%)]/10 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Mark Read
                        </button>
                      {/if}
                      <button
                        onclick={() => deleteNotification(notification.id)}
                        disabled={loading}
                        class="px-2 py-1 text-xs font-medium text-[hsl(222.2_47.4%_11.2%)] border border-red-500/20 rounded hover:bg-red-500/10 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Delete
                      </button>
                    </div>
                  </Table.Cell>
                </Table.Row>
              {/each}
            </Table.Body>
          </Table.Root>
        </Card.Content>
      </Card.Root>
    {:else}
      <div class="text-center py-12">
        <div class="text-6xl mb-4">📭</div>
        <h2 class="text-2xl font-semibold mb-4">No Notifications</h2>
        <p class="text-[hsl(215.4_16.3%_46.9%)]">You're all caught up! Check back later for new notifications.</p>
      </div>
    {/if}
  </div>
</div>


