
import * as suggestionsRepository from '../repositories/suggestionsRepository';
import { supabase } from '../repositories/supabaseClient'; // Assuming supabaseClient is needed for auth

export async function submitSuggestion(title: string, description: string) {
  const user = (await supabase.auth.getUser()).data.user;
  if (!user) {
    return { error: { message: 'User not authenticated.' } };
  }
  const error = await suggestionsRepository.insertSuggestion(user.id, title, description);
  return { error };
}
