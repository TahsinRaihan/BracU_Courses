
import * as specialsService from '../services/specialsService';

export async function loadToday() {
  const specials = await specialsService.getTodaySpecials();
  return { specials };
}
