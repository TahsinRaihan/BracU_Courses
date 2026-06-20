
import * as specialsRepository from '../repositories/specialsRepository';

export async function getTodaySpecials() {
  return specialsRepository.getTodaySpecials();
}
