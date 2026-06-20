
import { supabase } from './supabaseClient';

export async function insertSuggestion(userId: string, title: string, description: string) {
  const { error } = await supabase.from('suggestions').insert({
    user_id: userId,
    title,
    description
  });
  return error;
}
