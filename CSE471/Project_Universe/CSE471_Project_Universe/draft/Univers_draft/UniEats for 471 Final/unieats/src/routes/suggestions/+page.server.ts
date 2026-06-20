import { fail } from '@sveltejs/kit';
import * as suggestionsService from '$lib/services/suggestionsService';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request }) => {
    const formData = await request.formData();
    const title = formData.get('title') as string;
    const description = formData.get('description') as string;

    if (!title || title.trim().length === 0) {
      return fail(400, { message: 'Title is required.', title, description });
    }

    // The service handles getting the authenticated user
    const { error } = await suggestionsService.submitSuggestion(title, description);

    if (error) {
      if (error.message === 'User not authenticated.') {
        return fail(401, { message: 'You must be logged in to make a suggestion.' });
      }
      return fail(500, { message: 'An unexpected error occurred. Please try again.' });
    }

    return { success: true };
  }
};
