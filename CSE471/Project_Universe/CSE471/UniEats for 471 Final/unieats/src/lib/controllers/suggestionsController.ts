
import * as suggestionsService from '../services/suggestionsService';

export async function submitSuggestion(title: string, description: string) {
  const { error } = await suggestionsService.submitSuggestion(title, description);
  return { error };
}
