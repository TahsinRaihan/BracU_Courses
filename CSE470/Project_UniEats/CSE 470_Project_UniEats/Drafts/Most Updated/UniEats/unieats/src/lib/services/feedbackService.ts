
import * as feedbackRepository from '../repositories/feedbackRepository';
import { supabase } from '$lib/server/supabaseClient'; // Assuming supabaseClient is needed for auth

export async function submitFeedback(content: string) {
  const user = (await supabase.auth.getUser()).data.user;
  if (!user) {
    return { error: { message: 'User not authenticated.' } };
  }
  const error = await feedbackRepository.insertFeedback(user.id, content);
  return { error };
}
