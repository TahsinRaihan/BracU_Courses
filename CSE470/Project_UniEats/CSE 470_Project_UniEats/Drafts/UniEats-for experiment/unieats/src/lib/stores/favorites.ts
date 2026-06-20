import { writable } from 'svelte/store';
import { supabase } from '$lib/supabase';

function createFavoritesStore() {
  const { subscribe, set, update } = writable<Set<number>>(new Set());

  async function fetchFavorites(userId: string) {
    const { data, error } = await supabase
      .from('favorites')
      .select('menu_item_id')
      .eq('user_id', userId);

    if (error) {
      console.error('Error fetching favorites:', error);
      return;
    }

    const favoriteIds = new Set(data.map(fav => fav.menu_item_id));
    set(favoriteIds);
  }

  async function addFavorite(userId: string, itemId: number) {
    const { error } = await supabase
      .from('favorites')
      .insert({ user_id: userId, menu_item_id: itemId });

    if (error) {
      console.error('Error adding favorite:', error);
      return;
    }

    update(ids => ids.add(itemId));
  }

  async function removeFavorite(userId: string, itemId: number) {
    const { error } = await supabase
      .from('favorites')
      .delete()
      .match({ user_id: userId, menu_item_id: itemId });

    if (error) {
      console.error('Error removing favorite:', error);
      return;
    }

    update(ids => {
      ids.delete(itemId);
      return ids;
    });
  }

  return {
    subscribe,
    fetchFavorites,
    addFavorite,
    removeFavorite,
  };
}

export const favorites = createFavoritesStore();
