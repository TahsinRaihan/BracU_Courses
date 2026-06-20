import type { SupabaseClient } from '@supabase/supabase-js';

export async function insertFeedback(supabase: SupabaseClient, userId: string, content: string, type: string, category: string) {
	const { error } = await supabase.from('feedback').insert({
		user_id: userId,
		content: `Type: ${type}, Category: ${category}\n\n${content}`
	});
	return error;
}

export async function getFeedback(supabase: SupabaseClient) {
	const { data, error } = await supabase
		.from('feedback')
		.select('*')
		.order('created_at', { ascending: false });
	if (error) {
		console.error('Error fetching feedback:', error);
		return [];
	}
	return data;
}