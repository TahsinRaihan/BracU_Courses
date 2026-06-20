
import * as feedbackService from '../services/feedbackService';

export async function submitFeedback(content: string) {
  const { error } = await feedbackService.submitFeedback(content);
  return { error };
}
