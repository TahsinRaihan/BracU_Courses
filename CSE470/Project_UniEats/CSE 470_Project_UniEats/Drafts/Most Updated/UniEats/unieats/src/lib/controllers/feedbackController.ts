
import * as feedbackService from '$lib/services/feedbackService';

export async function submitFeedback(content: string) {
  return await feedbackService.submitFeedback(content, userId);
}
