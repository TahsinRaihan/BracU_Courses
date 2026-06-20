<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import NotificationToasts from '$lib/components/notification-toasts.svelte'
	import { supabase } from '$lib/supabase'
	import { toasts } from '$lib/stores/notifications'
	import { browser } from '$app/environment'

	let { children } = $props();

	let channel: any = null
	let currentUserId: string | null = null

	$effect(() => {
		if (!browser) return

		// Get current user session
		supabase.auth.getSession().then(({ data: { session } }) => {
			currentUserId = session?.user?.id || null
			setupRealtimeSubscription()
		})

		// Listen for auth state changes
		const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
			currentUserId = session?.user?.id || null
			setupRealtimeSubscription()
		})

		return () => {
			subscription.unsubscribe()
			if (channel) {
				supabase.removeChannel(channel)
				channel = null
			}
		}
	})

	function setupRealtimeSubscription() {
		// Clean up existing channel
		if (channel) {
			supabase.removeChannel(channel)
			channel = null
		}

		// Only subscribe if user is authenticated
		if (!currentUserId) return

		channel = supabase
			.channel('realtime:notifications')
			.on(
				'postgres_changes',
				{ event: 'INSERT', schema: 'public', table: 'notifications' },
				(payload: any) => {
					const row = (payload as any).new
					if (!row) return
					
					// Only show toast for current user's notifications
					if (row.user_id === currentUserId) {
						toasts.push({
							id: row.id,
							title: row.title ?? 'Notification',
							message: row.message ?? '',
							type: row.type,
							created_at: row.created_at,
						})
					}
				}
			)
			.subscribe()
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children?.()}

<NotificationToasts />
