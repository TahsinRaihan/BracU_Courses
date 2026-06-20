import type { SupabaseClient } from '@supabase/supabase-js';
import * as feedbackRepository from '../repositories/feedbackRepository';

export async function submitFeedback(supabase: SupabaseClient, content: string, type: string, category: string) {
	const { data: { user } } = await supabase.auth.getUser();
	if (!user) {
		return { error: { message: 'User not authenticated.' } };
	}
	const error = await feedbackRepository.insertFeedback(supabase, user.id, content, type, category);
	return { error };
}
