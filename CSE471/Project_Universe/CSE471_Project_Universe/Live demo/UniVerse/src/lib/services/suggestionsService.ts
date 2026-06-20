import type { SupabaseClient } from '@supabase/supabase-js';
import * as suggestionsRepository from '../repositories/suggestionsRepository';

export async function submitSuggestion(supabase: SupabaseClient, title: string, description: string, category: string) {
	const { data: { user } } = await supabase.auth.getUser();
	if (!user) {
		return { error: { message: 'User not authenticated.' } };
	}
	const error = await suggestionsRepository.insertSuggestion(supabase, user.id, title, description, category);
	return { error };
}

export async function upvoteSuggestion(supabase: SupabaseClient, suggestionId: number) {
    const error = await suggestionsRepository.upvoteSuggestion(supabase, suggestionId);
    return { error };
}
