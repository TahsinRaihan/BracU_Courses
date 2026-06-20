import type { PageServerLoad, Actions } from './$types';
import * as suggestionsRepository from '$lib/repositories/suggestionsRepository';
import { submitSuggestion, upvoteSuggestion } from '$lib/services/suggestionsService';

export const load: PageServerLoad = async ({ locals }) => {
    const { supabase } = locals;
    const suggestions = await suggestionsRepository.getSuggestions(supabase);
    return { suggestions };
};

export const actions: Actions = {
    submit: async ({ request, locals }) => {
        const formData = await request.formData();
        const title = formData.get('title') as string;
        const description = formData.get('description') as string;
        const category = formData.get('category') as string;

        if (!title) {
            return {
                success: false,
                message: 'Title is required.'
            };
        }

        const { error } = await submitSuggestion(locals.supabase, title, description, category);

        if (error) {
            return {
                success: false,
                message: error.message
            };
        }

        return {
            success: true
        };
    },
	upvote: async ({ request, locals }) => {
		const formData = await request.formData();
		const suggestionId = formData.get('suggestion_id');

		if (!suggestionId) {
			return {
				success: false,
				message: 'Suggestion ID is required.'
			};
		}

		const { error } = await upvoteSuggestion(locals.supabase, Number(suggestionId));

		if (error) {
			return {
				success: false,
				message: error.message
			};
		}

		return {
			success: true
		};
	}
};