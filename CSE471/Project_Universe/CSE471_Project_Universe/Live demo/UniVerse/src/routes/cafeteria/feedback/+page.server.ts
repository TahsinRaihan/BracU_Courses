import type { PageServerLoad, Actions } from './$types';
import * as feedbackRepository from '$lib/repositories/feedbackRepository';
import { submitFeedback } from '$lib/services/feedbackService';

export const load: PageServerLoad = async ({ locals }) => {
    const { supabase } = locals;
    const feedback = await feedbackRepository.getFeedback(supabase);
    return { feedback };
};

export const actions: Actions = {
    default: async ({ request, locals }) => {
        const formData = await request.formData();
        const content = formData.get('content') as string;
        const type = formData.get('type') as string;
        const category = formData.get('category') as string;

        if (!content) {
            return {
                success: false,
                message: 'Content is required.'
            };
        }

        const { error } = await submitFeedback(locals.supabase, content, type, category);

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