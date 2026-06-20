import * as feedbackServiceModule from '../../lib/services/feedbackService';
import { fail } from '@sveltejs/kit';

export const actions = {
    default: async ({ request }) => {
        const data = await request.formData();
        const feedbackText = data.get('content')?.toString();
        console.log('Received feedbackText:', feedbackText);

        if (!feedbackText) {
            return fail(400, {
                feedbackText,
                error: 'Feedback text is required.'
            });
        }

        try {
            await feedbackServiceModule.submitFeedback(feedbackText);
            return {
                success: true,
                message: 'Thank you for your feedback!'
            };
        } catch (error) {
            console.error('Error submitting feedback:', error);
            return fail(500, {
                feedbackText,
                error: 'Failed to submit feedback.'
            });
        }
    }
};