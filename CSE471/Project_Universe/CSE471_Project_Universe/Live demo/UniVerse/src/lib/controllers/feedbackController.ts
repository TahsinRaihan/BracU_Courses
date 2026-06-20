import type { SupabaseClient } from '@supabase/supabase-js';
import * as feedbackService from '../services/feedbackService';

export async function submitFeedback(supabase: SupabaseClient, content: string, type: string, category: string) {
	const { error } = await feedbackService.submitFeedback(supabase, content, type, category);
	return { error };
}
