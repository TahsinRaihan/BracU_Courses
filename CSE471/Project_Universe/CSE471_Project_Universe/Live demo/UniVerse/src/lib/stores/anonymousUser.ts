// src/lib/stores/anonymousUser.ts
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const ANONYMOUS_USER_KEY = 'anonymous_user_id';

function createAnonymousUserStore() {
  const { subscribe, set } = writable<string | null>(null);

  if (browser) {
    let userId = localStorage.getItem(ANONYMOUS_USER_KEY);
    if (!userId) {
      userId = crypto.randomUUID();
      localStorage.setItem(ANONYMOUS_USER_KEY, userId);
    }
    set(userId);
  }

  return {
    subscribe,
    get: () => {
      if (browser) {
        return localStorage.getItem(ANONYMOUS_USER_KEY);
      }
      return null;
    }
  };
}

export const anonymousUser = createAnonymousUserStore();
