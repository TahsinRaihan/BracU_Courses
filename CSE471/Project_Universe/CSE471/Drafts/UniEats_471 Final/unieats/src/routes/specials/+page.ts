
import * as specialsController from '$lib/controllers/specialsController';

export async function load() {
  return specialsController.loadToday();
}
