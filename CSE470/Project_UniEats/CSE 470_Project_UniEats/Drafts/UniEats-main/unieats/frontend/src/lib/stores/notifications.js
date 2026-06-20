
import { writable } from 'svelte/store';

function createNotifications() {
  const { subscribe, update } = writable([]);
  let counter = 0;

 
  function notify(message, type = 'info', meta = {}) {
    const id = ++counter;
    const timestamp = new Date().toISOString();
    const note = { id, message, type, timestamp, seen: false, ...meta };
    update(n => [note, ...n]);
  }

  function markSeen(id) {
    update(n => n.map(x => (x.id === id ? { ...x, seen: true } : x)));
  }

  function markAllSeen() {
    update(n => n.map(x => ({ ...x, seen: true })));
  }

  function dismiss(id) {
    update(n => n.filter(x => x.id !== id));
  }

  return { subscribe, notify, markSeen, markAllSeen, dismiss };
}

export const notifications = createNotifications();
