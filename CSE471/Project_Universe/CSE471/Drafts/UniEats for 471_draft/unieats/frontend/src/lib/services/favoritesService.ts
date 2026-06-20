
import * as favoritesRepository from '../repositories/favoritesRepository';
import { supabase } from '../repositories/supabaseClient'; // Assuming supabaseClient is needed for auth

export async function getFavoritesForCurrentUser() {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    return [];
  }
  return favoritesRepository.getUserFavorites(user.id);
}
