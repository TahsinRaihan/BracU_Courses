<script lang="ts">
  import Marqueeck from '@arisbh/marqueeck';
  import { onMount } from 'svelte';
  import type { ActiveBanner } from '$lib/types/banner';
  import { BannerController } from '$lib/controllers/banner.controller';
  import { supabase } from '$lib/supabase';

  let activeBanners: ActiveBanner[] = [];
  let isLoading = true;
  let error: string | null = null;

  // Fetch active banners
  async function fetchActiveBanners() {
    try {
      const bannerController = new BannerController(supabase);
      const result = await bannerController.getActiveBanners();
      
      if (result.success) {
        activeBanners = result.data || [];
      } else {
        error = result.error || 'Failed to load banners';
        console.error('Banner fetch error:', error);
      }
    } catch (err) {
      error = 'Error loading banners';
      console.error('Error fetching active banners:', err);
    } finally {
      isLoading = false;
    }
  }

  // Refresh banners every 30 seconds
  let refreshInterval: ReturnType<typeof setInterval>;

  onMount(() => {
    fetchActiveBanners();
    
    // Set up real-time subscription for banner changes
    const channel = supabase
      .channel('banner_changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'banner_requests'
        },
        () => {
          // Refresh banners when database changes
          fetchActiveBanners();
        }
      )
      .subscribe();

    // Also refresh periodically to catch time-based changes
    refreshInterval = setInterval(fetchActiveBanners, 30000); // 30 seconds

    return () => {
      supabase.removeChannel(channel);
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  });
</script>

<!-- Always show marquee, even during loading -->
<div class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white py-3 shadow-lg border-b border-indigo-500/30">
  <Marqueeck>
    {#if !isLoading && activeBanners.length > 0}
      <span class="px-4 font-bold text-lg">✱</span>
      {#each activeBanners as banner, index}
        <span class="px-4 font-bold text-lg">
          {banner.title}
          <!-- {#if banner.description}
            - {banner.description}
          {/if} -->
        </span>
        <span class="px-4 font-bold text-lg">✱</span>
      {/each}
    {:else}
      <span class="px-4 font-bold text-lg">✱</span>
      <span class="px-4 font-bold text-lg">Book your ad now!!</span>
      <span class="px-4 font-bold text-lg">✱</span>
    {/if}
  </Marqueeck>
</div>
