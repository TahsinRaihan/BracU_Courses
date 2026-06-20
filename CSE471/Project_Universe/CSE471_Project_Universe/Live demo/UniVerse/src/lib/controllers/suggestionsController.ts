import type { SupabaseClient } from '@supabase/supabase-js';
import * as suggestionsService from '../services/suggestionsService';

export async function submitSuggestion(supabase: SupabaseClient, title: string, description: string, category: string) {
	const { error } = await suggestionsService.submitSuggestion(supabase, title, description, category);
	return { error };
}

export async function upvoteSuggestion(supabase: SupabaseClient, suggestionId: number) {
    const { error } = await suggestionsService.upvoteSuggestion(supabase, suggestionId);
    return { error };
}
