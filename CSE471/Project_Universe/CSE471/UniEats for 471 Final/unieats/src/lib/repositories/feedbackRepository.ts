
import { supabase } from './supabaseClient';

export async function insertFeedback(userId: string, content: string) {
  const { error } = await supabase.from('feedback').insert({
    user_id: userId,
    content
  });
  return error;
}
