
import * as homeController from '$lib/controllers/homeController';

export async function load() {
  return homeController.loadHomePage();
}
