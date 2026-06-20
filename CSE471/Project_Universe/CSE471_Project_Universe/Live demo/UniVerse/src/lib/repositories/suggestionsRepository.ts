import type { SupabaseClient } from '@supabase/supabase-js';

export async function insertSuggestion(supabase: SupabaseClient, userId: string, title: string, description: string, category: string) {
	const { error } = await supabase.from('suggestions').insert({
		user_id: userId,
		title,
		description: `Category: ${category}\n\n${description}`
	});
	return error;
}

export async function getSuggestions(supabase: SupabaseClient) {
	const { data, error } = await supabase
		.from('suggestions')
		.select('*')
		.order('likes', { ascending: false })
		.order('created_at', { ascending: false });
	if (error) {
		console.error('Error fetching suggestions:', error);
		return [];
	}
	return data;
}

export async function upvoteSuggestion(supabase: SupabaseClient, suggestionId: number) {
	const { error } = await supabase.rpc('increment_likes', { suggestion_id_param: suggestionId });
	return error;
}